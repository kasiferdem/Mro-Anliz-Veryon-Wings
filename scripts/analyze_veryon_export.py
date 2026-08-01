#!/usr/bin/env python3
"""Create metadata-only, Git-safe aggregates from a Veryon DB report ZIP.

The script never exports source row values. It emits schema/table names, counts,
column headers used for security classification, and aggregate risk counters.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


REPORT_ROOT = "Report/"
MAIN_FILES = {
    "columns": "01_kolonlar.csv",
    "constraints": "02_kisitlar.csv",
    "sizes": "03_tablo_boyutlari.csv",
    "indexes": "04_indeksler.csv",
    "objects": "05_kod_nesneleri.csv",
    "descriptions": "06_aciklamalar.csv",
}

MODULES = {
    "a": "accounts-commercial",
    "l": "labour-training",
    "o": "flight-operations",
    "q": "quality-safety",
    "s": "supply-commercial-mro",
    "t": "technical-maintenance",
    "u": "platform-configuration",
    "w": "workflow",
}

CAPABILITIES = {
    "airworthiness-fleet": r"(Reg|Aircraft|Fleet|Airworthiness|LifeCode|Defect|Journey|Reliability)",
    "maintenance-execution": r"(WorkOrder|OrderTask|WorkPackage|Card|Inspection|Maintenance|Hangar|Job|Task)",
    "materials-inventory": r"(Part|Stock|Warehouse|Receipt|Issue|Pick|Inventory|Demand|Requisition|Tool|Kit)",
    "procurement-commercial": r"(Vendor|Supplier|Purchase|RFQ|Quote|Sales|Customer|Contract|Invoice|Warranty|Consign|Loan|Repair)",
    "people-training": r"(Employee|Course|Training|Qualification|Licence|License|Skill|Competence|OJT|Roster|Labour)",
    "quality-safety": r"(Audit|Quality|Safety|Occurrence|Risk|NonConformance|Finding|Corrective)",
    "flight-operations": r"(Flight|Mission|Crew|Duty|FTL|Dispatch|Hotel|Transport)",
    "integration-reporting": r"(API|Import|Export|Interface|Report|Dashboard|Template|Middleware)",
}

SENSITIVE_HEADER = re.compile(
    r"^(?:password|passwordsalt|passwordresettoken|token|jwtid|secret|"
    r"firstname|surname|email|useremail|telephone|usertel|mobile|dateofbirth|"
    r"nationalinsuranceno|bankaccountnumber|bankibanno|bankswiftcode)$",
    re.IGNORECASE,
)
CRITICAL_HEADER = re.compile(r"(?:password|salt|token|secret|jwt)", re.IGNORECASE)
LEGACY_TYPES = {"timestamp", "ntext", "image", "money", "smalldatetime"}
CAMO_REFERENCE_TABLES = [
    "tLifeCode",
    "tTaskCode",
    "tADComplianceStatus",
    "tComplianceCategory",
    "tComplianceTaskType",
    "tMELCode",
    "tDefectStatus",
    "tAssetRemovalReason",
    "tAssetStatus",
    "sOrderTaskStatus",
    "tCardStatus",
    "tForecastFrom",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Veryon DB Report ZIP")
    parser.add_argument("--output", required=True, type=Path, help="Directory for safe aggregates")
    return parser.parse_args()


def read_csv(zf: zipfile.ZipFile, member: str) -> list[dict[str, str]]:
    raw = zf.read(member).decode("utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(raw)))


def int_value(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def parse_source_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        result = datetime.fromisoformat(normalized)
        return result.replace(tzinfo=None)
    except ValueError:
        pass
    for fmt in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue
    return None


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def security_inventory(zf: zipfile.ZipFile) -> tuple[list[dict[str, object]], dict[str, object]]:
    results: list[dict[str, object]] = []
    token_stats: dict[str, object] = {}
    current = datetime.combine(date.today(), datetime.min.time())

    for info in sorted(zf.infolist(), key=lambda item: item.filename.lower()):
        if info.is_dir() or not info.filename.startswith(f"{REPORT_ROOT}kod_tablolari/"):
            continue
        if not info.filename.lower().endswith(".csv"):
            continue

        raw = zf.read(info.filename).decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(raw))
        headers = reader.fieldnames or []
        sensitive = [header for header in headers if SENSITIVE_HEADER.search(header)]
        if not sensitive:
            continue

        row_count = 0
        nonempty = Counter()
        future_expiry = 0
        not_used_not_invalidated = 0
        for row in reader:
            row_count += 1
            for header in sensitive:
                if row.get(header):
                    nonempty[header] += 1
            if "Token" in headers:
                expiry = parse_source_datetime(row.get("ExpiryDate"))
                if expiry and expiry > current:
                    future_expiry += 1
                used = str(row.get("Used", "")).strip().lower() in {"true", "1", "yes"}
                invalidated = str(row.get("Invalidated", "")).strip().lower() in {"true", "1", "yes"}
                if not used and not invalidated:
                    not_used_not_invalidated += 1

        risk = "credential" if any(CRITICAL_HEADER.search(header) for header in sensitive) else "pii"
        results.append(
            {
                "file": info.filename,
                "risk_class": risk,
                "row_count": row_count,
                "sensitive_headers": "|".join(sensitive),
                "nonempty_counts": "|".join(f"{key}:{nonempty[key]}" for key in sorted(nonempty)),
            }
        )
        if "Token" in headers:
            token_stats[info.filename] = {
                "rows": row_count,
                "future_expiry": future_expiry,
                "not_used_not_invalidated": not_used_not_invalidated,
            }

    return results, token_stats


def analyze(input_path: Path, output_dir: Path) -> None:
    if not input_path.is_file():
        raise SystemExit(f"Input ZIP not found: {input_path}")

    with zipfile.ZipFile(input_path) as zf:
        members = set(zf.namelist())
        required = {f"{REPORT_ROOT}{name}" for name in MAIN_FILES.values()}
        missing = sorted(required - members)
        if missing:
            raise SystemExit(f"Required report files missing: {', '.join(missing)}")

        columns = read_csv(zf, f"{REPORT_ROOT}{MAIN_FILES['columns']}")
        constraints = read_csv(zf, f"{REPORT_ROOT}{MAIN_FILES['constraints']}")
        sizes = read_csv(zf, f"{REPORT_ROOT}{MAIN_FILES['sizes']}")
        indexes = read_csv(zf, f"{REPORT_ROOT}{MAIN_FILES['indexes']}")
        objects = read_csv(zf, f"{REPORT_ROOT}{MAIN_FILES['objects']}")
        descriptions = read_csv(zf, f"{REPORT_ROOT}{MAIN_FILES['descriptions']}")

        tables = sorted({(row["sema"], row["tablo"]) for row in columns})
        column_count = Counter((row["sema"], row["tablo"]) for row in columns)
        size_map = {(row["sema"], row["tablo"]): int_value(row.get("satir")) for row in sizes}
        index_count = Counter((row["sema"], row["tablo"]) for row in indexes)

        schema_names = sorted({schema for schema, _ in tables})
        schema_summary: dict[str, dict[str, int]] = {}
        for schema in schema_names:
            schema_tables = [table for table in tables if table[0] == schema]
            schema_summary[schema] = {
                "tables": len(schema_tables),
                "columns": sum(column_count[table] for table in schema_tables),
                "rows": sum(size_map.get(table, 0) for table in schema_tables),
            }

        module_rows: list[dict[str, object]] = []
        for prefix, module in MODULES.items():
            selected = [table for table in tables if table[0] == "dbo" and table[1].startswith(prefix)]
            module_rows.append(
                {
                    "prefix": prefix,
                    "module": module,
                    "tables": len(selected),
                    "columns": sum(column_count[table] for table in selected),
                    "snapshot_rows": sum(size_map.get(table, 0) for table in selected),
                    "nonempty_tables": sum(size_map.get(table, 0) > 0 for table in selected),
                    "indexes": sum(index_count.get(table, 0) for table in selected),
                }
            )

        qualified_tables = [f"{schema}.{table}" for schema, table in tables]
        capability_rows: list[dict[str, object]] = []
        for capability, pattern in CAPABILITIES.items():
            hits = sorted(
                name for name in qualified_tables if re.search(pattern, name.split(".", 1)[1], re.IGNORECASE)
            )
            capability_rows.append(
                {
                    "capability": capability,
                    "matching_tables": len(hits),
                    "sample_tables": "|".join(hits[:15]),
                    "evidence_level": "schema-name-signal",
                }
            )

        sensitive_rows, token_stats = security_inventory(zf)

        camo_reference_counts: dict[str, int] = {}
        for table in CAMO_REFERENCE_TABLES:
            member = f"{REPORT_ROOT}kod_tablolari/dbo.{table}.csv"
            if member in members:
                camo_reference_counts[f"dbo.{table}"] = len(read_csv(zf, member))

        total_rows = sum(size_map.values())
        nonempty_tables = sum(value > 0 for value in size_map.values())
        max_columns = max(column_count.values()) if column_count else 0
        top_tables = [
            {"table": f"{schema}.{table}", "rows": count}
            for (schema, table), count in sorted(size_map.items(), key=lambda item: (-item[1], item[0]))[:20]
        ]

        summary = {
            "generated_on": date.today().isoformat(),
            "source_name": input_path.name,
            "safety": "metadata-only; no source row values exported",
            "archive": {
                "entries": len(zf.infolist()),
                "files": sum(not item.is_dir() for item in zf.infolist()),
                "code_table_files": sum(
                    not item.is_dir() and item.filename.startswith(f"{REPORT_ROOT}kod_tablolari/")
                    for item in zf.infolist()
                ),
                "sample_files": sum(
                    not item.is_dir() and item.filename.startswith(f"{REPORT_ROOT}ornekler/")
                    for item in zf.infolist()
                ),
            },
            "schema": {
                "schemas": len(schema_names),
                "tables": len(tables),
                "columns": len(columns),
                "average_columns_per_table": round(len(columns) / len(tables), 2),
                "max_columns_per_table": max_columns,
                "descriptions": len(descriptions),
                "by_schema": schema_summary,
            },
            "rows": {
                "total": total_rows,
                "nonempty_tables": nonempty_tables,
                "empty_tables": len(size_map) - nonempty_tables,
                "empty_table_rate": round((len(size_map) - nonempty_tables) / len(size_map), 4),
                "top_tables": top_tables,
            },
            "constraints": dict(sorted(Counter(row["tur"] for row in constraints).items())),
            "indexes": {
                "total": len(indexes),
                "by_type": dict(sorted(Counter(row["type_desc"] for row in indexes).items())),
                "by_uniqueness": dict(sorted(Counter(row["is_unique"] for row in indexes).items())),
            },
            "code_objects": {
                "total": len(objects),
                "by_type": dict(sorted(Counter(row["tur"] for row in objects).items())),
            },
            "data_types": dict(sorted(Counter(row["tip"] for row in columns).items())),
            "legacy_data_types": {
                key: value
                for key, value in sorted(Counter(row["tip"] for row in columns).items())
                if key in LEGACY_TYPES
            },
            "relationship_naming_signals": {
                "columns_ending_with__ID": sum(row["kolon"].endswith("_ID") for row in columns),
                "columns_containing__ID": sum("_ID" in row["kolon"] for row in columns),
                "caveat": (
                    "Naming signals are not foreign keys. The broader count includes audit, creator, "
                    "default and role-qualified identifiers."
                ),
            },
            "camo_reference_table_rows": dict(sorted(camo_reference_counts.items())),
            "common_columns": dict(Counter(row["kolon"] for row in columns).most_common(20)),
            "security": {
                "sensitive_export_files": len(sensitive_rows),
                "credential_export_files": sum(row["risk_class"] == "credential" for row in sensitive_rows),
                "token_aggregates": token_stats,
            },
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "schema-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(
        output_dir / "module-summary.csv",
        module_rows,
        ["prefix", "module", "tables", "columns", "snapshot_rows", "nonempty_tables", "indexes"],
    )
    write_csv(
        output_dir / "capability-evidence.csv",
        capability_rows,
        ["capability", "matching_tables", "sample_tables", "evidence_level"],
    )
    write_csv(
        output_dir / "security-inventory.csv",
        sensitive_rows,
        ["file", "risk_class", "row_count", "sensitive_headers", "nonempty_counts"],
    )


def main() -> None:
    args = parse_args()
    analyze(args.input.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()

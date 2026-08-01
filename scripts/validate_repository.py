#!/usr/bin/env python3
"""Validate the report repository and reviewed aggregate metrics."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "SECURITY.md",
    "docs/00-executive-summary.md",
    "docs/02-veryon-database-analysis.md",
    "docs/03-competitor-comparison.md",
    "docs/04-decision-and-benefit-case.md",
    "docs/05-target-architecture.md",
    "docs/06-roadmap-and-migration.md",
    "docs/07-rfp-scorecard.md",
    "docs/08-data-mapping.md",
    "docs/09-camo-m7-extension.md",
    "research/source-register.md",
    "research/internal-observations/2026-07-25-wings-production-observation.md",
    "research/internal-observations/2026-07-31-veryon-secondary-analysis.md",
    "data/generated/schema-summary.json",
    "data/generated/module-summary.csv",
    "data/generated/capability-evidence.csv",
    "data/generated/security-inventory.csv",
]
EXPECTED = {
    ("schema", "schemas"): 10,
    ("schema", "tables"): 3166,
    ("schema", "columns"): 56828,
    ("schema", "descriptions"): 15,
    ("rows", "total"): 564223,
    ("rows", "nonempty_tables"): 651,
    ("rows", "empty_tables"): 2515,
}
EXPECTED_RELATIONSHIP_SIGNALS = {
    "columns_ending_with__ID": 9217,
    "columns_containing__ID": 14026,
}
EXPECTED_CAMO_REFERENCE_ROWS = {
    "dbo.sOrderTaskStatus": 14,
    "dbo.tADComplianceStatus": 3,
    "dbo.tAssetRemovalReason": 4,
    "dbo.tAssetStatus": 7,
    "dbo.tCardStatus": 5,
    "dbo.tComplianceCategory": 3,
    "dbo.tComplianceTaskType": 6,
    "dbo.tDefectStatus": 5,
    "dbo.tForecastFrom": 4,
    "dbo.tLifeCode": 14,
    "dbo.tMELCode": 5,
    "dbo.tTaskCode": 73,
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_local_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            if not (markdown.parent / clean).resolve().exists():
                fail(f"Broken local link in {markdown.relative_to(ROOT)}: {target}", errors)


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"Missing required file: {relative}", errors)

    forbidden_archives = list(ROOT.rglob("*.zip"))
    if forbidden_archives:
        fail("ZIP files must not be committed: " + ", ".join(str(p.relative_to(ROOT)) for p in forbidden_archives), errors)

    raw_report_dirs = [path for path in ROOT.rglob("Report") if path.is_dir()]
    if raw_report_dirs:
        fail("Extracted Report directories must not be committed", errors)

    forbidden_internal_notes = [
        path
        for path in ROOT.rglob("*.md")
        if path.name.casefold() in {"wings-analiz.md", "veryon-analiz.md"}
    ]
    if forbidden_internal_notes:
        fail(
            "Raw internal notes must not be committed: "
            + ", ".join(str(path.relative_to(ROOT)) for path in forbidden_internal_notes),
            errors,
        )

    summary_path = ROOT / "data/generated/schema-summary.json"
    if summary_path.is_file():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            for keys, expected in EXPECTED.items():
                actual = summary
                for key in keys:
                    actual = actual[key]
                if actual != expected:
                    fail(f"Metric {'.'.join(keys)} expected {expected}, got {actual}", errors)
            if summary.get("safety") != "metadata-only; no source row values exported":
                fail("Missing metadata-only safety marker", errors)
            constraint_expected = {"CHECK": 6, "FK": 404, "PK": 3091, "UQ": 19}
            if summary.get("constraints") != constraint_expected:
                fail(f"Constraint metrics changed: {summary.get('constraints')}", errors)
            relationship_signals = summary.get("relationship_naming_signals", {})
            for key, expected in EXPECTED_RELATIONSHIP_SIGNALS.items():
                if relationship_signals.get(key) != expected:
                    fail(
                        f"Relationship naming signal {key} expected {expected}, "
                        f"got {relationship_signals.get(key)}",
                        errors,
                    )
            if summary.get("camo_reference_table_rows") != EXPECTED_CAMO_REFERENCE_ROWS:
                fail(
                    "CAMO reference counts changed: "
                    f"{summary.get('camo_reference_table_rows')}",
                    errors,
                )
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            fail(f"Invalid schema summary: {exc}", errors)

    for relative, expected_headers in {
        "data/generated/module-summary.csv": [
            "prefix", "module", "tables", "columns", "snapshot_rows", "nonempty_tables", "indexes"
        ],
        "data/generated/capability-evidence.csv": [
            "capability", "matching_tables", "sample_tables", "evidence_level"
        ],
        "data/generated/security-inventory.csv": [
            "file", "risk_class", "row_count", "sensitive_headers", "nonempty_counts"
        ],
    }.items():
        path = ROOT / relative
        if path.is_file():
            with path.open(encoding="utf-8", newline="") as handle:
                headers = next(csv.reader(handle), [])
            if headers != expected_headers:
                fail(f"Unexpected CSV headers in {relative}: {headers}", errors)

    validate_local_links(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Veryon — ikincil analiz çapraz kontrolü

**Evidence ID:** `INT-VERYON-2026-07-31`

**Kaynak tipi:** Kullanıcı tarafından sağlanan ikincil analiz

**Ham dosya:** Depoya alınmadı

**SHA-256:** `947320F411FCA06BD3D27C5D719CACA0E697E818DC9BAF67DD0633FF69458C4C`

## Veri sınıflandırması

Ham not; veritabanı sunucu/instance adı ve yerel kaynak konumları içerir. Public GitHub için uygun değildir. Bulgular kaynak ZIP üzerinde yeniden sayılmış ve aşağıda düzeltilmiştir.

## Çapraz kontrol

| İddia | Sonuç | Yeniden üretilebilir kanıt |
|---|---|---|
| Rusada ENVISION / nGen kökeni | Doğrulandı | `uRusada*`, `nGenImport`, `ENV*` isimleri; Veryon'un resmî eski-ad beyanı |
| 3.166 tablo / 56.828 kolon | Doğrulandı | `schema-summary.json` |
| 2.954 procedure / 4.110 trigger / 2.348 view | Doğrulandı | `schema-summary.json` |
| 404 deklaratif FK | Doğrulandı | `02_kisitlar.csv` toplulaştırması |
| 13.457 örtük ilişki | **Doğrulanmadı** | `_ID` ile biten 9.217; `_ID` içeren 14.026 kolon. Geniş ölçüm audit/default/qualified alanları da içerir; ikisi de gerçek ilişki sayısı değildir. |
| `t` alanında 956 tablo | Farklı sonuç | Aynı deterministic script `dbo` altında küçük `t` ile başlayan 959 tablo sayar. |
| `wComponent` 3.522 / `wComponentAction` 4.680 / `wWorkFlow` 1.729 | Doğrulandı | Tablo satır sayıları |
| `uRoleComponent` 342.237 | Doğrulandı | Tablo satır sayısı |
| `api` + `webapi` 61 tablo | Doğrulandı | 29 + 32 |
| `import` + `nGenImport` 297 tablo | Doğrulandı | 253 + 44 |

## Doğrulanan CAMO sinyalleri

- `tCard` 198 kolon: maliyet tahmini/notları, man-hour, weight/moment/station, engineering reference, affected manuals, AMOC ve AD-related task alanları.
- `tLifeCode` 14 referans kaydı ve `tTaskCode` 73 referans kaydı.
- `tPublication` ile publication/revision/subscription/effectivity/review sinyalleri; AD compliance tarafında AMOC bulunması.
- `tAsset_IDHigherAssembly`, `CamoConfirmationRequired`, certificate ve software version alanları.
- `tRegJourney` içinde departure/arrival, take-off/landing ve tech-log referansı.
- `tForecastScenario` içinde daily/weekly/monthly/yearly, by-registration ve default flag'leri; `tForecastFrom` için dört başlangıç yaklaşımı.
- MEL/defect status, removal reason, asset lifecycle ve work-order task QC/requisition state referansları.

## Temiz oda ve fikrî mülkiyet sınırı

Kod tablolarındaki değerler doğrudan FOX seed data'sı olarak kopyalanmamalıdır. Endüstri terimleri kuruluşun onaylı prosedürü, lisanslı standart/OEM kaynağı ve hukukî değerlendirme ile bağımsız sözlük olarak kurulmalıdır. Veryon şeması gereksinim keşfi kanıtıdır; hedef modelin kaynağı değildir.

# 08 — Veryon → FOX kavramsal eşleme

Bu belge migration specification değildir. Tablo ailelerinden canonical FOX entity'lerine temiz oda eşlemesidir; kolon düzeyi dönüşüm, veri profillemesi ve business owner onayı ayrıca yapılır.

| Veryon aile/sinyali | FOX canonical model | Dönüşüm notu |
|---|---|---|
| `aCompany`, `aAccount*` | Organization / BusinessPartner | Customer, supplier, owner ve billing rollerini ayrı ilişki olarak modelle |
| `sPart*` | Part / PartRevision / Applicability / Alternate | PN normalize değeri ve görünen değeri ayrı; kaynak/revizyon zorunlu |
| `sPartCondition`, `sPartStatus` | ConditionCode / EligibilityState | Teknik condition ile kullanılabilirlik kararını ayır |
| `sStock*` | StockItem / StockLot / InventoryBalanceProjection | Balance değil event kaynak; owner/location/status ayrı |
| `sBaseWarehouse*`, `sBaseLocation*` | Site / Warehouse / Location | Hiyerarşi, special storage ve active date aralığı |
| `sDemand*` | Demand / DemandLine / SourcingCase | Bakım, satış, replenishment ve AOG nedenini tiplenmiş tut |
| `sVendorOrder*`, `sOrder*`, `sOrderPart*` | CommercialOrder / OrderLine / Schedule | Purchase/repair/exchange/loan/consignment subtype |
| `sDemandQuote*`, `sCustomerQuote*` | RFQ / SupplierQuote / CustomerQuote | Quote revision ve approval snapshot korunur |
| `sOrderPartReceipt*` | Receipt / ReceiptLine / Inspection / Discrepancy | Receipt, acceptance ve inventory event farklı kayıtlar |
| `sPartDocument`, `*ReceiptDocument`, `*Cert*` | EvidenceDocument / CertificatePackage | Binary object storage'da; metadata/hash/verification FOX'ta |
| `sConsignmentStock`, `sStockOwnership` | Ownership / UsageRight | Fiziksel possession ve legal/commercial ownership ayrılır |
| `sCoreReturn*` | ExchangeCoreObligation | Due, charge, received ve accepted eventleri |
| `sRepair`, repair order sinyalleri | RepairOrder / RepairEvent | Vendor repair ve internal component work sınırı açık olmalı |
| `sScrap*`, `sPartWriteOff` | ScrapCase / InventoryEvent(SCRAP) | Maker-checker, evidence ve normal harekete kapalı terminal state |
| `aWarranty*` | WarrantyTerm / WarrantyAssessment / WarrantyClaim | Coverage snapshot ve source transaction link |
| `tReg*` | ExternalAircraft / AircraftRegistration | Başlangıçta M&E master; kaynak/revizyon/provenance ile M7A projection |
| `tPublication*`, publication/manual sinyalleri | PublicationRevision / RequirementSource | Özel yayın içeriği kopyalanmaz; lisanslı kaynak kimliği, revision ve effectivity tutulur |
| `tCard*` | TaskRequirement / TaskRevision / CostAndWBProjection | Vendor kolon yapısı kopyalanmaz; maliyet, W&B, AD/AMOC ve etkilenen manual gereksinimleri temiz oda modeline ayrılır |
| `tAsset*` | AircraftAsset / Installation / ConfigurationSnapshot | Higher assembly, certificate ve software configuration zaman etkili ilişki olarak; M7A'da read-only |
| `tRegJourney*` | Journey / CounterSourceEvent | Departure/arrival/takeoff/landing/tech-log provenance; düzeltme event'i ve reconciliation zorunlu |
| `tForecastScenario*`, `tForecastFrom*` | ForecastScenario / ForecastRun / DueProjection | Algorithm/configuration version, as-of time, input snapshot ve reason trace olmadan sonuç kabul edilmez |
| `tDefect*`, MEL/compliance/status sinyalleri | DefectReference / OperationalConstraint / ComplianceState | Referans değerler doğrudan seed edilmez; onaylı kuruluş sözlüğüne eşlenir |
| `lEmployee*` | PersonReference / EmploymentSnapshot | Authentication IdP'de; HR master kopyalanmaz |
| `lCourse*`, `lQualification*`, `lLicence*` | CourseRevision / Completion / Qualification / Licence | Her kanıt kendi revision ve validity aralığına bağlı |
| `lEmployeeRole/Right`, `uRole*` | AccessRole / PolicyBinding | Business authorization ile UI permission ayrılır |
| `qAudit*`, `qOccurrence*`, `qRisk*` | Audit / Finding / Action / Occurrence / Risk | SQL condition yerine sürümlü, testli policy expression |
| `uRALUser*`, `AuthRefreshTokens` | **Göç edilmez** | Kullanıcı auth IdP'de yeniden provision edilir; secret import edilmez |
| `uReport*`, `uTemplate*`, `wWorkFlow*` | ReportDefinition / FormRevision / WorkflowPolicy | Yalnız işçe onaylı aktif tanımlar taşınır; vendor UI metadata kopyalanmaz |
| `api`, `webapi`, `interfaces`, `nGenImport` | Connector / MappingVersion / InboxOutbox | Tarihsel staging kayıtları canonical domain'e alınmaz |

## Zorunlu dönüşüm kuralları

### Kimlik

- Her source record için `source_system`, `source_table`, `source_id`, `source_version` crosswalk tutulur.
- FOX primary key'i source numeric ID değildir.
- Aynı iş nesnesinin birden çok source kaydı business-approved merge kaydı ile çözülür.

### Tarih ve sentinel değerler

Referans veride `1900-01-01` benzeri sentinel tarihler görülür. FOX'ta “bilinmiyor/yok” için `null` ve gerekirse ayrı reason code kullanılır; sentinel tarih taşınmaz.

### Kullanıcı ve audit

- Source user ID, gerekiyorsa historical actor reference'a eşlenir.
- Parola, salt, reset token ve refresh token taşınmaz.
- Historical actor bulunamazsa `LEGACY_UNKNOWN` kullanılır; uydurma aktif kullanıcı yaratılmaz.

### Durumlar

- Birden çok boolean durum alanı canonical state machine'e çevrilir.
- Çelişkili boolean kombinasyonları exception queue'ya gider.
- Geçmiş olay üretilebiliyorsa state + transition history taşınır; yalnız son durumdan sahte event üretilmez.
- Veryon code-table satırları FOX seed verisi olarak kopyalanmaz; aynı terim endüstri standardı olsa bile kaynak, lisans ve kuruluş onayı kaydedilir.

### Miktar ve para

- UOM dönüşümü sürümlü katalogla yapılır; seri numaralı item quantity=1 invariant'ı doğrulanır.
- Tutar, currency, exchange rate source/date ve rounding ayrı alanlardır.
- Landed cost bileşenleri tek unit price içine kaybedilmez.

### Belge

- Dosya MIME/type/size/hash kontrol edilir.
- OCR değeri ile human-verified değer ayrı tutulur.
- Certificate package completeness policy version'a göre yeniden hesaplanır; eski sistemdeki “accepted” değeri körlemesine kullanılmaz.

## Mutabakat çıktıları

Her migration dalgası şu raporları üretmelidir:

- Source/accepted/rejected/quarantined sayıları
- Duplicate ve merge disposition
- Unknown code/UOM/currency listesi
- Serial/lot/owner/location farkı
- Certificate hash/completeness farkı
- Açık demand/order quantity ve status farkı
- Actor/policy/audit link coverage

İş sahibi imzası olmayan exception otomatik olarak “başarılı göç” sayılmaz.

# 06 — Yol haritası ve geçiş

## Ön koşul: güvenlik ve yönetişim — 0–2 hafta

- Veryon export kopyalarını bulun, erişimi sınırlandırın ve retention kararı alın.
- Token/parola rotasyonu gerekip gerekmediğini kaynak sistem sahibiyle teyit edin.
- FOX ürün sahibi, compliance owner, data owner ve security owner atayın.
- Kuruluş tipi, yetkiler, MOE/MTOE prosedürleri, sertifika ve saklama kurallarını kesinleştirin.

Çıkış kapısı: hassas veri olayı kapatılmış veya takip planına alınmış; karar sahipleri atanmış.

## Faz 0 — ürün ve entegrasyon sınırı — 2–4 hafta

- FOX Store + FOX Training ortak sözlüğünü oluşturun.
- M&E/CAMO ve ERP için system-of-record matrisi onaylayın.
- 20 çekirdek ve 5 opsiyonel CAMO demo/pilot senaryosunu gerçek kullanıcılarla doğrulayın.
- Bir site, bir warehouse ve bir part class pilotunu seçin.

Çıkış kapısı: onaylı kapsam, canonical entity listesi, API erişimi ve pilot baseline KPI.

## Faz 1 — ortak platform temeli — 6–8 hafta

- Organization/site/person bağlantıları, OIDC, RBAC/ABAC.
- Evidence metadata, immutable object storage, audit event ve outbox.
- Policy/revision altyapısı, maker-checker ve notification job'ları.
- Dev/test/prod, backup/restore, observability ve CI quality gates.

Çıkış kapısı: tenant isolation, audit completeness ve restore tatbikatı.

## Faz 2 — kontrollü depo dikey dilimi — 8–10 hafta

- Part/revision/alternate/effectivity referansı.
- Receipt → quarantine/inspection → release/reject.
- Serial/lot/batch stock item, owner, condition, location.
- Append-only inventory event, reservation, pick/issue/return/count/scrap.
- Certificate package ve source-to-current trace.

Çıkış kapısı: fiziksel sayımla mutabakat; eksik belge ile serviceable geçişinin teknik olarak engellenmesi.

## Faz 3 — tedarik ve satış — 8–10 hafta

- Demand, shortage, RFQ, quote comparison ve approval.
- Purchase, repair, exchange, loan ve consignment order.
- Vendor approval/performance, receipt match ve landed cost.
- Customer quote/order, allocation, shipment, return ve core due.
- ERP invoice/accounting events.

Çıkış kapısı: demand-to-available ve quote-to-cash pilotları; partial receipt, AOG, core ve RMA senaryoları.

## Faz 4 — training ve authorization gate — 8–12 hafta

- Course revision, completion/evidence, expiry.
- Competence assessment, OJT/practical, findings.
- Authorization issuance/suspension/revocation ve scope.
- Synchronous eligibility API ve M&E assignment/sign-off entegrasyonu.

Çıkış kapısı: expired/suspended/mismatched scope için deny-path E2E testleri; karar snapshot'ı ve evidence bundle.

## Faz 5 — M&E entegrasyonu ve yayılım — 8–12 hafta

- Aircraft/task/work package/demand sözleşmeleri.
- Material request, availability, issue/install/return acknowledgement.
- Correlation/reconciliation workbench ve retry/dead-letter.
- Site ve part class dalgaları; legacy read-only erişim.

Çıkış kapısı: günlük mutabakat sıfır açıklanamayan fark; rollback ve AOG continuity tatbikatı.

## Faz 6 — M7A CAMO gözetimi — 10–14 hafta

- Authoritative M&E/CAMO'dan aircraft configuration, counters, requirements, compliance ve forecast feed'i.
- Kaynak/revizyon/provenance koruyan normalize read model.
- Bağımsız due/forecast projection, applicability değerlendirmesi ve fark açıklaması.
- Journey/counter, asset configuration, AD/SB/AMP ve forecast reconciliation workbench.
- Düzeltme önerisi ve maker-checker; authoritative sisteme otomatik yazım yok.

Çıkış kapısı: en az iki kapalı bakım döngüsünde deterministik tekrar üretim; kritik farkların tamamında owner/disposition; stale/missing feed'de fail-safe davranış.

## Faz 7 — M7B opsiyonel yetkili CAMO — ayrı yatırım kararı

Bu faz takvime otomatik eklenmez. Sınırlı aircraft fleet/domain için ancak veri kalitesi eşiği, paralel işletim, bağımsız compliance validation, business continuity, rollback, MOE değişikliği ve gerekiyorsa otorite onayı tamamlanırsa başlatılır. Work-card execution ve maintenance release ayrıca kapsamlandırılır.

## Veryon'dan veri geçişi

### 1. Kaynak sınıflandırması

Her tablo ailesi için `migrate`, `reference`, `archive-only`, `exclude-sensitive` kararı verilir. Tüm 3.166 tabloyu taşımak hedef değildir.

### 2. Landing ve zincirleme kayıt

- Şifreli, erişimi sınırlı landing alanı.
- Export zamanı, source version, dosya hash'i ve extract job kaydı.
- Kullanıcı/token/parola tabloları varsayılan exclude.

### 3. Canonical mapping

- Source ID → FOX ID crosswalk.
- Kod değeri → kontrollü FOX sözlüğü; bilinmeyen değer quarantine queue'ya.
- Tarih, timezone, currency, UOM ve owner normalization.
- Duplicate part/serial/person/supplier çözümü iş sahibinin onayıyla.

### 4. Dalga sırası

1. Organization/site/location ve kontrollü sözlükler
2. Part ve approved relationships
3. Supplier/customer ve approvals
4. Açık stock + certificate/evidence
5. Açık demand/order/receipt/repair/exchange/loan
6. Training/qualification/authorization
7. Gerekli tarihsel event ve audit referansları
8. M7A seçilirse aircraft/configuration/counter/requirement/compliance snapshot'ları; önce read-only ve tam provenance ile

### 5. Mutabakat

- Kayıt sayısı tek başına yeterli değildir.
- Quantity/UOM, owner, condition, location, serial uniqueness ve certificate completeness ayrı mutabakat edilir.
- Finans için değer ve kur farkı ERP ile karşılaştırılır.
- Her exception owner, reason ve disposition taşır.

## Paralel işletim

- Çekirdek geçişte ilk hafta read-only shadow; FOX karar üretmez.
- Sonra sınırlı command dual-check; tek sistem writer kalır.
- Günlük stock/order/eligibility reconciliation.
- Cutover öncesi açık işlemler freeze window veya event delta ile taşınır.
- Rollback, FOX eventlerini silmez; compensating action ve source ownership dönüşü kullanır.
- M7A CAMO paralel işletimi en az iki kapalı bakım döngüsü sürer; kaynak sistem tek writer kalır.
- M7B kararı verilirse her yetkili domain ayrı cutover/rollback ve MOE/otorite kanıtı taşır.

## Go-live durdurma kriterleri

- Açıklanamayan serial/lot/owner/location farkı
- Certificate ve quarantine kurallarının onaysız olması
- Cross-tenant erişim veya privilege escalation açığı
- Duplicate movement üreten retry davranışı
- Eligibility API'nin stale veriyle allow verebilmesi
- ERP/M&E double-write ve rollback'in test edilmemesi
- AOG continuity yönteminin tatbik edilmemesi

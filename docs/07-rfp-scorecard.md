# 07 — RFP ve demo puan kartı

## Puanlama

Her senaryoyu 0–5 puanlayın:

| Puan | Tanım |
|---:|---|
| 0 | Yok / roadmap sözü |
| 1 | Ağır özel geliştirme veya manuel workaround |
| 2 | Kısmi, yüksek operasyon riski |
| 3 | Standart fonksiyon; önemli konfigürasyon gerekir |
| 4 | Güçlü standart fonksiyon; küçük konfigürasyon |
| 5 | Canlı demoda uçtan uca, audit ve API kanıtıyla çalıştı |

Her puanın yanında `kanıt türü`, `ürün sürümü`, `ek lisans`, `customization`, `API davranışı` ve `bilinen sınır` yazılmalıdır.

## 20 zorunlu senaryo

| # | Senaryo | Beklenen kanıt |
|---:|---|---|
| 1 | Exact PN + approved alternate + effectivity araması | Kaynak/revizyon ve neden uygun/uygun değil açıklaması |
| 2 | AOG demand ve paralel sourcing | SLA, escalation; kalite bypass olmaması |
| 3 | Purchase/repair/exchange/loan/consignment | Tek order çekirdeği, tipe özel kurallar |
| 4 | RFQ ve quote comparison | Landed cost, TAT, certificate promise, vendor risk |
| 5 | Partial receipt ve backorder | Quantity/UOM ve açık bakiye |
| 6 | Receipt → inspection → quarantine → release | Yetki, maker-checker, zorunlu belge |
| 7 | Eksik/şüpheli certificate | Serviceable/issue engeli ve discrepancy |
| 8 | Serial duplicate | DB/API/UI seviyesinde engelleme |
| 9 | Lot split/merge | Quantity conservation ve trace |
| 10 | Customer/consignment/loan ownership | Fiziksel stoktan ayrı kullanım hakkı |
| 11 | Reservation/pick/issue/install/return | Work task korelasyonu ve idempotency |
| 12 | Exchange core due | Due, charge, return ve closure |
| 13 | Warranty claim | Removal/task/receipt/cost ve status history |
| 14 | Scrap | Yetki, reason, evidence ve geri döndürülemez normal hareket |
| 15 | Cycle count | Freeze, variance approval, reversal ve audit |
| 16 | Training expiry | Assignment/sign-off için synchronous deny |
| 17 | Authorization scope mismatch | Aircraft/task/site/time bazlı reason code |
| 18 | Offline/mobile depo veya hangar | Conflict, retry ve duplicate önleme |
| 19 | API retry | Aynı idempotency key ile tek movement |
| 20 | Audit bundle | Bir stock item/work task için dakikalar içinde kaynak→sonuç kanıtı |

## 5 opsiyonel CAMO senaryosu

Airline/CAMO kapsamı veya M7A seçeneği değerlendiriliyorsa aşağıdaki paket de zorunludur:

| # | Senaryo | Beklenen kanıt |
|---:|---|---|
| 21 | Publication/AMP revision impact assessment | Kaynak revizyon, applicability, etkilenen task/asset ve onay izi |
| 22 | AD compliance ve AMOC | Status, compliance task, AMOC reference/approval ve geçmiş karar snapshot'ı |
| 23 | Journey/counter reconciliation | Tech-log/journey kaynağı, düzeltme, late feed ve forecast yeniden hesaplama |
| 24 | Deterministic maintenance forecast | Aynı input/revizyonla aynı due sonucu, günlük/haftalık/aylık scenario ve reason trace |
| 25 | CAMO confirmation/configuration exception | Higher assembly, removal/install, certificate/software ve maker-checker çözümü |

## Teknik ve sözleşmesel sorular

### Veri ve entegrasyon

- Tüm müşteri verisi ve ekleri açık, belgeli formatta export edilebilir mi?
- API coverage yüzde kaç; hangi işlemler yalnız UI/custom SDK ile yapılır?
- Webhook/outbox, idempotency, rate limit, pagination ve delta feed nasıl çalışır?
- Sandbox ve anonymized production-like veri sağlanır mı?
- Direct database erişimi gerekiyor mu; upgrade'de compatibility garantisi nedir?

### Güvenlik

- SSO/OIDC/SAML, MFA, SCIM, session ve token rotation desteği?
- Tenant isolation, encryption, key ownership ve subprocessor listesi?
- Audit log export, immutability ve retention?
- Pen test/SOC/ISO kanıtı ve vulnerability SLA?
- Data residency, backup, RPO/RTO ve restore tatbikatı?

### Ürün ve yaşam döngüsü

- Ürün sürümü, support policy, release cadence ve deprecation süresi?
- Customization upgrade testini kim yapar ve maliyeti kim taşır?
- CORRIDOR için CAMP Aviate'a geçiş takvimi, haklar, veri göçü ve fiyat koruması?
- WINGS için güncel Java/Oracle versiyonları, mobile store durumu, API dokümanı ve güvenlik roadmap'i?
- WINGS'te SPA/modern arama ile frame/JSP ve F7/F8 sorgu davranışının ürün yol haritası; accessibility ve browser desteği?
- WINGS project/work-package customer/internal approval ayrımı API/audit'te nasıl temsil edilir; detailed work-card imza/stamp ve independent inspection nasıl kanıtlanır?
- Veryon/TRAX/Ramco için modül bağımlılıkları ve minimum lisans seti?

### Ticari

- Beş yıllık TCO, para birimi, fiyat artış tavanı ve minimum commit?
- Implementation milestone'ları, acceptance criteria ve delay remedy?
- Data export/exit assistance ücreti ve sözleşme sonu erişim süresi?
- 24/7 AOG support, severity tanımı ve service credit?

## Pilot kabul koşulu

Ürün kısa listeye ancak şu koşullarda kalır:

- 20 çekirdek senaryonun en az 16'sı gerçek veriye yakın pilotta puanlanmış olmalı.
- Senaryo 6, 7, 8, 16, 17, 19 ve 20'nin hiçbiri 4'ün altında olmamalı.
- Veri export ve exit planı sözleşme eki olmalı.
- Kritik özelliklerin “roadmap” olması kabul edilmemeli.
- Toplam puan kadar kanıt güveni ve customization sayısı raporlanmalı.
- CAMO kapsamı varsa 21–25'in tamamı puanlanmalı; 22, 23, 24 ve 25'in hiçbiri 4'ün altında olmamalı.

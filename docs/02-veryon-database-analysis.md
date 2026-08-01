# 02 — Veryon veritabanı analizi

## Ürünün kimliği

Dökümdeki `uRAL*`, `uRusada*`, `nGenImport`, `ENV*` ve benzeri isimler, veritabanının Veryon Tracking+'ın önceki adı Rusada ENVISION kökenli olduğunu güçlü biçimde gösteriyor. Veryon da Tracking+'ı resmî olarak “formerly Rusada ENVISION” şeklinde tanımlıyor.

## Yapısal profil

| Alan | Değer |
|---|---:|
| Şema | 10 |
| Tablo | 3.166 |
| Kolon | 56.828 |
| Ortalama kolon / tablo | 18,0 |
| En geniş tablo | 198 kolon |
| PK / FK / UQ / CHECK | 3.091 / 404 / 19 / 6 |
| İndeks | 4.662 |
| SQL trigger | 4.110 |
| Stored procedure | 2.954 |
| View | 2.348 |
| Scalar/table/inline function | 201 / 39 / 15 |
| Extended description | 15 |

En büyük şema `dbo`dur: 2.768 tablo ve 51.632 kolon. `import` 253, `nGenImport` 44, `api` 29, `webapi` 32 tablo içerir. Bu dağılım, ana uygulamanın yanında veri göçü, API ve entegrasyon için ayrı katmanların zaman içinde eklendiğini gösterir.

### İlişki adlandırma sinyalleri

Tanımlı foreign key sayısı **404**'tür. Ek ikincil notta geçen “13.457 örtük ilişki” sayısı aynı kuralla yeniden üretilemedi. Ana export üzerinde açık iki sayım yapılmıştır:

- Adı `_ID` ile biten kolon: **9.217**
- Adının herhangi bir yerinde `_ID` geçen kolon: **14.026**

İkinci küme audit/default/configuration alanlarını da içerebilir; iki sayı da “gerçek ilişki” değildir. Yalnız uygulama tarafından yönetilen olası referanslar için inceleme kuyruğu üretir. Gerçek bağ için hedef tablo, cardinality, null davranışı ve iş kuralı ayrıca doğrulanmalıdır.

## Modül izleri

Aşağıdaki eşleme tablo adlarına dayalıdır; ürünün resmî modül lisanslaması değildir.

| Ön ek | Yorumlanan alan | `dbo` tablo | Kolon | Snapshot satırı | Örnek kanıt |
|---|---|---:|---:|---:|---|
| `a` | Ticari, sözleşme, muhasebe, warranty | 246 | 4.536 | 185 | `aContract`, `aWarrantyClaim`, `aJournal` |
| `l` | Personel, eğitim, lisans, roster | 288 | 5.137 | 926 | `lEmployee`, `lCourseRevision`, `lQualification` |
| `o` | Flight/mission/crew/FTL | 77 | 1.305 | 203 | `oMission`, `oDuty`, `oFTLRule` |
| `q` | Kalite, audit, occurrence, risk | 129 | 2.402 | 158 | `qAudit`, `qOccurrence`, `qRisk` |
| `s` | Supply, procurement, MRO commercial | 691 | 13.960 | 974 | `sPart`, `sStock`, `sDemand`, `sOrder` |
| `t` | Teknik bakım, asset, card, defect, fleet | 959 | 18.179 | 16.321 | `tAsset`, `tCard`, `tDefect`, `tRegJourney` |
| `u` | Platform, güvenlik, konfigürasyon, rapor | 324 | 5.208 | 462.605 | `uRALUser`, `uRoleComponent`, `uTemplate` |
| `w` | Workflow ve UI bileşenleri | 27 | 422 | 35.046 | `wWorkFlow`, `wComponent`, `wWorkFlowNodes` |

Toplam satırın çok büyük bölümü `u` ve `w` platform/konfigürasyon alanlarındadır. `uRoleComponent` tek başına 342.237 satırla snapshot'ın yaklaşık %60,7'sini oluşturur.

## Fonksiyonel kapsam kanıtları

### Teknik bakım ve CAMO

- Aircraft/registration, asset history, life code, defect, task card, forecast, reliability ve journey aileleri bulunur.
- 198 kolonlu `tCard`; manhour/material/modkit/tooling/access maliyetleri, weight/moment/station, publication/manual etkileri, AD bağlantısı ve AMOC/reference alanlarını birlikte taşır.
- `tAsset`; higher-assembly, CAMO confirmation, certificate ve software configuration sinyalleri içerir. `tRegJourney` departure/arrival/takeoff/landing/tech-log bağını, `tForecastScenario` ise günlük/haftalık/aylık/yıllık/registration bazlı senaryo tasarımını gösterir.
- Life/task code, AD compliance, compliance category/type, MEL, defect, removal reason, asset/card/order-task status ve forecast-from için ayrı referans tabloları bulunur. Bu, yalnız kayıt saklama değil kontrollü CAMO karar uzayı sinyalidir.
- Base hangar, bay, work order/task, NRC, independent inspection ve sign-off izleri vardır.
- Model/serial applicability ve interchangeability için ayrı yapılar görülür.

### Supply chain ve commercial MRO

- `sPart`, `sStock`, `sDemand`, `sVendorOrder`, `sCustomerQuote` ve geniş `sOrderPart*` aileleri yer alır.
- Purchase, repair, exchange ve loan tipleri `sOrderPartType` referansında açıkça modellenmiştir.
- Receipt/inspection, discrepancy, core return, warranty, scrap, stock check ve consignment izleri vardır.
- Demand durumları planned, back order, on order, reserved, picked ve issued aşamalarını ayırır.

### İnsan, eğitim ve yetki

- Employee, role/right, course revision, exam, qualification, licence, skill, roster ve time booking yapıları geniştir.
- Bu kapsam FOX Training'in ayrı bir uygulama olarak değil, kritik maintenance command'larına bağlı ortak bir eligibility hizmeti olarak tasarlanmasını destekler.

### Kalite ve emniyet

- Audit instance, non-conformance, action, root cause, occurrence, risk, safety type ve severity aileleri mevcuttur.
- Durum kayıtlarında iş kuralı SQL ifadeleri tutulabildiği görülür; bu esnektir fakat kural güvenliği, test ve sürüm yönetimi gerektirir.

### Entegrasyon ve raporlama

- `api`, `webapi`, `interfaces`, `systeminterfaces`, `cmro`, `ect`, `ewi`, `import` ve `nGenImport` şemaları entegrasyon geçmişine işaret eder.
- Data exchange event, export job, SSIS log, middleware ve import/export package tabloları vardır.
- Çok sayıda report/template/dashboard nesnesi özelleştirilebilir platform yaklaşımını destekler.

## Mimari değerlendirme

### Güçlü taraflar

- Çok geniş ve gerçek MRO edge-case'leriyle olgunlaşmış domain kapsamı.
- Standart audit kolonlarının yaklaşık 2.800 tabloda tekrarlanması sayesinde kayıt sahipliği ve optimistic/versioning benzeri desenler.
- Workflow, rol/sağ ve rapor konfigürasyonunun platform seviyesinde ele alınması.
- API ve import/export için ayrı şemaların bulunması.

### Borç ve risk sinyalleri

- 3.166 tabloya karşı yalnız 404 tanımlı FK ve 6 CHECK vardır. Çıkarım: bütünlük önemli ölçüde uygulama, trigger veya prosedürlere bağlı olabilir.
- 4.110 trigger ve 2.954 prosedür, davranışın keşfini ve bağımsız servis sınırlarına ayrılmasını zorlaştırabilir.
- `timestamp`, `ntext`, `image`, `money`, `smalldatetime` gibi legacy SQL Server tipleri mevcuttur.
- `Old`, `Backup`, tarih ekli ve numaralı en az 15 tablo görülür; şema hijyeni ve göç geçmişi riski taşır.
- 56.828 kolon için yalnız 15 açıklama vardır; veri sözlüğü uygulama ekibine bağımlı olabilir.
- `import` ve `nGenImport` kopyaları, canonical model ile staging model sınırlarının zaman içinde çoğaldığını düşündürür.
- Tablo başına tekrar eden `Closed`, `ReadOnly`, `RecordLocked`, `Version`, kullanıcı ve timestamp kolonları yeni modelde körlemesine taşınmamalıdır.

## Veri hacmi neden performans kanıtı değil

- 3.166 tablonun 2.515'i boştur.
- Teknik ve supply tablolarının çoğunda yalnız kod/konfigürasyon satırları vardır.
- En yüksek satır sayıları rol-component, veri sözlüğü, dil çevirisi, şehir ve workflow konfigürasyonundadır.

Bu nedenle “Veryon bu hacimde hızlı/yavaş” sonucu çıkarılamaz. Performans için gerçek transaction hacmi, sorgu planı, IO/wait ve kullanıcı concurrency ölçülmelidir.

## Güvenlik bulgusu

Paket içinde iki refresh token CSV'sinde toplam 311 token satırı bulunur. İnceleme tarihine göre expiry tarihleri geçmiş olsa da 307 kayıt `used=false` ve `invalidated=false` görünümündedir. Ayrıca 28 kullanıcı ve 3 password history satırında parola alanları doludur; isim/soyisim de mevcuttur.

Sonuç:

- Kaynak paket gizli kabul edilmelidir.
- Aktif sistemle bağ varsa token/parola rotasyonu ve erişim log incelemesi yapılmalıdır.
- Export üretim süreci allow-list ile yeniden tasarlanmalıdır.
- Bu depoya yalnız toplulaştırılmış metadata alınmıştır.

## FOX MRO için alınacak, alınmayacak ders

### Alınacak

- Demand → order → receipt → stock → issue/sale zincirinin uçtan uca korelasyonu
- Purchase/repair/exchange/loan/consignment için ortak fakat tiplenmiş ticari çekirdek
- Technical, supply, training, quality ve workflow bounded context'leri
- Rol bazlı iş kuyrukları ve mobil hangar/depo işlemleri
- Import/export ve API'nin sonradan eklenti değil ürün sınırı olması

### Alınmayacak

- Her tabloya aynı durum bayraklarını çoğaltma
- İş kuralını açıklamasız SQL metni veya trigger içinde saklama
- Ham şemayı microservice sınırı sanma
- Vendor tablosunu FOX canonical modeli yapma
- Kullanıcı/token/parola kayıtlarını analiz paketiyle taşıma
- Veryon'a ait tablo, field veya code-table değerlerini FOX şeması/seed verisi olarak kopyalama

FOX'ta kurallar policy-as-data şeklinde sürümlü, imzalı, testli ve açıklanabilir olmalıdır; kritik invariant'lar veritabanı constraint'i ve domain command doğrulamasıyla birlikte korunmalıdır. Referans sözlükleri yalnız lisanslı/kamu standardı ve kuruluşça onaylı prosedürlerden temiz oda yöntemiyle üretilmelidir.

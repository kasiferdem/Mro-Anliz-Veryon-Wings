# 01 — Kapsam, yöntem ve kanıt

## İncelenen girdiler

- `Veryon DB Report.zip`: SQL Server şema envanteri, kısıtlar, indeksler, kod nesnesi listesi, tablo satır sayıları, referans/kod tabloları ve sınırlı örnekler.
- `Fox-Store.zip`: parça tedarik, satış, depo, traceability, API ve veri modeli taslağı.
- `Fox Training.zip`: Part-145/66/147 training, competence, OJT, authorization ve eligibility taslağı.
- `wings-analiz.md`: 25 Temmuz 2026 tarihli, tek üretim ortamı ve gözlemci rolüyle sınırlı WINGS saha gözlemi.
- `veryon-analiz.md`: 31 Temmuz 2026 tarihli ikincil Veryon şema/CAMO analizi; sayısal iddiaları ana export'a karşı yeniden doğrulandı.
- Üreticilerin 1 Ağustos 2026 tarihinde erişilen resmî ürün sayfaları.

Kaynak ZIP'ler ve iki ham iç not bu depoya kopyalanmamıştır; hassas kimlikler çıkarılarak yalnız kanıt özeti ve kaynak hash'i saklanmıştır.

## Kanıt sınıfları

| Sınıf | Anlam | Kullanım |
|---|---|---|
| Doğrudan bulgu | CSV'den sayılan tablo/kolon/kısıt/nesne | Veryon şema ölçüleri |
| Şema sinyali | Tablo/kolon/nesne adından çıkan makul yorum | Modül ve kabiliyet haritası |
| İç saha gözlemi | Belirli ortam, rol ve tarihte doğrudan görülen ekran/iş akışı | WINGS project/work-package/work-order ve UX davranışı |
| Üretici iddiası | Resmî ürün sayfasında belirtilen kabiliyet | Rakip profilleri |
| Çıkarım | Birden fazla sinyalden türetilen değerlendirme | Risk, mimari ve puan |
| Öneri | FOX hedefleri için tasarım/karar | Yol haritası ve hedef mimari |

Çıkarımlar dokümanlarda açıkça belirtilir. Üretici iddiaları bağımsız performans kanıtı sayılmaz.

## Analiz yöntemi

1. ZIP içindeki altı ana CSV doğrudan arşivden okunur.
2. Tablo, kolon, veri tipi, şema, kısıt, indeks, kod nesnesi ve satır sayısı toplulaştırılır.
3. `dbo` tablo ön ekleri ürün alanlarına eşlenir: `a` ticari/finans, `l` personel/eğitim, `o` operasyon, `q` kalite/emniyet, `s` supply/MRO commercial, `t` teknik bakım, `u` platform, `w` workflow.
4. Kabiliyet kanıtı, tablo adlarında kontrollü anahtar kelime aramasıyla çıkarılır.
5. Hassas dosyalar yalnızca dosya adı, başlık ve satır sayısı düzeyinde incelenir; değerler dışarı yazılmaz.
6. İç gözlem iddiaları kapsam/tarih/rol sınırlamasıyla kaydedilir; operasyon kimlikleri ve altyapı adresleri çıkarılır.
7. İkincil analizdeki sayısal iddialar ana export üzerinde tanımlı ve tekrarlanabilir kurallarla yeniden hesaplanır.
8. Rakipler aynı kriter setiyle resmî/güncel web kaynakları ve açıkça etiketlenmiş iç gözlem kullanılarak profillenir.
9. FOX Store ve FOX Training hedefleri üzerinden ağırlıklı karar modeli uygulanır.

## Bilinen sınırlamalar

- Döküm stored procedure, trigger, function veya view tanımlarını içermez; yalnızca nesne adı/tipi ve tarihleri vardır.
- Uygulama kodu, ekranlar, API sözleşmeleri, execution plan, wait statistics ve canlı performans metrikleri yoktur.
- Satır sayıları ürün şablonu/konfigürasyon snapshot'ını gösterir; işlem hacmi, büyüme veya kullanıcı sayısını göstermez.
- Referans verisinin bazı satır tarihleri 2005'e kadar gider; bu tarihler tek başına bugünkü kod sürümünün yaşı değildir.
- Ürün fiyatları kamuya açık değildir. TCO ve uygulama kolaylığı puanları göreli, RFP öncesi tahmindir.
- WINGS gözlemi tek üretim ortamı, belirli kullanıcı rolü ve tek oturumla sınırlıdır; görmediği ekranların yokluğunu kanıtlamaz. Project/work-package yürütme güvenini artırır, API/güvenlik/release/performans kanıtı sağlamaz.
- Veryon ikincil notundaki “13.457 örtük ilişki” sayısı aynı tanımla yeniden üretilememiştir. Ana export'ta 9.217 kolon `_ID` ile biter; 14.026 kolon adında `_ID` geçer. İki metrik de gerçek ilişki sayısı değil, yalnız adlandırma sinyalidir.
- CORRIDOR aktif bir üründür; aynı zamanda CAMP Aviate, Temmuz 2026 itibarıyla CORRIDOR/Quantum/TotalFBO/FBO One'ın yeni nesil platformu olarak konumlandırılmıştır.

## Temiz oda ilkesi

Bu çalışma Veryon/Rusada'nın özel şemasını veya iş mantığını FOX'a kopyalamayı önermez. Tablo ve özel kod değerleri yalnızca ürün kapsamını ve entegrasyon ihtiyacını anlamak için kullanılır. FOX veri modeli ve seed sözlükleri lisanslı/kamu standardı, otorite gereksinimi ve kuruluşun onaylı prosedürlerinden bağımsız olarak tasarlanmalıdır.

## Tekrarlanabilirlik

`scripts/analyze_veryon_export.py`, ham arşivden aşağıdaki güvenli çıktıları üretir:

- `schema-summary.json`
- `module-summary.csv`
- `capability-evidence.csv`
- `security-inventory.csv`

Script kaynak kayıt değerlerini hiçbir dosyaya yazmaz.

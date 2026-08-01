# 03 — Ürün karşılaştırması

## Aynı pazar değil, örtüşen pazarlar

Beş ürün aynı işlevleri farklı hedeflerde paketler:

- Veryon Tracking+, TRAX ve Ramco airline/M&E/MRO düzeyinde geniş suite'tir.
- WINGS airline ve bakım kuruluşlarına tam çözüm iddiasındadır; Türkiye referans yoğunluğu ayırt edicidir.
- CORRIDOR service center, repair station, parts distribution ve business aviation ekseninde modülerdir; CAMP Aviate ise bunu daha geniş, cloud-native ERP yönüne taşır.

Bu yüzden “en iyi ürün” tek sayı değildir. Doğru soru, FOX'un hangi alanlarda ürün sahipliği istediği ve hangi alanlarda hazır çekirdeğe güveneceğidir.

## Özet fark matrisi

| Alan | Veryon Tracking+ | WINGS | TRAX eMRO | CORRIDOR / CAMP Aviate | Ramco Aviation |
|---|---|---|---|---|---|
| Hedef | Airline, MRO, CAMO, rotary, military | Airline, M&E, MRO | Büyük airline/MRO | Service center, repair station, parts/FBO; yeni Aviate daha geniş | Line/component/engine/heavy MRO, operator, OEM |
| M&E derinliği | Çok yüksek; CAMO şema ayrıntısı doğrulandı | Project/work-package/work-order derinliği iç gözlemde doğrulandı; detay work-card kanıtı eksik | Çok yüksek, 21 modül | Work order/service center güçlü; airline CAMO derinliği daha sınırlı olabilir | Çok yüksek; engine/component ve contracts güçlü |
| Inventory/ticari | Procure/sell, integrated inventory | Inventory/RFID/mobile; detay RFP ile | Geniş ERP süreçleri | Inventory, procurement, sales, rental, rotable, warranty | Integrated supply chain, commercials, finance |
| Training/qualification | Şemada derin iz; kamu sayfasında business support | Kamu kanıtı sınırlı | Quality ve role apps; ayrıntı doğrulanmalı | Training & Qualifications modülü açıkça listeli | Workforce/resource kapsamı; eligibility ayrıntısı doğrulanmalı |
| Mobil/paperless | Role-based mobile, paperless | Tablet, kiosk, mobile inventory | 14 role-based iOS/web app | CORRIDOR Go; Aviate persona apps | Mobile/paperless MRO |
| Entegrasyon | REST API + flat file | Entegrasyon ve özelleştirme hizmeti; API ayrıntısı yok | Web ERP/cloud; API sözleşmesi RFP ile | SDK/API, accounting/ILS/CAMP bağları | Suite entegrasyonu; API/data export sözleşmesi RFP ile |
| Deployment | Cloud-based; fiyat kullanıcı/uçak/modül + kurulum | Java/Ajax/Oracle web; resmî site “reasonable/rapid” iddiası | Cloud hosting ve browser | CORRIDOR cloud veya on-prem; Aviate cloud-native yön | Multi-tenant, desktop-mobile, geniş suite |
| Ana risk | Büyük şema/konfigürasyon ve vendor bağımlılığı | Legacy UX; API/security/release ve detay work-card doğrulaması | Uygulama ve veri göçü karmaşıklığı | CORRIDOR → CAMP Aviate ürün geçişi ve ticari yol haritası | Yüksek kapsam, maliyet ve değişim yönetimi |

## Veryon Tracking+

Resmî ürün sayfası fleet, MRO, inventory, flight operations ve business support olmak üzere beş alanı; paperless MRO, mobile interfaces, integrated inventory ve REST/flat-file entegrasyonunu belirtir. Ekteki şema bu genişliği teknik olarak destekleyen güçlü bir sinyaldir. Ek inceleme; task-card maliyet/W&B, publication/AD/AMOC, asset configuration, journey, forecast, MEL/defect ve QC durum alanlarıyla CAMO derinliğini daha somut doğrular.

FOX açısından artısı, mevcut veri yapısına yakınlık ve tam suite kapsamıdır. Eksisi, FOX'un farklılaşma katmanının vendor şeması içinde kaybolması ve veri/iş kuralı bağımlılığıdır.

## WINGS

ADT'nin resmî sayfası WINGS'i airlines ve maintenance organizations için web tabanlı J2EE/Java/Ajax/Oracle çözümü olarak tanımlar; tablet, teknisyen kiosk'u, RFID, dashboard ve KPI sunar. Müşteri listesi Türkiye'de airline, MRO, OEM ve savunma referansları açısından güçlüdür.

25 Temmuz 2026 tarihli tek ortam/rol saha gözlemi; project/work-package ana ekranında work order, approval, resources, status, log, KPI, training, off-day, document, checklist ve dashboard katmanlarını; routine/non-routine ve base/line/shop/component ayrımlarını; müşteri onayı ile iç manhour/material authorization ayrımını doğruladı. Facility timeline ve project-hours görünümü de planlama/yürütme olgunluğu sinyalidir. Bu kanıt yalnız gözlenen ortam için geçerlidir.

Aynı gözlem frame/JSP tabanlı MDI, F7/F8 sorgu davranışı ve çok katmanlı menü nedeniyle öğrenilebilirlik ve modern UX riskini gösterdi. Detaylı work-card imza/stamp akışı, API, güvenlik, release, SLA ve performans henüz doğrulanmadı. FOX açısından yerel referans ve olası uygulama maliyeti avantajdır; WINGS yine 60–90 günlük ücretli pilotla doğrulanmalıdır.

## TRAX eMRO

TRAX, eMRO'yu engineering, planning, production, inventory, quality, documentation, technical records ve finance'i birleştiren 21 modüllü web ERP olarak tanımlar. eMobility 14 role-based iOS/web uygulaması sunar.

FOX açısından en iyi benchmark'ı geniş süreç ve paperless execution kataloğudur. Ancak FOX'un ilk kapsamı parça/depo/training ise TRAX'ın tam suite'i gereğinden büyük uygulama programı yaratabilir.

## CORRIDOR / CAMP Aviate

CORRIDOR; work order, inventory, procurement, shipping/receiving, pricing, barcoding, accounting integration, invoicing, training/qualifications, planning, tool crib, sales, rental, rotable/core ve warranty modüllerini açıkça listeler. Cloud ve on-prem seçenekleri ile SDK/API sunar.

CAMP Aviate, 2026'da CORRIDOR, Quantum, TotalFBO ve FBO One'ın yeni nesli olarak duyurulmuştur; MRO, parts distribution, inventory/supply chain, accounting, persona apps ve AI çözümlerini cloud-native platformda birleştirmeyi hedefler.

FOX'un service center + parts + training profiline en yakın hazır ürün budur. Aynı nedenle ürün geçiş planı, legacy CORRIDOR müşterisinin Aviate hakkı, veri göçü ve fiyatlandırma sözleşmede net olmalıdır.

## Ramco Aviation

Ramco; line, component, engine, hangar/heavy maintenance ve OEM aftermarket için end-to-end çözüm; work scheduling, contract management, customer portal ve one-touch demand-to-procurement supply chain sunar. Aviation 6.0 multi-tenant, analytics, mobile/paperless ve integrated commercials vurgular.

FOX açısından en güçlü benchmark commercial contract, engine/component MRO ve finans bütünlüğüdür. Orta ölçekli ilk sürüm için kapsam ve uygulama karmaşıklığı ağır olabilir.

## FOX'un farklılaşma boşluğu

Üretici sayfaları genişliği anlatır; aşağıdaki ayrıntılar çoğunlukla açık kanıtlanmaz:

- Certificate/trace paketinin attachment değil sürümlü domain object olması
- Stok bakiyesinin append-only event ledger'dan yeniden üretilebilmesi
- Eligibility kararının eğitim, lisans, yetki, task/asset/site ve karar zamanı ile açıklanması
- AOG'nin kontrol bypass'ı değil ölçülen fast-lane olması
- Türkçe/İngilizce audit evidence bundle
- Policy sürümü ve karar snapshot'ının geçmiş kayıtta korunması

FOX ürün tezi bu boşluk üzerine kurulmalıdır.

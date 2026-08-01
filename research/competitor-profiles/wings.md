# WINGS — ürün profili

**Üretici:** Applied Database Technology (ADT)

**URL:** https://www.adbtech.com/products/

**Araştırma:** 2026-08-01 — resmî kaynak taraması + 2026-07-25 sınırlı iç saha gözlemi

## Konumlandırma

ADT, WINGS'i airlines ve aircraft maintenance organizations için complete M&E/MRO çözümü olarak tanımlar.

## Kamuya açık kapsam

- Web tabanlı J2EE / Java / Ajax / Oracle mimarisi
- User-defined dashboard ve KPI
- Teknisyen kiosk'ları, tablet ve WINGS Mobile
- Mobile inventory, workflow authorization, attendance ve labor collection
- RFID inventory ve tool tagging
- Configuration, data migration, training, integration, customization hizmetleri

## İç saha gözlemi

Tek üretim ortamı ve belirli gözlemci rolüyle sınırlı oturumda aşağıdakiler doğrudan görüldü:

- Project/work-package ekranında project, work orders, approvals, resources, status, logs, KPI, trainings, off-days, documents, checklists ve dashboards katmanları
- Routine/non-routine ile base/line/shop/component work-order ayrımları; paperless, invoice, approval, bump/overshoot ve requisition göstergeleri
- Customer approval ile iç manhour/material authorization ayrımı
- Manager, inspector, planner, buyer, stockroom ve certifying staff kaynak rolleri
- Facility timeline ve project-hours/KPI görünümleri
- Frame/JSP tabanlı MDI, F7/F8 sorgu deseni ve yoğun menü navigasyonu

Bu gözlem project/work-package yürütme kabiliyetine ilişkin kanıt güvenini düşükten ortaya taşır. Detay work-card imza/stamp, API, güvenlik, release cadence ve performans hakkında kanıt üretmez.

## Güçlü taraflar

- Türkiye'de airline, MRO, OEM ve savunma alanında geniş referans listesi.
- Vendor, uygun lisans ve hızlı/uygun maliyetli implementation iddiasında bulunur.
- Tablet/kiosk/RFID yaklaşımı hangar ve depo operasyonuna uygundur.
- Project/work-package, müşteri/iç onay ve kaynak yönetimi tek gözlemde operasyonel olarak görüldü.

## Zayıflık/risk

- Resmî web içeriği API sözleşmesi, güvenlik sertifikaları ve release cadence hakkında sınırlıdır.
- Gözlenen frame/JSP ve F7/F8 sorgu deseninin güncel browser, accessibility, öğrenilebilirlik ve modernizasyon yolu doğrulanmalıdır.
- İlan edilen J2EE/Ajax/Oracle stack'in güncel sürüm, mobile ve cloud işletim modeli doğrulanmalıdır.
- Maliyet ve hızlı uygulama üretici iddiasıdır; bağımsız teklif/pilot kanıtı yoktur.

## FOX için uygunluk

Yerel uygulama, Türk kullanıcı ekosistemi ve bütçe öncelikliyse kısa listede olmalıdır. Saha gözlemi bakım yürütme güvenini artırmıştır; yine de API/güvenlik, detailed work-card ve UX kabulü için ücretli sandbox/pilot olmadan birinci tercih yapılmamalıdır.

## RFP'de doğrulanacaklar

- Güncel product version, technology stack, cloud/on-prem seçenekleri
- REST API/OpenAPI, webhook/delta, mobile offline ve SSO
- Part trace/certificate/quarantine ve authorization gate davranışı
- Beş yıllık TCO ve upgrade/customization sorumluluğu
- Veri export, attachment ve exit assistance
- Project/work-package approval audit'i ile detailed work-card signature/stamp/independent inspection
- Frame/JSP/F7-F8 kullanıcı akışının modern arama, accessibility ve browser roadmap'i

## Raw data sources

`research/raw/wings/2026-08-01/scrapes/official-sources.md`

Gizliliği giderilmiş iç kanıt: `research/internal-observations/2026-07-25-wings-production-observation.md`

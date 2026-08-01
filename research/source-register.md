# Kaynak kayıt defteri

**Erişim tarihi:** 2026-08-01

| Ürün | Resmî kaynak | Bu raporda desteklediği iddia |
|---|---|---|
| Veryon Tracking+ | https://veryon.com/products/veryon-tracking-plus | Beş ürün alanı, cloud, paperless, mobile, API/flat file, fiyatlama şekli |
| WINGS | https://www.adbtech.com/products/ | Complete M&E/MRO, J2EE/Java/Ajax/Oracle, dashboard/KPI, tablet/kiosk/RFID |
| WINGS Mobile | https://www.adbtech.com/mobile/ | Mobile inventory, workflow authorization, attendance/labor |
| WINGS Customers | https://www.adbtech.com/customers/ | Türkiye ve global airline/MRO/OEM referans listesi |
| WINGS Services | https://www.adbtech.com/services/ | Configuration, migration, training, integration ve customization |
| TRAX | https://www.trax.aero/en/products/ | 21 modül, integrated ERP alanları, 14 role apps, cloud hosting |
| CORRIDOR | https://www.corridor.aero/software/ | Temel ve süreç modülleri, sales/rental/core/warranty/training |
| CORRIDOR Deployment | https://www.corridor.aero/software-deployment-options/ | Cloud ve on-prem seçenekleri |
| CORRIDOR Integration | https://www.corridor.aero/software-integrate-and-optimize/ | Accounting integrations ve SDK/API |
| CAMP Aviate | https://campaviate.aero/ | CORRIDOR/Quantum/TotalFBO/FBO One'ın yeni nesli; cloud ERP/persona/AI |
| Ramco MRO | https://www.ramco.com/products/aviation-software/maintenance-repair-and-overhaul/ | MRO türleri, scheduling, contracts, portal, integrated supply chain |
| Ramco Aviation | https://www.ramco.com/products/aviation-software/ | Aviation 6.0, multi-tenant, mobile/paperless, çözüm alanları |

## İç kanıt kayıtları

| Kanıt ID | Tarih | Sınıf | Bütünlük | Kullanım ve sınır |
|---|---|---|---|---|
| `INT-WINGS-2026-07-25` | 2026-07-25 | İç saha gözlemi | SHA-256 `4CF9A23E8FF67BD334425475C73DB807584EAF64C1F91DDA06B29196617D7F56` | Tek üretim ortamı/rol; project, work-package, approvals, resources, dashboard ve UX. API/güvenlik/performance kanıtı değil. |
| `INT-VERYON-2026-07-31` | 2026-07-31 | İkincil teknik analiz | SHA-256 `947320F411FCA06BD3D27C5D719CACA0E697E818DC9BAF67DD0633FF69458C4C` | CAMO tablo/kolon ve referans sayıları ana export'a karşı doğrulandı; 13.457 ilişki iddiası düzeltilmiştir. |

Ham iç kanıtlar hassas URL, altyapı ve operasyon kimlikleri nedeniyle depoya alınmamıştır. Gizliliği giderilmiş kayıtlar `research/internal-observations/` altındadır.

## Kaynak politikası

- Ürün kabiliyetleri resmî üretici sayfalarından alınmıştır.
- Üretici fayda ve maliyet iddiaları doğrulanmış tasarruf gibi kullanılmamıştır.
- Fiyatlar kamuya açık olmadığı için raporda tahmini lisans tutarı verilmemiştir.
- Veryon veritabanı sayıları kullanıcı tarafından sağlanan export'tan yeniden üretilmiştir; ham export gizlidir.
- İç gözlem, resmî ürün iddiası veya bağımsız performans testi yerine geçmez; tarih, ortam, rol ve görülmeyen kapsam açıkça taşınır.

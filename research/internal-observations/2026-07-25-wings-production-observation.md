# WINGS NG — anonimleştirilmiş canlı ekran gözlemi

**Evidence ID:** `INT-WINGS-2026-07-25`

**Kaynak tipi:** Kullanıcı tarafından sağlanan iç analiz; tek bir production oturumunda canlı gezinme

**Ham dosya:** Depoya alınmadı

**SHA-256:** `4CF9A23E8FF67BD334425475C73DB807584EAF64C1F91DDA06B29196617D7F56`

## Veri sınıflandırması

Ham not; iç sistem adresi, müşteri/project/work-order referansları, aircraft/tail bilgisi ve ekran alan envanteri içerir. Public GitHub için uygun değildir. Aşağıdaki özet operasyon kimlikleri çıkarılarak hazırlanmıştır.

## Gözlenen kabiliyetler

- JSP/frame tabanlı MDI kullanıcı deneyimi; Oracle Forms benzeri F7/F8 sorgu davranışı.
- Rol seçimine göre değişen Setup, Applications, Inquiries, Reports, Interface ve Inventory menüleri.
- Planning ve Project Planning alanlarında aircraft, project/work package, work order, work card, maintenance planning, parts/orders, attendance/labor, discrepancy, milestone ve dashboard ekranları.
- Project/work-package ekranında project, work order, approval, resource, status history, log, KPI, training, off-day, document, checklist ve dashboard bölümleri.
- Work-order tipinde routine/non-routine, line/base/shop/component, paperless, invoice, estimate approval, bump/overshoot ve requisition davranışını etkileyen flag'ler.
- Customer approval ile internal man-hour/material authorization'ın ayrılması.
- Manager, inspector, planner, buyer, stockroom, production crew ve certifying staff gibi kaynak kategorileri.
- SHY-145/EASA-145 referansları, RII/CRS belgeleri ve project/card document ağaçları.
- Facility timeline ve required/assigned/actual hours gibi planning/KPI görünümleri.

## FOX için çıkarım

WINGS'in bakım yürütme derinliği, resmî web sayfasından görüldüğünden daha yüksektir. FOX aşağıdaki desenleri korumalıdır:

- Project/work package → work order → work card/task hiyerarşisi
- Müşteri onayı ile iç release/authorization kararının ayrılması
- Resource category, capacity, target/revised/actual date ve status history
- Document/checklist/KPI'nin aynı operasyon korelasyonuna bağlanması

Kopyalanmaması gerekenler:

- F7/F8 sorgu ve frame/MDI gezinme
- Çok sayıda boolean flag ile davranış tanımlama
- Ekran/program kodunu domain kimliği yapma
- “Current” bayraklı geçmiş yerine geçiş invariant'ı olmayan status kaydı

## Kanıt sınırı

Bu gözlem tek environment ve sınırlı rollerle yapılmıştır. Work-card signature/stamp, parts/order, quality, security, API, performance ve mobile davranışı tam incelenmemiştir. Ürün puanını destekler fakat vendor demo/pilot yerine geçmez.

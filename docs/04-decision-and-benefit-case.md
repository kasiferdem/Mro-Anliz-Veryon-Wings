# 04 — Karar ve fayda modeli

## Ağırlıklı uygunluk modeli

Puanlar 1–5 arasındadır ve kamu kaynakları + FOX hedef kapsamı üzerinden verilmiştir. Canlı pilot olmadan satın alma kararı değildir.

| Kriter | Ağırlık |
|---|---:|
| Parça, tedarik, satış ve depo uyumu | %20 |
| M&E/CAMO/MRO yürütme derinliği | %15 |
| Training, competence ve authorization | %10 |
| Audit, traceability ve kontrol tasarımı | %15 |
| API, veri taşınabilirliği ve entegrasyon | %10 |
| Mobil/paperless kullanıcı deneyimi | %10 |
| Uygulama çevikliği ve TCO öngörülebilirliği | %10 |
| Türkiye/yerel operasyon uyumu | %5 |
| Stratejik kontrol ve farklılaşma | %5 |

## Sonuç

| Seçenek | Hedef uyum puanı / 100 | Bugünkü olgunluk | Ana risk |
|---|---:|---|---|
| FOX hibrit hedef mimarisi | **89** | Tasarım / düşük | Teslimat, ürün yönetimi ve compliance validation |
| CORRIDOR / CAMP Aviate | **82** | Ürün / yüksek | 2026 platform geçişi ve ticari roadmap |
| Ramco Aviation | **80** | Ürün / çok yüksek | Kapsam, maliyet ve değişim yönetimi |
| Veryon Tracking+ | **78** | Ürün / çok yüksek | Karmaşık veri modeli ve vendor bağımlılığı |
| TRAX eMRO | **78** | Ürün / çok yüksek | Enterprise uygulama büyüklüğü |
| WINGS | **71** | Ürün / yüksek; execution kanıt güveni orta, API/security düşük | Legacy UX ile API/security/roadmap ve detay work-card belirsizliği |

FOX puanı “bugün hazır ürün” puanı değil, doğru ürün sınırı uygulandığında beklenen stratejik uyumdur. Hazır ürünler teslimat riskinde belirgin biçimde öndedir.

## Tavsiye edilen karar

### Karar A — Ürün inşa et

FOX MRO'yu ilk teslimatta şu üç değer akışında sahiplenin:

1. `Demand → sourcing → order → receipt/inspection → stock → issue/sale`
2. `Person → training/competence → authorization → eligibility decision → sign-off`
3. `Requirement/policy → control → evidence → audit bundle`

Çekirdek kararlı hâle geldikten sonra dördüncü akış M7A olarak eklenebilir:

4. `Authoritative CAMO feed → normalized oversight → forecast/reconciliation → exception/evidence`

Technical records, AMP/MPD/AD/SB ve heavy maintenance execution başlangıçta hazır M&E sistemine bağlı kalsın. FOX'un bunlarda yetkili writer olması, M7B karar kapıları geçilmeden plan varsayımı yapılmamalıdır.

### Karar B — Hazır ürün gerekiyorsa

- Service center/parts/training profili: CORRIDOR/CAMP Aviate pilotu.
- Airline/CAMO dengesi: Veryon Tracking+.
- Büyük, paperless airline/MRO: TRAX.
- Engine/component/heavy MRO ve güçlü commercial/finance: Ramco.
- Türkiye'de maliyet ve yerel uygulama önceliği: WINGS; teknik pilot ve sözleşme korumaları şart.

## Fayda hipotezleri

Rakam uydurmak yerine pilot öncesi baseline ve pilot sonrası ölçüm kullanılır.

| Fayda | KPI | Hesap |
|---|---|---|
| AOG yanıt hızlanması | AOG demand-to-committed süre | `committed_at - demand_created_at` |
| Kabul çevrim süresi | Receipt-to-release p50/p95 | `released_at - received_at` |
| Trace hazırlık hızı | Audit bundle üretim süresi | `bundle_ready_at - request_at` |
| Stok doğruluğu | Cycle count accuracy | `1 - abs(system-physical)/physical` |
| Belge kalitesi | İlk kontrolde eksiksiz paket | `first_pass_complete / receipts` |
| Tedarik performansı | OTIF ve supplier defect rate | Tam/zamanında teslim ve ret oranı |
| Maliyet kontrolü | Landed cost variance | `actual_landed - approved_estimate` |
| Yetki güvenliği | Engellenen uygunsuz sign-off | Deny reason ve policy version ile sayım |
| Kullanıcı verimliliği | İşlem başına dokunuş/süre | Event ve UX telemetry |

## Beklenen nitel fayda

- FOX Store ve Training arasında çift kişi/organizasyon/rol yönetimi ortadan kalkar.
- Bir part/stock item için satın alma, sertifika, sahiplik, konum, issue/install ve yetkili kişi kanıtı tek korelasyonda görünür.
- Satıcı değiştirme veya çoklu M&E bağlantısında canonical FOX model korunur.
- Compliance kontrolleri ekran uyarısından API düzeyinde deny/allow kararına dönüşür.
- Rapor hazırlama yerine audit bundle üretimi otomatikleşir.

## Toplam sahip olma maliyetini ölçme

Tekliflerde en az aşağıdaki beş yıllık kalemler aynı formatta istenmelidir:

- Kullanıcı, aircraft, module, site ve environment lisansları
- Implementation, configuration, migration, report ve integration hizmeti
- Training, sandbox, test ve go-live desteği
- API çağrısı, storage, e-signature, mobile ve analytics ek ücretleri
- Upgrade, custom code uyarlama, support tier ve çıkış/export maliyeti
- İç ürün ekibi, operasyonel değişim ve veri temizliği maliyeti

## Karar kapıları

Hibrit çekirdek ancak aşağıdaki koşullarda devam etmelidir:

- Ürün sahibi ve domain leads atanmışsa
- Compliance owner invariant ve kanıt modelini onaylıyorsa
- En az 12 aylık çekirdek ekip bütçesi varsa
- M&E entegrasyonuna sandbox/API erişimi varsa
- Bir depo ve part class için pilot veri temizlenebiliyorsa

Bu koşullar yoksa hazır ürün pilotuna dönmek daha yüksek net fayda verir.

M7A/M7B için ek kapılar; authoritative kaynak sahipliğinin yazılı olması, counter/forecast ve applicability mutabakatının deterministik çalışması, paralel işletimde açıklanamayan kritik fark kalmaması, veri kalitesi eşiği, bağımsız compliance validation ve gerekiyorsa otorite/MOE onayıdır.

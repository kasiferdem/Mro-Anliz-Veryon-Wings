# Veryon Tracking+ — ürün profili

**Üretici:** Veryon

**URL:** https://veryon.com/products/veryon-tracking-plus

**Araştırma:** 2026-08-01 — resmî kaynak + sağlanan DB şeması

## Konumlandırma

Veryon Tracking+, eski adıyla Rusada ENVISION; commercial airline, MRO, complex helicopter ve military/government operasyonları için cloud-based aviation M&E çözümüdür.

## Kapsam

- Fleet management ve airworthiness planning
- Base/component MRO planning ve execution
- Inventory planning, aircraft part procurement ve sales
- Flight/crew operations
- HR, finance, risk, quality ve safety business support
- Paperless MRO, role-based interfaces, mobile ve analytics
- REST API ve karmaşık ihtiyaçlar için flat-file exchange

## Sağlanan şemayla doğrulanan sinyaller

- Teknik bakım, supply, personel/eğitim, kalite/emniyet, flight ops ve finance için geniş tablo aileleri.
- Purchase/repair/exchange/loan, receipt/discrepancy, stock/demand, warranty ve workflow yapıları.
- API/webapi/import/interface katmanları.
- Yoğun SQL trigger/procedure ve platform konfigürasyonu.
- `tCard` üzerinde maliyet, weight/balance, publication/manual, AD ve AMOC; `tAsset` üzerinde configuration/certificate/software; `tRegJourney` ve forecast senaryolarında CAMO gözetim sinyalleri.
- Kontrollü life/task, compliance, MEL, defect, removal, asset/card/order-task status ve forecast reference tabloları.

İkincil analizde verilen “13.457 örtük ilişki” sayısı yeniden üretilememiştir. Ana export'ta 9.217 kolon `_ID` ile biter, 14.026 kolon adında `_ID` içerir; bunlar gerçek ilişki sayısı değil yalnız adlandırma sinyalidir. Tanımlı foreign key sayısı 404'tür.

## Güçlü taraflar

- İş alanlarının aynı suite içinde gerçek zamanlı bağlantısı.
- Fixed/rotary ve standalone MRO/CAMO profiline uyum.
- Mevcut Veryon verisi için en düşük semantik göç mesafesi.

## Zayıflık/risk

- Şema genişliği ve davranışın SQL katmanında yoğun olması entegrasyon/göç bağımlılığı yaratabilir.
- Kamu kaynakları ayrıntılı certificate validation, event immutability ve segregation-of-duties davranışını kanıtlamaz.
- Fiyat kullanıcı/uçak/modül ve one-time implementation fee'ye göre teklif edilir; TCO RFP gerektirir.

## FOX için uygunluk

FOX airline/CAMO ve MRO kapsamını tek pakette satın alacaksa güçlü adaydır. FOX'un kendi Store/Training ürün tezini koruyacağı modelde API üzerinden technical master ve work execution sistemi olarak konumlandırılmalı; FOX önce M7A read-mostly CAMO oversight ile bağlanmalıdır.

## RFP'de doğrulanacaklar

- API coverage, event/delta feed, idempotency ve bulk export
- Certificate package, quarantine/release ve serial duplicate kontrolleri
- Training/qualification ile task assignment/sign-off gate
- Custom report/workflow upgrade maliyeti
- Tam exit export ve attachment/hash erişimi

## Raw data sources

`research/raw/veryon-tracking-plus/2026-08-01/scrapes/official-sources.md`

Gizliliği giderilmiş ikincil kanıt: `research/internal-observations/2026-07-31-veryon-secondary-analysis.md`

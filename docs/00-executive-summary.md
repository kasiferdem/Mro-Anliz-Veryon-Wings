# 00 — Yönetici özeti

## Öneri

FOX MRO için önerilen yön **hibrit ürün stratejisidir**:

1. FOX'un sahip olacağı çekirdek: parça ve effectivity, tedarik, satış, depo, certificate/trace paketi, değiştirilemez envanter olayları, training/competence/authorization ve açıklanabilir uygunluk kararları.
2. İlk aşamada satın alınacak veya entegre edilecek çekirdek: CAMO, AMP/MPD/AD/SB yönetimi, teknik kayıt, güvenilirlik ve derin hangar/component work execution. FOX, M7A'da bunların read-mostly gözetim ve mutabakat katmanını kurabilir.
3. Yetki ilkesi: FOX'un CAMO'da yazarlık üstlenmesi ancak paralel işletim, deterministik forecast/mutabakat, veri kalitesi, otorite ve MOE onayı kapıları geçilirse M7B olarak değerlendirilir.
4. Entegrasyon ilkesi: bakım talebi ve work package ile FOX demand/stock/eligibility kayıtları aynı `correlation_id` altında bağlanır; her alan için tek bir system-of-record belirlenir.

Bu seçim, Veryon'daki kapsamı öğrenme kaynağı olarak kullanır fakat 3.166 tablolu yapıyı kopyalamaz. FOX'un farkı ekran sayısı değil; **kanıtı eksik işlemi teknik olarak engelleyen, Türkçe/İngilizce, denetlenebilir ve entegrasyon-dostu bir çekirdek** olmalıdır.

## Neden

- Attached Veryon şeması, tam M&E/MRO ürününün onlarca yıllık kapsam ve edge-case biriktirdiğini gösteriyor. Aynısını sıfırdan yapmak yüksek takvim, uygunluk ve veri göçü riski taşır.
- Mevcut FOX Store taslağı; tedarik, satış, depo ve traceability için doğru ürün sınırını kurmuş durumda.
- FOX Training taslağı; lisans, eğitim, yetkinlik, OJT ve yetkilendirmeyi kritik bakım komutlarına bağlayarak pazarda anlamlı bir farklılaşma alanı yaratıyor.
- Veryon dökümündeki yoğun trigger/procedure yapısı ve düşük declarative constraint görünürlüğü, yeni üründe kuralların daha görünür, test edilebilir ve sürümlü olmasının değerini gösteriyor.
- Ek Veryon analizi `tCard`, `tAsset`, `tRegJourney` ve forecast/reference tablolarında maliyet, W&B, yayın/AD/AMOC, asset configuration, journey ve planlama ayrıntılarını doğruladı; bu kapsam M7A CAMO gözetim tasarımını somutlaştırdı.
- Tek üretim ortamındaki WINGS saha gözlemi; project/work package, work order, müşteri onayı, kaynak, KPI ve doküman katmanlarının operasyonel derinliğini doğruladı. Aynı gözlem frame/JSP tabanlı MDI ve F7/F8 sorgu desenleri nedeniyle modern kullanıcı deneyimini FOX için ayrı bir avantaj alanı yaptı.

## Veryon dökümünden çıkan sayısal fotoğraf

| Ölçü | Sonuç | Yorum |
|---|---:|---|
| Tablo | 3.166 | Çok geniş fonksiyon alanı |
| Kolon | 56.828 | Tablo başına ortalama yaklaşık 18 kolon |
| PK / FK / UQ / CHECK | 3.091 / 404 / 19 / 6 | İlişki ve iş kuralı önemli ölçüde DB dışı veya kod nesnelerinde olabilir |
| İndeks | 4.662 | 3.600 unique, 1.062 non-unique |
| Trigger / prosedür / view | 4.110 / 2.954 / 2.348 | Davranışın SQL katmanında yoğun olduğu güçlü sinyali |
| Extended description | 15 | Şema sözlüğü için yetersiz |
| Toplam satır | 564.223 | Canlı operasyon hacmi olarak yorumlanamaz |
| Boş tablo | 2.515 (%79,4) | Snapshot büyük ölçüde ürün şablonu/konfigürasyonu |
| Hassas export | Token, parola, personel/PII | Kaynak paket GitHub'a uygun değil |

## Ürünlere göre en doğru kullanım

| İhtiyaç | En güçlü kısa liste |
|---|---|
| FOX'un stratejik ve farklılaşmış ürününü kurmak | FOX hibrit hedef mimarisi |
| Orta ölçekli service center + parça ticareti, hızlı modüler başlangıç | CORRIDOR / CAMP Aviate |
| Airline/CAMO + MRO + flight ops + business support dengesi | Veryon Tracking+ |
| Büyük airline/MRO, çok geniş paperless süreç kataloğu | TRAX eMRO |
| Engine/component/heavy MRO + commercial + finance bütünlüğü | Ramco Aviation |
| Türkiye referansları ve maliyet odaklı kısa liste | WINGS; bakım yürütme güveni saha gözlemiyle arttı, API/güvenlik ve detaylı work-card kanıtı hâlâ pilot gerektirir |

## Yönetim kararı

### Birincil yol

FOX Store ve FOX Training'i ortak platform altında birleştirin; kontrollü depo → tedarik/satış → training/authorization gate → bakım entegrasyonu sırasını izleyin. Çekirdekten sonra M7A CAMO gözetimini ayrı bir karar ve teslimat dalgası olarak ele alın; M7B yetkili CAMO geçişini otomatik kapsam genişlemesi saymayın.

### Satın alma alternatifi

Altı aydan kısa sürede hazır operasyon gerekiyorsa CORRIDOR/CAMP Aviate ile pilot yapın. Ancak CAMP Aviate'ın Temmuz 2026'da CORRIDOR ve diğer CAMP ERP ürünlerinin yeni nesli olarak duyurulması nedeniyle ürün yaşam döngüsü, göç hakkı, veri taşınabilirliği ve fiyat korumasını sözleşmede doğrulayın.

### Tam suite alternatifi

FOX'un kapsamı airline-scale CAMO ve teknik kayıtlara genişleyecekse Veryon, TRAX ve Ramco için senaryo bazlı RFP yürütün. Bu durumda “özellik var mı?” yerine gerçek iş verisiyle 20 çekirdek ve 5 CAMO uçtan uca senaryosunu çalıştırın.

## İlk 30 gün

1. Kaynak ZIP için güvenlik olayı/erişim incelemesi ve credential rotation kararı.
2. FOX Store ile FOX Training veri ve kimlik modellerini tek platform sözlüğünde birleştirme.
3. Bakım/CAMO system-of-record seçimi; M7A gözetim ile M7B yetkili yazarlık sınırının onayı.
4. Bir depo, bir part class ve sınırlı kullanıcı grubu için pilot veri seti.
5. RFP puan kartındaki 20 çekirdek + 5 CAMO senaryosu için satıcı demo planı.

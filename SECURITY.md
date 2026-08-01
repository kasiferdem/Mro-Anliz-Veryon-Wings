# Güvenlik ve veri sınıflandırması

## Kritik bulgu

İncelenen kaynak pakette aşağıdaki hassas veri sınıfları görülmüştür:

- `api.AuthRefreshTokens.csv` ve `webapi.AuthRefreshTokens.csv`: token alanları
- `dbo.uRALUser.csv`: parola, parola salt'ı, kişi adı/soyadı ve kullanıcı alanları
- `dbo.lPasswordHistory.csv`: geçmiş parola ve salt alanları
- Personel, iletişim, kimlik/lisans ve banka alanları içeren şemalar

İnceleme tarihinde refresh token son kullanımları geçmiş görünse de bu, paketi yayımlanabilir yapmaz. Parola değerlerinin algoritması ve tekrar kullanılabilirliği bu dökümden doğrulanamamıştır.

Kullanıcı tarafından sağlanan ek notlar da ham hâlleriyle yayımlanabilir değildir:

- `wings-analiz.md`: iç sistem URL'si ile aircraft/customer/project/work-order gibi operasyon kimlikleri içerir.
- `veryon-analiz.md`: veritabanı sunucu/instance bilgileri ve yerel dosya yolları içerir.

Bu iki dosya depoya kopyalanmamıştır. Yalnız gizliliği giderilmiş bulgu özeti, kanıt kapsamı ve bütünlük doğrulaması için SHA-256 değeri `research/internal-observations/` altında tutulur.

## Zorunlu işlem

1. Kaynak ZIP'i ve açılmış kopyaları `CONFIDENTIAL / RESTRICTED` sınıfında tutun.
2. Kaynak dosyayı GitHub'a, issue'ya, CI artifact'ına veya sohbet bağlantısına yüklemeyin.
3. Kaynak sistem hâlâ aktifse ilgili token ve parolaları döndürün; uygulama loglarında kullanım araştırması yapın.
4. Paylaşılmış kopyaları erişim kayıtlarıyla bulun ve kaldırma/retention işlemi uygulayın.
5. Gelecek export aracında kimlik doğrulama, kullanıcı, parola geçmişi ve PII tablolarını varsayılan olarak dışlayın.
6. Güvenli export için allow-list kullanın; deny-list tek başına yeterli değildir.

## Depodaki veri politikası

- `data/generated/` yalnızca sayı, şema adı, tablo adı ve kolon başlığı gibi toplulaştırılmış metadata içerir.
- Satır değerleri, tokenlar, hash/salt değerleri ve kişisel veriler hiçbir çıktıya yazılmaz.
- Güvenlik envanteri yalnızca dosya adı, satır sayısı, hassas alan adları ve risk sınıfı içerir.
- Ham iç gözlem notları, ekran görüntüleri, URL'ler, sunucu adları ve operasyon kimlikleri depoya alınmaz.
- Kaynak ZIP'in checksum'u kamu deposuna zorunlu değildir; iç zincirleme kayıt gerekiyorsa özel kayıt sisteminde tutulmalıdır. İç gözlem özetlerinde hash yalnız doğru kaynak revizyonunu tanımlamak için kullanılabilir.

## Açık bildirim

Bu depoya yanlışlıkla hassas veri commit edilirse normal bir commit ile silmek yeterli değildir. Erişimi durdurun, sırları döndürün, depo geçmişini yetkili ekipçe temizleyin ve olay kaydı açın.

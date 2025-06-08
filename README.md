KagoAI: Senin Akıllı Asistanın! 
Selamlar! Bu repo, KagoAI projemin kaynak kodlarını içeriyor. KagoAI, Python ile geliştirilmiş ve gelişmiş yapay zeka yetenekleriyle senin için harikalar yaratacak, akıllıca yanıtlar üretecek bir asistan!

Özellikler
Gelişmiş Doğal Dil Anlayışı: İnsan dilini derinlemesine anlayarak karmaşık sorulara bile mantıklı ve akıcı yanıtlar üretebilir.
Akıcı ve Yaratıcı Metin Üretimi: Farklı konularda, çeşitli tarzlarda özgün ve yaratıcı metinler oluşturma yeteneği.
Bilgi İşleme ve Özetleme: Uzun metinleri hızlıca analiz edip anahtar bilgileri çıkarabilir ve anlaşılır özetler sunar.
Kapsamlı Soru Cevaplama: Geniş bir bilgi yelpazesinden yararlanarak, en zorlu sorulara bile isabetli ve bilgilendirici cevaplar sağlar.
Programlama Desteği: Kod yazma süreçlerinde yardımcı olabilir, kod parçacıkları önerebilir veya teknik konularda bilgi sağlayabilir.

Kurulum
Bu projeyi kendi bilgisayarında çalıştırmak mı istiyorsun? Süper! İşte adım adım nasıl yapacağını anlatıyorum:

1. Repoyu Klonla
İlk olarak bu repoyu bilgisayarına klonla:
(Bilgisayarında Git kurulu olmalı. Eğer yoksa, git-scm.com/downloads adresinden kurabilirsin.)
git clone https://github.com/KaganKuzu/KagoAI.git
cd KagoAI

2. Sanal Ortam Oluştur (Şiddetle Tavsiye Edilir!)
Projenin bağımlılıklarını izole etmek için bir sanal ortam oluşturman projenin temiz kalmasını sağlar:

Terminali aç.
cd C:\Users\kagan\Contacts\Desktop\KagoAI - Türk Yapay Zekası (klasörün olduğu yolu) yazarak KagoAI klasörüne git.
Sonra python -m venv .venv yaz.
Ve hemen ardından, terminal hala o klasördeyken, .venv\Scripts\activate yaz ve Enter'a bas.

macOS/Linux için:
source .venv/bin/activate

3. Bağımlılıkları Yükle
Projenin çalışması için gerekli tüm kütüphaneleri requirements.txt dosyasından yükleyebilirsin:
terminale:
pip install -r requirements.txt

4. Ortam Değişkenlerini Ayarla (Çok Önemli!)
Bu proje, harici servislerle iletişim kurmak için bir API anahtarı kullanır. Güvenliğin için bu anahtarı bir .env dosyası içinde saklaman gerekiyor.

Projenin ana dizininde .env adında bir dosya oluştur.
https://platform.openai.com/settings/organization/api-keys adresine git, kayıt ol veya giriş yap,
Create New Secret Key'e tıkla, permissions kısmını all yap ve api keyi aşağıdaki gibi yapıştır;

.env dosyasının içine sadece şu satırı ekle (kendi API anahtarınla değiştirerek):
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

DİKKAT: .env dosyası GitHub'a yüklenmez! Hassas bilgilerinin güvende kalması için Git tarafından otomatik olarak göz ardı edilir. Bu yüzden, projeyi klonlayan herkesin kendi .env dosyasını oluşturması gerekir.

Projeyi Çalıştırma
Tüm kurulumları tamamladıktan sonra KagoAI'yi çalıştırmak çok kolay:

python KagoAI.py

Katkıda Bulunma
Projeyi geliştirmeye katkıda bulunmak ister misin? Harika olur! Her türlü katkıya açığım. Pull request'lerini bekliyorum!

Lisans
Bu proje, Apache Lisansı 2.0 (Apache License 2.0) altında yayımlanmıştır.
Daha fazla bilgi için lütfen LICENSE dosyasını inceleyiniz.

Made with ❤️ by KaganKuzu



**KagoAI: Senin Akıllı Asistanın! 🧠**

Selamlar! Bu repo, KagoAI projemin kaynak kodlarını içeriyor. KagoAI, Python ile geliştirilmiş ve gelişmiş yapay zeka yetenekleriyle senin için harikalar yaratacak, akıllıca yanıtlar üretecek bir asistan!

**Özellikler 🚀**

Gelişmiş Doğal Dil Anlayışı: İnsan dilini derinlemesine anlayarak karmaşık sorulara bile mantıklı ve akıcı yanıtlar üretebilir.
Akıcı ve Yaratıcı Metin Üretimi: Farklı konularda, çeşitli tarzlarda özgün ve yaratıcı metinler oluşturma yeteneği.
Bilgi İşleme ve Özetleme: Uzun metinleri hızlıca analiz edip anahtar bilgileri çıkarabilir ve anlaşılır özetler sunar.
Kapsamlı Soru Cevaplama: Geniş bir bilgi yelpazesinden yararlanarak, en zorlu sorulara bile isabetli ve bilgilendirici cevaplar sağlar.
Programlama Desteği: Kod yazma süreçlerinde yardımcı olabilir, kod parçacıkları önerebilir veya teknik konularda bilgi sağlayabilir.

**Kurulum 💻**

Bu projeyi kendi bilgisayarında çalıştırmak mı istiyorsun? Süper! İşte adım adım nasıl yapacağını anlatıyorum:

**1. Repoyu Klonla**

İlk olarak bu repoyu bilgisayarına klonla. (Bilgisayarında Git kurulu olmalı. Eğer yoksa, git-scm.com/downloads adresinden kurabilirsin.)

*Terminale yaz:* git clone https://github.com/KaganKuzu/KagoAI.git

*Terminale yaz:* cd KagoAI

**2. Sanal Ortam Oluştur (Şiddetle Tavsiye Edilir!) 🌳**

Projenin bağımlılıklarını izole etmek ve temiz kalmasını sağlamak için bir sanal ortam oluşturalım:

Terminali aç.

*Terminale yaz:* cd C:\Users\kagan\Contacts\Desktop\KagoAI - Türk Yapay Zekası
(Bu yol, senin proje klasörünün olduğu yer olmalı.)

Sanal ortamı oluştur:


*Terminale yaz:* python -m venv .venv

Sanal ortamı aktifleştir:

Windows için:

*Terminale yaz:* .venv\Scripts\activate

macOS/Linux için:
source .venv/bin/activate

**3. Bağımlılıkları Yükle 📦**
Projenin çalışması için gerekli tüm kütüphaneleri requirements.txt dosyasından yükleyebilirsin:

*Terminale yaz:* pip install -r requirements.txt

**4. Ortam Değişkenlerini Ayarla (Çok Önemli!) 🔑**

Bu proje, harici servislerle iletişim kurmak için bir API anahtarı kullanır. Güvenliğin için bu anahtarı projenin ana dizininde .env adında bir dosya içinde saklaman gerekiyor.

Projenin ana dizininde **.env** adında yeni bir dosya oluştur.

*platform.openai.com/settings/organization/api-keys* adresine git, kayıt ol veya giriş yap, Create New Secret Key'e tıkla, permissions kısmını all yap ve API key'i aşağıdaki gibi .env dosyasının içine yapıştır:

Kod snippet'i;

OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
(Bu satırı kendi API anahtarınla değiştirerek env dosyasına ekle.)

**DİKKAT: .env dosyası GitHub'a yüklenmez! Hassas bilgilerinin güvende kalması için Git tarafından otomatik olarak göz ardı edilir. Bu yüzden, projeyi klonlayan herkesin kendi .env dosyasını oluşturması gerekir.**

**Projeyi Çalıştırma ▶️**

Tüm kurulumları tamamladıktan sonra KagoAI'yi çalıştırmak çok kolay:

*Terminal'e*

**python KagoAI.py**
                 yaz yeter.

**Katkıda Bulunma 🤝**

Projeyi geliştirmeye katkıda bulunmak ister misin? Harika olur! Her türlü katkıya açığım. Pull request'lerini bekliyorum!

**Lisans 📜**

Bu proje, Apache Lisansı 2.0 (Apache License 2.0) altında yayımlanmıştır. Daha fazla bilgi için lütfen LICENSE dosyasını inceleyiniz.

Made with ❤️ by KaganKuzu

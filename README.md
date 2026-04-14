# Instagram Follower Analyzer

Bir Instagram hesabının takipçi listesini ve takip edilen listesini alan, bunları karşılaştırarak kimler tarafından tek taraflı takip edilenliğini, karşılıklı takip ilişkilerini ve detaylı istatistikleri gösteren bir Python CLI aracı.

## Özellikler

✨ **Temel Özellikler:**
- Instagram hesabına güvenli giriş ve oturum yönetimi
- Takipçi listesi indirme
- Takip edilen listesi indirme
- Verinin otomatik olarak cache'lenmesi

📊 **Analiz Özellikleri:**
- **Tek taraflı takipçiler**: Sizi takip eden ama siz takip etmeyen kişiler
- **Takip ettiğiniz ama takip etmeyen**: Siz takip ettiğiniz ama sizi takip etmeyen kişiler
- **Karşılıklı takipleşmeler**: Birbirinizi takip eden kişiler
- **Detaylı istatistikler**: Engagement oranı, takip geri dönüş oranı vb.
- **Filtre ve arama**: Kullanıcıları username veya isim ile arayabilme
- **JSON'a aktarım**: Tüm analiz sonuçlarını dışa aktarma

🔒 **Güvenlik:**
- Kimlik bilgileri .env dosyasında saklanır
- Oturum dosyaları yerel olarak cache'lenir
- Şifre terminal ekranında gösterilmez

## Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Adımlar

1. Depoyu klonlayın:
```bash
cd dijinst
```

2. Virtual environment oluşturun (opsiyonel ama önerilen):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# veya
source venv/bin/activate  # Linux/Mac
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env.example` dosyasını `.env` olarak kopyalayın ve Instagram kimlik bilgilerinizi girin:
```bash
cp .env.example .env
```

5. `.env` dosyasını düzenleyin:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

## Kullanım

### 1. İlk Giriş (Tercihen)
```bash
python cli.py login
```
Bu komutu kullanarak bir kez oturum açın ve oturumu kaydedin. Sonraki çalıştırmalarda yeniden giriş yapmanız gerekmeyecek.

### 2. Verileri İndirin
```bash
python cli.py fetch
```
Instagram'dan takipçi ve takip edilen listelerini indirin. Bu işlem hesap boyutuna bağlı olarak biraz zaman alabilir.

### 3. Analiz Sonuçlarını Görüntüleyin

**Sizi tek taraflı takip edenler:**
```bash
python cli.py unfollowers
```
Sizi takip eden ama siz takip etmeyen kişileri gösterir.

Seçenekler:
```bash
python cli.py unfollowers --limit 50          # İlk 50 sonuç
python cli.py unfollowers --filter "john"     # "john" ile ara
```

**Siz takip ettiğiniz ama takip etmeyen:**
```bash
python cli.py notfollowingback
```
Siz takip ettiğiniz ama sizi takip etmeyen kişileri gösterir.

**Karşılıklı takipleşmeler:**
```bash
python cli.py mutual
```
Birbirinizi takip eden kişileri gösterir.

**İstatistikler:**
```bash
python cli.py stats
```
Takipçi ilişkilerinizin detaylı istatistiklerini gösterir:
- Toplam takipçi sayısı
- Toplam takip sayısı
- Karşılıklı takip sayısı
- Tek yönlü takip sayıları
- Engagement oranı
- Doğrulanmış takipçi sayısı
- Özel hesap takipçi sayısı

**Analiz Sonuçlarını Dışa Aktarın:**
```bash
python cli.py export
```
Tüm analiz sonuçlarını JSON dosyası olarak kaydeder.

## Komut Özeti

```
python cli.py login              # Instagram'a giriş yap
python cli.py fetch              # Takipçi ve takip verisini indir
python cli.py unfollowers        # Tek yönlü takipçiler
python cli.py notfollowingback   # Takip ettiğiniz ama takip etmeyen
python cli.py mutual             # Karşılıklı takipçiler
python cli.py stats              # Detaylı istatistikler
python cli.py export             # Sonuçları JSON'a aktarma
python cli.py --help             # Tüm komutları göster
```

## Çıktı Formatı

### Tablo Formatı Örneği
```
┌──────────────────┬──────────────────┬──────────┬─────────┐
│ Username         │ Full Name        │ Verified │ Private │
├──────────────────┼──────────────────┼──────────┼─────────┤
│ john_doe         │ John Doe         │          │         │
│ jane_smith       │ Jane Smith       │ ✓        │ 🔒      │
└──────────────────┴──────────────────┴──────────┴─────────┘
```

### İstatistik Formatı Örneği
```
📊 Follower Statistics

┌──────────────────────┬─────────┐
│ Metric               │ Value   │
├──────────────────────┼─────────┤
│ Total Followers      │ 1250    │
│ Total Following      │ 890     │
│ Mutual Follows       │ 750     │
│ One-Way Followers    │ 500     │
│ One-Way Following    │ 140     │
│ Engagement Ratio     │ 60.00%  │
│ Follow-Back Ratio    │ 84.27%  │
└──────────────────────┴─────────┘
```

## Dosya Yapısı

```
dijinst/
├── cli.py                    # Ana CLI arayüzü
├── config.py                 # Konfigürasyon yönetimi
├── instagram_api.py          # Instagram API istemcisi
├── follower_analyzer.py      # Analiz mantığı
├── requirements.txt          # Python bağımlılıkları
├── .env.example              # Ortam değişkenleri şablonu
├── .env                      # Gerçek ortam değişkenleri (git ignore'lanmış)
├── cache/                    # Takipçi verisi ve session cache'i
└── README.md                 # Bu dosya
```

## Dikkat Edilecek Noktalar

⚠️ **Önemli:**

1. **Instagram Şartları**: Bu aracı Instagram'ın kullanıcı anlaşmasına uygun şekilde kullanın. Otomatik erişim Instagram tarafından kontrol edilebilir.

2. **Oturum Güvenliği**: Oturum dosyaları `.cache/` dizininde saklanır. Bu dosyaları asla paylaşmayın.

3. **Büyük Hesaplar**: Çok fazla takipçisi/takip ettiği olan hesaplarda işlem biraz zaman alabilir.

4. **Oran Sınırlaması**: İnstagram API'ının oran sınırlamaları olabilir. Birden fazla çalışma yaparsanız aralar verin.

5. **Veri Gizliliği**: Dışa aktarılan JSON dosyaları kişi verisi içerir. Bunu güvenli bir şekilde saklayın.

## Sorun Giderme

### "No saved session found"
```bash
python cli.py login
```
Komutu çalıştırarak yeniden oturum açın.

### "Login failed"
- Kimlik bilgilerinizin doğru olduğundan emin olun
- İki faktörlü kimlik doğrulama etkinse, bir uygulama şifresi kullanmanız gerekebilir
- Kendi hesabınızda iki adımlı doğrulama kullanıyorsanız devre dışı bırakın (veya uygulamaya özgü şifre oluşturun)

### "Rate limit exceeded"
Bu, Instagram'ın oran sınırlamalarına ulaştığınız anlamına gelir. Bir süre bekleyip tekrar deneyin.

## Güvenlik Notları

- Asla `.env` dosyasını git'e commit etmeyin (zaten `.gitignore`'da)
- Instagram şifrenizi başkasıyla paylaşmayın
- Bu aracı yalnızca kendi hesabınız için kullanın
- İnstagram'ın hizmet şartlarına ve gizlilik politikasına uyun

## Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.

## Yardım

Sorunlarla karşılaşırsanız:

1. `python cli.py --help` komutunu çalıştırarak yardım alın
2. `.env` dosyanızın doğru yapılandırıldığını kontrol edin
3. Python sürümünüzün 3.8+ olduğundan emin olun
4. Tüm bağımlılıkların yüklendiğini doğrulayın: `pip install -r requirements.txt`

## Katkılar

Hata bildirme, öneriler ve katkılar hoş geldiniz!

---

**Hasılı**: Bu aracı kullanarak Instagram takipçi ilişkileriniz hakkında detaylı analizler yapabilirsiniz. Sizi takip eden ama siz takip etmeyen kişileri, karşılıklı takip ilişkilerinizi ve çeşitli istatistikleri kolayca görebilirsiniz.

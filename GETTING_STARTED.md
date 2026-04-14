# 🎉 Instagram Follower Analyzer - Proje Tamamlandı!

## ✅ Ne İnşa Ettik?

Instagram hesabınızın takipçi ve takip edilen listelerini analiz eden, karşılaştıran ve kapsamlı raporlar sunan **profesyonel bir Python CLI aracı** kurdum.

---

## 📚 Proje İçeriği

### 1. **Ana Uygulama Dosyaları**
- **`cli.py`** - Komut satırı arayüzü (tüm kullanıcı komutları)
- **`instagram_api.py`** - Instagram bağlantısı ve veri çekme
- **`follower_analyzer.py`** - Analiz motoru (karşılaştırma, istatistikler)
- **`config.py`** - Ayar yönetimi
- **`utils.py`** - Veri dışa aktarma (CSV, JSON, HTML)

### 2. **Kurulum ve Yardım Dosyaları**
- **`requirements.txt`** - Tüm Python bağımlılıkları
- **`setup.py`** - Kurulum scripti
- **`test_setup.py`** - Kurulum kontrolü
- **`.env.example`** - Kimlik bilgileri şablonu

### 3. **Dokümantasyon**
- **`README.md`** - Tam kullanım kılavuzu (Türkçe)
- **`QUICKSTART.md`** - 5 dakikalık hızlı başlangıç
- **`DOCUMENTATION.md`** - Teknik dokümantasyon
- **`TROUBLESHOOTING.md`** - Sorun giderme rehberi

### 4. **Örnekler ve Testler**
- **`examples.py`** - Kodda kullanım örnekleri
- **`.gitignore`** - Git yapılandırması

---

## 🚀 Kurulum Adımları (Hızlı)

### Adım 1: Bağımlılıkları Yükleyin
```bash
cd c:\Users\salah\dijinst
pip install -r requirements.txt
```

### Adım 2: Kimlik Bilgilerini Ayarlayın
```bash
cp .env.example .env
```
Sonra `.env` dosyasını açıp şunları ekleyin:
```
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
```

### Adım 3: Kurulumu Test Edin
```bash
python test_setup.py
```

### Adım 4: İlk Çalıştırma
```bash
python cli.py login
python cli.py fetch
python cli.py stats
```

---

## 🎯 Ana Komutlar

```bash
# Giriş yap ve oturumu kaydet
python cli.py login

# Takipçi ve takip verisini indir
python cli.py fetch

# Sizi takip eden ama siz takip ETMeyenleri göster
python cli.py unfollowers

# Siz takip ettiğiniz ama takip ETMeyenleri göster
python cli.py notfollowingback

# Karşılıklı takipçileri göster
python cli.py mutual

# Detaylı istatistikleri göster
python cli.py stats

# Sonuçları JSON'a aktar
python cli.py export
```

---

## 📊 Sistem Özellikleri

### 🔍 Analiz Yetenekleri
- ✅ Takipçi listesi indirme
- ✅ Takip edilen listesi indirme
- ✅ Tek yönlü takipçileri tespit etme
- ✅ Karşılıklı takipçileri gösterme
- ✅ İstatistikler (engagement, follow-back oranları)
- ✅ Doğrulanmış takipçileri filtreleme
- ✅ Özel hesapları gösterme
- ✅ Potansiyel bot hesaplarını tespit etme

### 💾 Veri Yönetimi
- ✅ Otomatik session cache'leme
- ✅ JSON formatında veri saklama
- ✅ Arama ve filtreleme
- ✅ Sıralama seçenekleri
- ✅ Limit belirleme

### 📤 Dışa Aktarma
- ✅ JSON'a aktarma
- ✅ CSV'ye aktarma (gelişmiş)
- ✅ HTML raporu oluşturma (gelişmiş)

### 🛡️ Güvenlik
- ✅ Şifre maskeleme
- ✅ Local session storage
- ✅ .env dosya şifrelemesi
- ✅ Git ignore ayarları

---

## 📁 Proje Yapısı

```
c:\Users\salah\dijinst\
│
├── 📜 Python Modülleri
│   ├── cli.py                  (CLI uygulaması)
│   ├── config.py               (Konfigürasyon)
│   ├── instagram_api.py        (API istemcisi)
│   ├── follower_analyzer.py    (Analiz motoru)
│   ├── utils.py                (Yardımcılar)
│   └── __init__.py             (Package tanımı)
│
├── 🚀 Kurulum Dosyaları
│   ├── requirements.txt         (Bağımlılıklar)
│   ├── setup.py                 (Kurulum scripti)
│   ├── test_setup.py            (Test scripti)
│   ├── .env.example             (Şablonlar)
│   └── .gitignore               (Git ayarları)
│
├── 📖 Dokümantasyon
│   ├── README.md                (Ana rehber)
│   ├── QUICKSTART.md            (Hızlı başlangıç)
│   ├── DOCUMENTATION.md         (Teknik döküman)
│   └── TROUBLESHOOTING.md       (Sorun çözümleri)
│
├── 💡 Örnekler
│   └── examples.py              (Kod örnekleri)
│
└── 💾 Cache (çalıştırıldıktan sonra)
    └── cache/                   (Veriler burada)
        ├── session.json         (Oturum)
        └── *_followers_*.json   (Takipçi verisi)
```

---

## 🎓 Kullanım Örnekleri

### Örnek 1: Basit Analiz
```bash
python cli.py stats
```
📊 Tüm istatistikleri gösterir.

### Örnek 2: Belirli Birini Arama
```bash
python cli.py unfollowers --filter "john"
```
🔍 "john" ismini içeren tek yönlü takipçileri bulur.

### Örnek 3: İlk 100 Sonuç
```bash
python cli.py unfollowers --limit 100
```
📋 İlk 100 tek yönlü takipçiyi gösterir.

### Örnek 4: Python Kodundan Kullanma
```python
from instagram_api import InstagramClient
from follower_analyzer import FollowerAnalyzer

client = InstagramClient()
client.login()

followers = client.get_followers()
following = client.get_following()

analyzer = FollowerAnalyzer(followers, following)
stats = analyzer.get_statistics()

print(f"Engagement Ratio: {stats.engagement_ratio}%")
```

---

## 🔧 Teknik Özellikler

### Kullanılan Kütüphaneler
| Kütüphane | Kullanım |
|-----------|----------|
| **instagrapi** | Instagram bağlantısı ve veri çekme |
| **click** | CLI komutları ve seçenekleri |
| **tabulate** | Güzel tablo gösterimi |
| **requests** | HTTP istekleri |
| **python-dotenv** | .env dosya yönetimi |

### Python Sürümü
- **Minimum**: Python 3.8
- **Tavsiye edilen**: Python 3.10+

---

## ⚠️ Önemli Notlar

### Instagram ToS Uyum
- ✅ Yalnızca kendi hesabınız için kullanın
- ✅ Instagram'ın şartlarına uyun
- ⚠️ Otomatik erişim kontrol edilebilir
- ⚠️ Oran sınırlamaları olabilir (1-2 saat)

### Güvenlik
- 🔒 Şifrenizi asla paylaşmayın
- 🔒 `.env` dosyasını git'e eklemeyin
- 🔒 Kimlik bilgilerini güvenli tutun
- 🔒 Cache'deki verileri gizli tutun

### Performans
- **Küçük hesaplar** (0-500): 1-2 dakika
- **Orta hesaplar** (500-2000): 2-5 dakika
- **Büyük hesaplar** (2000+): 5-30+ dakika

---

## 🆘 Sorun Yaşıyorsanız

1. **Kurulum**: `python test_setup.py` komutunu çalıştırın
2. **Login**: `.env` dosyasını kontrol edin
3. **2FA**: Uygulamaya özgü şifre kullanın
4. **Yardım**: 
   - `QUICKSTART.md` - Hızlı başlangıç
   - `TROUBLESHOOTING.md` - Sorun çözüm
   - `DOCUMENTATION.md` - Teknik bilgi
   - `examples.py` - Kod örnekleri

---

## 📈 İleri Özellikler

### HTML Raporu Oluşturma
```python
from utils import DataExporter
exporter = DataExporter()
exporter.to_html_report(analyzer, 'report.html')
```

### CSV'ye Aktarma
```python
exporter.to_csv(one_way_followers, 'unfollowers.csv')
```

### Özel Filtreleme
```python
verified = analyzer.get_verified_followers()
private = analyzer.get_private_followers()
ghost = analyzer.get_inactive_followers()
```

---

## 🎁 Bonus Özellikler

- ✨ Renkli terminal çıktısı
- ✨ Tablo formatında sonuçlar
- ✨ Unicode ikonlar (✓, 🔒 vb)
- ✨ Türkçe dokümantasyon
- ✨ Detaylı hata mesajları
- ✨ Cache sistem
- ✨ Otomatik session yönetimi

---

## 📞 Hızlı Referans

```bash
# Kurulum
pip install -r requirements.txt
cp .env.example .env
# (Düzenle: INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# İlk Çalıştırma
python test_setup.py          # Kontrol et
python cli.py login           # Giriş yap
python cli.py fetch           # Veri indir

# Analiz
python cli.py stats           # İstatistikleri göster
python cli.py unfollowers     # Tek yönlü takipçiler
python cli.py notfollowingback # Sizi takip etmeyenler
python cli.py mutual          # Karşılıklı takipçiler

# Dışa Aktar
python cli.py export          # JSON'a aktar
```

---

## 🎯 Sonraki Adımlar

1. **Yükle**: `pip install -r requirements.txt`
2. **Yapılandır**: `.env` dosyasını düzenle
3. **Test Et**: `python test_setup.py`
4. **Oturum Aç**: `python cli.py login`
5. **Veri İndir**: `python cli.py fetch`
6. **Analiz Et**: `python cli.py stats`

---

## 💬 Geri Bildirim

Eğer:
- 🐛 Hata bulursanız
- 💡 Fikriniz varsa
- ⚡ İyileştirme öneriniz varsa

Lütfen bildirin!

---

## 📄 Dosya Listeleri

### Kilit Dosyalar
1. `cli.py` - Tüm komutlar burada
2. `follower_analyzer.py` - Analiz mantığı
3. `README.md` - Kullanıcı rehberi
4. `QUICKSTART.md` - Hızlı başlangıç

### Referans Dosyaları
1. `DOCUMENTATION.md` - API referansı
2. `TROUBLESHOOTING.md` - Sorun çözüm
3. `examples.py` - Kod örnekleri

---

## ✨ Teşekkürler

Bu sistem sizin Instagram takipçi ilişkilerinizi detaylı bir şekilde analiz etmek ve anlamak için tasarlanmıştır!

**Başarılı analiz yapmalar dilerim! 🎉**

---

**Sürüm**: 1.0.0  
**Tarih**: 2026-04-14  
**Python**: 3.8+  
**Durum**: ✅ Hazır Kullanıma

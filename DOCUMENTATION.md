# Instagram Follower Analyzer - Proje Dokumentasyonu

## 📑 İçindekiler
1. Proje Özeti
2. Dosya Yapısı
3. Kurulum
4. Kullanım
5. API Referansı
6. Gelişmiş Özellikler
7. Katkıda Bulunma

---

## 1. Proje Özeti

**Instagram Follower Analyzer**, bir Instagram hesabının takipçi ve takip edilen listelerini analiz ederek:
- Kimlerin sizi tek taraflı takip ettiğini gösterir
- Kim'i siz takip ettiğiniz ama takip etmediğini gösterir
- Karşılıklı takip ilişkilerini listeler
- Detaylı istatistikler sağlar
- Sonuçları CSV, JSON ve HTML formatlarında dışa aktarır

**Teknoloji Stack:**
- **Dil**: Python 3.8+
- **Ana Kütüphane**: instagrapi
- **CLI Framework**: Click
- **Veri Formatı**: JSON, CSV, HTML
- **Tablo Gösterimi**: tabulate

---

## 2. Dosya Yapısı

```
dijinst/
├── cli.py                    # Ana CLI uygulaması
├── config.py                 # Konfigürasyon yönetimi
├── instagram_api.py          # Instagram API istemcisi
├── follower_analyzer.py      # Analiz motoru
├── utils.py                  # Yardımcı fonksiyonlar
├── examples.py               # Kod örnekleri
├── test_setup.py             # Kurulum test scripti
├── setup.py                  # Proje kurulum scripti
├── requirements.txt          # Python bağımlılıkları
├── .env.example              # Ortam değişkenleri şablonu
├── .env                      # Gerçek kimlik bilgileri (gitignore)
├── .gitignore                # Git ignore dosyası
├── cache/                    # Takipçi verisi ve session kasası
├── README.md                 # Ana dokümantasyon
├── QUICKSTART.md             # Hızlı başlangıç rehberi
├── TROUBLESHOOTING.md        # Sorun giderme rehberi
└── DOCUMENTATION.md          # Bu dosya
```

---

## 3. Kurulum

### 3.1 Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Aktif Instagram hesabı

### 3.2 Adımlar

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Ortam dosyasını oluştur
cp .env.example .env

# 3. Kimlik bilgilerini ayarla
# .env dosyasını açıp şunları ekle:
# INSTAGRAM_USERNAME=your_username
# INSTAGRAM_PASSWORD=your_password

# 4. Kurulumu test et
python test_setup.py

# 5. Oturum aç ve veri indir
python cli.py login
python cli.py fetch
```

---

## 4. Kullanım

### 4.1 Temel Komutlar

#### Login - Giriş
```bash
python cli.py login
```
Instagram hesabınıza giriş yapar ve oturumu cache'ler.

#### Fetch - Veri İndirme
```bash
python cli.py fetch
```
Takipçi ve takip edilen listelerini indirir.

#### Unfollowers - Tek Yönlü Takipçiler
```bash
python cli.py unfollowers [OPTIONS]
```
Sizi takip eden ama sız takip etmeyen kişileri gösterir.

**Seçenekler:**
- `--limit N` : İlk N sonucu göster (default: 20)
- `--filter KEYWORD` : Arama yap
- `--sort FIELD` : Sırala

**Örnekler:**
```bash
# İlk 50 sonuç
python cli.py unfollowers --limit 50

# İsmi John içeren takipçiler
python cli.py unfollowers --filter "John"

# Doğrulanmış takipçiler
python cli.py unfollowers --filter "verified"
```

#### Not Following Back - Sizi Takip Etmeyenler
```bash
python cli.py notfollowingback [OPTIONS]
```
Siz takip ettiğiniz ama sizi takip etmeyen kişileri gösterir.

#### Mutual - Karşılıklı Takipçiler
```bash
python cli.py mutual [OPTIONS]
```
Birbirinizi takip eden kişileri gösterir.

#### Stats - İstatistikler
```bash
python cli.py stats
```
Takipçi ilişkilerinizin detaylı istatistiklerini gösterir:
- Toplam takipçi/takip
- Karşılıklı takip
- Engagement oranları
- Doğrulanmış takipçiler
- Özel hesaplar
- Potansiyel inaktif hesaplar

#### Export - Dışa Aktarma
```bash
python cli.py export
```
Tüm analiz sonuçlarını JSON dosyasına aktarır.

### 4.2 Komut Kombinasyonları

```bash
# İlk 100 sonucu adıyla birlikte göster
python cli.py unfollowers --limit 100

# "tech" kelimesini içeren takipçileri ara
python cli.py unfollowers --filter "tech"

# Karşılıklı takipçilerin ilk 30'unu göster
python cli.py mutual --limit 30

# İstatistikleri al ve sonuçları görmek için ihraç et
python cli.py stats
python cli.py export
```

---

## 5. API Referansı

### 5.1 InstagramClient Sınıfı

```python
from instagram_api import InstagramClient

# Örnek kullanım
client = InstagramClient()

# Giriş yap
client.login(username='your_username', password='your_password')

# Takipçileri al
followers = client.get_followers()  # Dict[int, Dict]

# Takip edilenleri al
following = client.get_following()  # Dict[int, Dict]

# Kullanıcı bilgisi al
user_info = client.get_user_info()  # Dict

# Verileri kaydet
client.save_data(followers, following)
```

**Dönüş Biçimi:**
```python
{
    user_id: {
        'username': 'john_doe',
        'full_name': 'John Doe',
        'is_verified': False,
        'is_private': False
    },
    ...
}
```

### 5.2 FollowerAnalyzer Sınıfı

```python
from follower_analyzer import FollowerAnalyzer

analyzer = FollowerAnalyzer(followers, following)

# Tek yönlü takipçiler
one_way = analyzer.get_one_way_followers()  # Dict[int, Dict]

# Takip ettiğiniz ama takip etmeyen
not_following_back = analyzer.get_one_way_following()  # Dict[int, Dict]

# Karşılıklı takipçiler
mutuals = analyzer.get_mutual_followers()  # Dict[int, Tuple]

# İstatistikler
stats = analyzer.get_statistics()  # FollowerStats

# Filtre
filtered = analyzer.filter_by_keyword(followers, 'john')

# Detaylı analiz
summary = analyzer.export_comparison_summary()  # Dict
```

### 5.3 DataExporter Sınıfı

```python
from utils import DataExporter

exporter = DataExporter()

# CSV'ye aktarma
exporter.to_csv(data, 'output.csv')

# JSON'a aktarma
exporter.to_json(data, 'output.json')

# HTML raporu oluşturma
exporter.to_html_report(analyzer, 'report.html')
```

---

## 6. Gelişmiş Özellikler

### 6.1 Programmatik Kullanım

```python
from instagram_api import InstagramClient
from follower_analyzer import FollowerAnalyzer
from utils import DataExporter

# Temel workflow
client = InstagramClient()
client.login()

followers = client.get_followers()
following = client.get_following()

analyzer = FollowerAnalyzer(followers, following)
stats = analyzer.get_statistics()

print(f"Engagement: {stats.engagement_ratio}%")

# Sonuçları aktar
exporter = DataExporter()
exporter.to_json(analyzer.export_comparison_summary(), 'analysis.json')
```

### 6.2 Filtreleme ve Arama

```python
# Belirli isim/username arama
results = analyzer.filter_by_keyword(one_way_followers, 'tech')

# Doğrulanmış takipçiler
verified = analyzer.get_verified_followers()

# Özel hesaplar
private = analyzer.get_private_followers()

# Potansiyel bot hesapları
inactive = analyzer.get_inactive_followers()
```

### 6.3 Veri Analizi

```python
# Tüm istatistikleri bir yerde topla
full_analysis = {
    'stats': analyzer.get_statistics(),
    'summary': analyzer.export_comparison_summary(),
    'one_way_followers': analyzer.get_one_way_followers(),
    'one_way_following': analyzer.get_one_way_following(),
    'mutuals': analyzer.get_mutual_followers()
}
```

---

## 7. Performans Notları

### Veri İndirme Süresi

| Durumdu | Ortalama Zaman |
|---------|---------|
| 0-500 takipçi | 1-2 dakika |
| 500-2000 takipçi | 2-5 dakika |
| 2000-10000 takipçi | 5-15 dakika |
| 10000+ takipçi | 15-30+ dakika |

### Oran Sınırlaması

Instagram API oran sınırlamalarına sahip. Eğer hata alırsanız:
```
Rate limit exceeded - HTTP 429
```

1-2 saat bekleyip tekrar deneyin.

### Optimizasyon İpuçları

1. **Cache kullanın**: Veriler `.cache/` dizininde saklanır
2. **Kesme işlemleri**: Çok sık çalıştırmayın (maksimum günde 2-3 kez)
3. **VPN kullanmayın**: Instagram engel atabilir
4. **2FA devre dışı bırakın**: Giriş hızlanır (veya uyg şifresi kullanın)

---

## 8. Sorun Giderme Hızlı Referans

| Sorun | Çözüm |
|-------|-------|
| Login başarısız | .env dosyasını kontrol edin |
| 2FA hatası | Uygulamaya özgü şifre kullanın |
| No cached data | `python cli.py fetch` çalıştırın |
| Rate limit | 1-2 saat bekleyin |
| Türkçe göstermiyor | Terminal kodlaması değiştirin |

Detaylar için `TROUBLESHOOTING.md`'ye bakın.

---

## 9. Katkıda Bulunma

### Hata Bildirme
Hata bulursanız lütfen:
1. Hata mesajını not edin
2. Hangi komutu çalıştırdığınızı yazın
3. Python ve bağımlılıkları versiyonlarını kontrol edin

### İyileştirme Önerileri
Öneriniz varsa:
1. Özelliği açıkça tanımlayın
2. Neden gerekli olduğunu açıklayın
3. Kod örneği sağlayın (opsiyonel)

---

## 10. Lisans ve Kullanım Şartları

⚠️ **Önemli:**
- Bu araç kişisel kullanım içindir
- Instagram'ın hizmet şartlarına uyun
- Otomatik erişim Instagram tarafından kontrol edilebilir
- Üçüncü taraflarla veri paylaşmayın
- Kişiden izin almadan veri toplamayın

---

## Destek

Sorularınız varsa:
- `QUICKSTART.md` - Hızlı başlangıç
- `TROUBLESHOOTING.md` - Sorun çözüm
- `examples.py` - Kod örnekleri

---

**Son Güncelleme**: 2026-04-14
**Sürüm**: 1.0.0
**Yazar**: Instagram Analyzer Team

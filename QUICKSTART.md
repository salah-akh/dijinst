# HIZLI BAŞLANGIÇ KILAVUZU
# Instagram Takipçi Analiz Sistemi - Kurulum ve Kullanım

## ⚡ 5 Dakikalık Kurulum

### Adım 1: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 2: Kimlik Bilgilerini Ayarlayın
```bash
cp .env.example .env
```

Sonra `.env` dosyasını açın ve şunları ekleyin:
```
INSTAGRAM_USERNAME=sizin_kullanıcı_adınız
INSTAGRAM_PASSWORD=sizin_şifreniz
```

### Adım 3: Oturum Açın
```bash
python cli.py login
```

### Adım 4: Verileri İndirin
```bash
python cli.py fetch
```

### Adım 5: Analizi Görüntüleyin
```bash
python cli.py stats
```

---

## 🎯 En Sık Yapılan İşlemler

### Beni Takip Eden Ama Ben Takip Etmeyenleri Görmek
```bash
python cli.py unfollowers
```

### Sizi Takip Etmeyen Kişileri Görmek
```bash
python cli.py notfollowingback
```

### Karşılıklı Takip Listesini Görmek
```bash
python cli.py mutual
```

### Detaylı İstatistikleri Görmek
```bash
python cli.py stats
```

### Sonuçları JSON'a Aktarmak
```bash
python cli.py export
```

---

## 📊 Çıktı Örnekleri

### stats komutu çıktısı
```
📊 Follower Statistics

┌──────────────────────┬──────────┐
│ Metric               │ Value    │
├──────────────────────┼──────────┤
│ Total Followers      │ 1500     │
│ Total Following      │ 800      │
│ Mutual Follows       │ 650      │
│ One-Way Followers    │ 850      │
│ One-Way Following    │ 150      │
│ Engagement Ratio     │ 43.33%   │
│ Follow-Back Ratio    │ 81.25%   │
└──────────────────────┴──────────┘
```

### unfollowers komutu çıktısı
```
👥 People who follow you but you don't follow back (850 total)

┌──────────────┬─────────────────┬──────────┬─────────┐
│ Username     │ Full Name       │ Verified │ Private │
├──────────────┼─────────────────┼──────────┼─────────┤
│ john_creator │ John Smith      │ ✓        │         │
│ jane_writes  │ Jane Williams   │          │ 🔒      │
│ ...          │ ...             │ ...      │ ...     │
└──────────────┴─────────────────┴──────────┴─────────┘
```

---

## 💡 İpuçları ve Püf Noktaları

### Filtreleme
Belirli bir kişiyi veya grubu aramak için:
```bash
python cli.py unfollowers --filter "john"
```

### Sonuç Sayısını Sınırlama
İlk 50 sonucu görmek için:
```bash
python cli.py unfollowers --limit 50
```

### Komut Kombinasyonları
İlk 30 uno taraflı takipçisi `teknoloji` kelimesi içeren:
```bash
python cli.py unfollowers --limit 30 --filter "teknoloji"
```

---

## 🔍 Analiz Ayıklaması

### Metric    | Ne Demek? | Neden İnemli?
|-----------|----------|-------------|
| Engagement Ratio | Takipçilerinizin kaçı karşılıklı takip ediyor | Topluluk bağlılığını gösterir |
| Follow-Back Ratio | Takip ettiğiniz kişilerin yüzde kaçı sizi takip ediyor | Etkiniz gösterir |
| One-Way Followers | Sadece sizi takip eden kişiler | İlgi tabanınız |
| Verified Followers | Doğrulanmış takipçiler | Etkinlik ve güven |

---

## ⚠️ Önemli Uyarılar

1. **Şifre Güvenliği**: Şifrenizi asla başkasıyla paylaşmayın
2. **Veri Gizliliği**: İndirilen kişi verileri gizli tutun
3. **Instagram ToS**: Bu aracı Instagram'ın kullanıcı anlaşmasına uygun kullanın
4. **Oran Sınırlaması**: Çok sık çalıştırırsanız Instagram geçici olarak engel atabilir

---

## 🛠️ Ortamı Sıfırlama

Tüm cache verilerini silip temiz başlamak için:
```bash
rm -r cache/*
```

Veya Windows'ta:
```bash
rmdir /s cache
```

---

## 📚 Gelişmiş Kullanım

### Python Kodundan Kullanma
```python
from instagram_api import InstagramClient
from follower_analyzer import FollowerAnalyzer

# Giriş yap
client = InstagramClient()
client.login()

# Verileri al
followers = client.get_followers()
following = client.get_following()

# Analiz yap
analyzer = FollowerAnalyzer(followers, following)
stats = analyzer.get_statistics()

print(f"Engagement Ratio: {stats.engagement_ratio}%")
```

### CSV'ye Aktarma
```bash
python cli.py export  # JSON'a aktarır
# Sonra JSON'u CSV'ye dönüştürebilirsiniz
```

---

## 🐛 Sık Sorunlar

| Sorun | Çözüm |
|-------|-------|
| "No cached data" | `python cli.py fetch` çalıştırın |
| "Login failed" | Kimlik bilgilerini `.env` dosyasında kontrol edin |
| 2FA hatası | Uygulamaya özgü şifre kullanın |
| Türkçe göstermiyor | Windows'ta PowerShell yerine Command Prompt kullanın |

Daha fazla sorun için `TROUBLESHOOTING.md`'ye bakın.

---

## 📞 Yardım Komutları

Belirli komut hakkında yardım:
```bash
python cli.py unfollowers --help
python cli.py stats --help
python cli.py export --help
```

Tüm komutları görmek:
```bash
python cli.py --help
```

---

## 🎉 Başarılı Kurulumun İşaretleri

Tüm kurulum başarılı ise:
- ✅ `python cli.py login` bitmeli
- ✅ `cache/` klasörü oluşturulmalı
- ✅ `python cli.py stats` sonuçları göstermeli
- ✅ Türkçe karakterler düzgün gösterilmeli

---

**Hedefli Sonuç**: Artık Instagram takipçi ilişkileriniz hakkında detaylı analiz yapabilirsiniz!

---

Daha fazla bilgi için:
- 📖 README.md - Tam dokümantasyon
- 🔧 TROUBLESHOOTING.md - Sorun giderme
- 💻 examples.py - Kod örnekleri

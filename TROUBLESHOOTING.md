# TROUBLESHOOTING GUIDE
# Instagram Follower Analyzer - Sorun Giderme Rehberi

## Sık Karşılaşılan Sorunlar ve Çözümleri

### 1. "No module named 'instagrapi'" Error

**Sorun**: Bağımlılıklar yüklenmemiş

**Çözüm**:
```bash
pip install -r requirements.txt
```

Eğer hala sorun yaşıyorsanız:
```bash
pip install --upgrade pip
pip install instagrapi requests click tabulate python-dotenv
```

---

### 2. "Instagram credential not provided"

**Sorun**: .env dosyasında kimlik bilgileri eksik

**Çözüm**:
1. `.env` dosyasını açın (varsa) veya `.env.example`'dan kopyalayın:
```bash
cp .env.example .env
```

2. `.env` dosyasını düzenleyin:
```
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here
```

3. Dosyayı kaydedin ve tekrar deneyin

---

### 3. "Login failed: Invalid credentials"

**Sorun**: Şifre veya kullanıcı adı yanlış

**Çözüm**:
- Kullanıcı adınızı telaffuz (@ olmadan) kontrol edin
- Şifrenizin doğru olduğundan emin olun
- Caps Lock'u kontrol edin
- Şifrenizde özel karakterler varsa uygun şekilde kaçış karakteri kullanın

---

### 4. "Two-factor authentication is enabled"

**Sorun**: Instagram hesabınızda iki faktörlü kimlik doğrulama etkin

**Çözüm - Seçenek 1**: Uygulamaya özgü şifre kullanın
1. Instagram > Settings & Privacy > Accounts Center > Security
2. "Uygulamaya özgü şifreler" bölümüne gidin
3. Yeni bir şifre oluşturun
4. Bu şifreyi `.env` dosyasında kullanın

**Çözüm - Seçenek 2**: Geçici olarak 2FA'yı devre dışı bırakın
1. Instagram > Settings > Account > Security > Two-factor Authentication
2. Kapatın
3. Aracı çalıştırın
4. İşlem bitince tekrar açın

---

### 5. "Session expired"

**Sorun**: Kaydedilmiş oturum süresi dolmuş

**Çözüm**:
```bash
python cli.py login
```

Veya cache dosyasını silin ve tekrar deneyin:
```bash
rm cache/session.json
python cli.py login
```

---

### 6. "No cached data found"

**Sorun**: Takipçi ve takip verisi indirilmemiş

**Çözüm**:
```bash
python cli.py fetch
```

Bu komutu çalıştırarak verilerinizi indirin

---

### 7. "Rate limit exceeded" veya "429 Error"

**Sorun**: Instagram API'ının oran sınırlamasına ulaştınız

**Çözüm**:
1. 1-2 saat bekleyin
2. VPN kullanmayın
3. Başka cihazlardan giriş yapmayı durdurun
4. Aracı tekrar kullanmayı deneyin

---

### 8. Komut çalıştırılmıyor (Windows)

**Sorun**: PowerShell güvenlik politikası engelleme

**Çözüm**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Veya Python'ı doğrudan çalıştırın:
```bash
python cli.py fetch
```

---

### 9. Türkçe karakterleri göstermiyor

**Sorun**: Terminal kodlaması sorunları

**Windows çözümü**:
```powershell
$env:PYTHONIOENCODING = "utf-8"
python cli.py stats
```

Linux/Mac çözümü:
```bash
export PYTHONIOENCODING=utf-8
python cli.py stats
```

---

### 10. "Permission denied" (cache dosyalarına yazamıyor)

**Sorun**: Klasör izinleri yetersiz

**Windows çözümü**:
1. `dijinst` klasörüne sağ tıklayın
2. Properties > Security > Edit
3. Kendi kullanıcınızı seçin
4. Full Control izni verin

**Linux/Mac çözümü**:
```bash
chmod -R 755 cache
```

---

### 11. Python bulunamıyor

**Sorun**: Python PATH'e eklenmemiş

**Windows çözümü**:
```bash
python --version
# Veya
py --version
```

Eğer çalışmıyorsa:
```bash
C:\Users\YourUsername\AppData\Local\Python\Python311\python.exe cli.py fetch
```

---

### 12. Takipçi verisi boş gösteri

**Sorun**: Hesap çok yeni veya takipçi yok

**Çözüm**:
- Genel hesabınızı kontrol edin (özel hesaplar takipçi göstermeyebilir)
- Hesabınızda en az birkaç takipçi olduğundan emin olun
- 24 saat bekleyip tekrar deneyin

---

## Hata Mesajı Referansı

| Hata | Anlamı | Çözüm |
|------|--------|------|
| `LoginRequired` | Oturum geçersiz | `python cli.py login` çalıştırın |
| `HTTPException` | Ağ bağlantısı sorunu | İnternet bağlantısını kontrol edin |
| `FileNotFoundError` | Dosya bulunamadı | Dosya yolunu kontrol edin |
| `JSONDecodeError` | Bozuk JSON verisi | Cache'i silin: `rm cache/*_*.json` |

---

## Loglama Etkinleştirme (Gelişmiş)

Detaylı hata ayıklama için:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

`cli.py` dosyasının başına ekleyin.

---

## İletişim ve Destek

Sorun çözemediyseniz:

1. Hata mesajını tam olarak not edin
2. `.env` dosyasının doğru yapılandırıldığını kontrol edin
3. Python sürümünü kontrol edin: `python --version`
4. Bağımlılıkları güncelleyin: `pip install -r requirements.txt --upgrade`

---

## Güvenlik Notları

⚠️ **Dikkat**:
- Şifrenizi hiç kimseyle paylaşmayın
- `.env` dosyasını git'e commit ETMEYİN
- Cache dosyalarında kısmen şifre bilgileri bulunabilir
- Bu aracı yalnızca kendi hesabınızda kullanın

---

## Veri Gizliliği

Bu aracı kullanırken:
- Dışa aktarılan dosyaları güvenli bir şekilde saklayın
- Kişisel bilgiler içeren raporları paylaşmayın
- Düzenli olarak cache'i temizleyin: `rm -r cache/*`

---

**Son Güncellenme**: 2026-04-14

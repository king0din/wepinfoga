# Bilgi Toplama Botu

Telegram botu ile entegre bir web sunucusu sistemi. Bot, kullanıcılar için benzersiz takip bağlantıları oluşturur ve bu bağlantılara tıklayan kişilerin rızasıyla IP adresi ve cihaz bilgilerini toplar.

## 🚀 Özellikler

- **Güvenli Veri Toplama**: Yalnızca IP adresi ve tarayıcı bilgisi toplanır
- **Rıza Tabanlı**: Kullanıcı onayı olmadan hiçbir veri toplanmaz
- **Telegram Entegrasyonu**: Kolay kullanım için Telegram bot arayüzü
- **Modern Web Arayüzü**: Responsive ve profesyonel tasarım
- **SQLite Veritabanı**: Güvenli veri saklama
- **Gerçek Zamanlı Takip**: Anlık veri toplama ve bildirim

## 📋 Sistem Gereksinimleri

- Python 3.11+
- Flask ve bağımlılıkları
- SQLite3
- Telegram Bot Token

## 🛠️ Kurulum

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/king0din/gigaprocect.git
cd gigaprocect
```

### 2. Web Sunucusunu Kurun
```bash
cd web_server
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Telegram Botunu Kurun
```bash
cd ../bot
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Telegram Bot Token Alın
1. Telegram'da @BotFather'a mesaj gönderin
2. `/newbot` komutunu kullanın
3. Bot için bir isim ve kullanıcı adı seçin
4. Aldığınız token'ı `bot/telegram_bot.py` dosyasındaki `BOT_TOKEN` değişkenine girin

### 5. Sistemi Başlatın
```bash
# Terminal 1: Web sunucusunu başlatın
cd web_server
source venv/bin/activate
python production_server.py

# Terminal 2: Telegram botunu başlatın
cd bot
source venv/bin/activate
python telegram_bot.py
```

## 🧪 Test

Sistem entegrasyonunu test etmek için:
```bash
python test_integration.py
```

## 📖 Kullanım

### Telegram Bot Komutları
- `/start` - Botu başlat
- `/link_olustur` - Yeni takip bağlantısı oluştur
- `/bilgilerim` - Toplanan verileri görüntüle
- `/help` - Yardım menüsü

### Web Arayüzü
- Ana sayfa: `http://localhost:5004/`
- Takip bağlantıları: Bot tarafından oluşturulan URL'ler

## 🔒 Güvenlik ve Gizlilik

### Toplanan Bilgiler
- ✅ IP Adresi
- ✅ Tarayıcı ve işletim sistemi bilgisi

### Toplanmayan Bilgiler
- ❌ Telefon numarası
- ❌ Kameradan görüntü
- ❌ Kişisel dosyalar
- ❌ Şifreler

### Yasal Uyarılar
- Bu sistem yalnızca yasal ve etik amaçlar için kullanılmalıdır
- Kullanıcının açık rızası olmadan veri toplanmaz
- KVKK ve GDPR gibi veri koruma yasalarına uygun hareket etmek kullanıcının sorumluluğundadır
- Kötüye kullanım durumunda sorumluluk kullanıcıya aittir

## 📁 Proje Yapısı

```
gigaprocect/
├── web_server/                 # Flask web sunucusu
│   ├── models/                 # Veritabanı modelleri
│   ├── routes/                 # API endpoint'leri
│   ├── static/                 # Statik dosyalar (HTML, CSS)
│   ├── database/               # SQLite veritabanı
│   ├── venv/                   # Python virtual environment
│   ├── production_server.py    # Production sunucusu
│   └── test_server.py          # Test sunucusu
├── bot/                        # Telegram bot
│   ├── telegram_bot.py         # Ana bot dosyası
│   ├── requirements.txt        # Bot bağımlılıkları
│   ├── README.md               # Bot kurulum talimatları
│   └── bot_commands.md         # Bot komutları dokümantasyonu
├── test_integration.py         # Entegrasyon testleri
├── schema.sql                  # Veritabanı şeması
├── DEPLOYMENT.md               # Deployment rehberi
└── README.md                   # Bu dosya
```

## 🔧 API Endpoint'leri

### POST /api/create_link
Yeni takip bağlantısı oluşturur.
```json
{
  "sender_telegram_id": 123456789
}
```

### GET /api/get_collected_data/{user_id}
Kullanıcının toplanan verilerini getirir.

### GET /track?tracking_id={id}&sender_id={id}
Rıza formunu gösterir.

### POST /collect_data
Rıza formundan gelen verileri işler.

## 🚀 Deployment

Detaylı deployment rehberi için `DEPLOYMENT.md` dosyasına bakın.

## 🐛 Sorun Giderme

Detaylı sorun giderme bilgileri için `DEPLOYMENT.md` dosyasına bakın.

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. `test_integration.py` scriptini çalıştırın
2. Log dosyalarını kontrol edin
3. Proje dokümantasyonunu inceleyin

## 📄 Lisans

Bu proje GPL-3.0 lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

---

**⚠️ Önemli Notlar:**
- Bu sistem güçlü bir araçtır ve sorumlu bir şekilde kullanılmalıdır. Kişisel veri koruma yasalarına uygun hareket etmek ve kullanıcıların gizliliğini korumak sizin sorumluluğunuzdadır.
- Production ortamında mutlaka HTTPS kullanın
- Bot token'ını asla kod içinde saklamayın, environment variable olarak kullanın
- Düzenli olarak sistem güncellemelerini yapın
- Log dosyalarını düzenli olarak temizleyin
- Veritabanını düzenli olarak yedekleyin


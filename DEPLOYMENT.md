# Deployment Rehberi

Bu rehber, Bilgi Toplama Botu'nu production ortamında nasıl deploy edeceğinizi açıklar.

## 🚀 Hızlı Başlangıç (Yerel Test)

### 1. Sistemi Başlatın
```bash
# Terminal 1: Web sunucusunu başlatın
cd web_server
source venv/bin/activate
python production_server.py

# Terminal 2: Telegram botunu başlatın (token gerekli)
cd bot
python telegram_bot.py
```

### 2. Test Edin
```bash
# Entegrasyon testlerini çalıştırın
python test_integration.py

# Web arayüzünü kontrol edin
# http://localhost:5004/
```

## 🌐 Production Deployment

### Seçenek 1: Manus Platform (Önerilen)

#### Web Sunucusu Deployment
```bash
# Web sunucusunu deploy edin
cd web_server
# Manus deployment komutları burada olacak
```

#### Bot Deployment
```bash
# Bot'u ayrı bir servis olarak deploy edin
cd bot
# Bot token'ınızı environment variable olarak ayarlayın
export BOT_TOKEN="your_bot_token_here"
python telegram_bot.py
```

### Seçenek 2: Manuel Server Deployment

#### Gereksinimler
- Ubuntu 20.04+ veya CentOS 8+
- Python 3.11+
- Nginx (opsiyonel)
- Systemd (servis yönetimi için)

#### 1. Sunucu Hazırlığı
```bash
# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Python ve pip kurulumu
sudo apt install python3.11 python3.11-venv python3-pip -y

# Nginx kurulumu (opsiyonel)
sudo apt install nginx -y
```

#### 2. Proje Deployment
```bash
# Proje dosyalarını sunucuya kopyalayın
scp -r info_collector_bot user@your-server:/opt/

# Sunucuda
cd /opt/info_collector_bot

# Web sunucusu bağımlılıklarını yükleyin
cd web_server
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Bot bağımlılıklarını yükleyin
cd ../bot
pip install -r requirements.txt
```

#### 3. Systemd Servisleri

**Web Sunucusu Servisi** (`/etc/systemd/system/info-collector-web.service`):
```ini
[Unit]
Description=Info Collector Web Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/info_collector_bot/web_server
Environment=PATH=/opt/info_collector_bot/web_server/venv/bin
ExecStart=/opt/info_collector_bot/web_server/venv/bin/python production_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Telegram Bot Servisi** (`/etc/systemd/system/info-collector-bot.service`):
```ini
[Unit]
Description=Info Collector Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/info_collector_bot/bot
Environment=PATH=/opt/info_collector_bot/bot
Environment=BOT_TOKEN=your_bot_token_here
ExecStart=/usr/bin/python3.11 telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Servisleri Başlatın
```bash
# Servisleri etkinleştirin
sudo systemctl enable info-collector-web
sudo systemctl enable info-collector-bot

# Servisleri başlatın
sudo systemctl start info-collector-web
sudo systemctl start info-collector-bot

# Durumu kontrol edin
sudo systemctl status info-collector-web
sudo systemctl status info-collector-bot
```

#### 5. Nginx Konfigürasyonu (Opsiyonel)

**Nginx Config** (`/etc/nginx/sites-available/info-collector`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    
    location /api/ {
        limit_req zone=api burst=5 nodelay;
        proxy_pass http://127.0.0.1:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Nginx konfigürasyonunu etkinleştirin
sudo ln -s /etc/nginx/sites-available/info-collector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 Güvenlik Konfigürasyonu

### 1. Environment Variables
```bash
# Bot token'ını güvenli şekilde saklayın
echo "BOT_TOKEN=your_bot_token_here" >> /opt/info_collector_bot/.env

# .env dosyasını bot kodunda kullanın
```

### 2. Firewall Ayarları
```bash
# UFW firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. SSL Sertifikası (Let's Encrypt)
```bash
# Certbot kurulumu
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikası alın
sudo certbot --nginx -d your-domain.com
```

### 4. Log Yönetimi
```bash
# Log rotasyonu için logrotate konfigürasyonu
sudo nano /etc/logrotate.d/info-collector
```

## 📊 Monitoring ve Maintenance

### 1. Log İzleme
```bash
# Web sunucusu logları
sudo journalctl -u info-collector-web -f

# Bot logları
sudo journalctl -u info-collector-bot -f

# Nginx logları
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Sistem Durumu
```bash
# Servis durumları
sudo systemctl status info-collector-web
sudo systemctl status info-collector-bot

# Sistem kaynakları
htop
df -h
```

### 3. Veritabanı Yedekleme
```bash
# SQLite veritabanını yedekleyin
cp /opt/info_collector_bot/web_server/src/database/app.db /backup/app_$(date +%Y%m%d_%H%M%S).db

# Otomatik yedekleme için cron job
echo "0 2 * * * cp /opt/info_collector_bot/web_server/src/database/app.db /backup/app_\$(date +\%Y\%m\%d_\%H\%M\%S).db" | sudo crontab -
```

## 🔧 Troubleshooting

### Web Sunucusu Sorunları
```bash
# Port kullanımını kontrol edin
sudo netstat -tlnp | grep :5004

# Servis loglarını kontrol edin
sudo journalctl -u info-collector-web --since "1 hour ago"

# Manuel başlatma
cd /opt/info_collector_bot/web_server
source venv/bin/activate
python production_server.py
```

### Bot Sorunları
```bash
# Bot token'ını kontrol edin
echo $BOT_TOKEN

# Bot loglarını kontrol edin
sudo journalctl -u info-collector-bot --since "1 hour ago"

# Manuel başlatma
cd /opt/info_collector_bot/bot
python telegram_bot.py
```

### Veritabanı Sorunları
```bash
# Veritabanı dosya izinlerini kontrol edin
ls -la /opt/info_collector_bot/web_server/src/database/

# Veritabanı bütünlüğünü kontrol edin
sqlite3 /opt/info_collector_bot/web_server/src/database/app.db "PRAGMA integrity_check;"
```

## 📈 Performance Optimization

### 1. Gunicorn ile Production WSGI
```bash
# Gunicorn kurulumu
pip install gunicorn

# Gunicorn ile çalıştırma
gunicorn --bind 0.0.0.0:5004 --workers 4 production_server:app
```

### 2. Redis Cache (Opsiyonel)
```bash
# Redis kurulumu
sudo apt install redis-server -y

# Flask-Caching entegrasyonu
pip install Flask-Caching redis
```

### 3. Database Optimization
```bash
# SQLite optimizasyonu
sqlite3 /opt/info_collector_bot/web_server/src/database/app.db "VACUUM;"
sqlite3 /opt/info_collector_bot/web_server/src/database/app.db "ANALYZE;"
```

---

**⚠️ Önemli Notlar:**
- Production ortamında mutlaka HTTPS kullanın
- Bot token'ını asla kod içinde saklamayın
- Düzenli olarak sistem güncellemelerini yapın
- Log dosyalarını düzenli olarak temizleyin
- Veritabanını düzenli olarak yedekleyin


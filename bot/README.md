# Telegram Bot Kurulum Talimatları

## Bot Token Alma

1. Telegram'da @BotFather'a mesaj gönderin
2. `/newbot` komutunu kullanın
3. Bot için bir isim seçin (örn: "Bilgi Toplama Botu")
4. Bot için bir kullanıcı adı seçin (örn: "bilgi_toplama_bot")
5. BotFather size bir token verecek (örn: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz")

## Bot Token'ını Ayarlama

1. `telegram_bot.py` dosyasını açın
2. `BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"` satırını bulun
3. `YOUR_BOT_TOKEN_HERE` kısmını BotFather'dan aldığınız token ile değiştirin
4. Dosyayı kaydedin

Örnek:
```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

## Bot'u Çalıştırma

1. Web sunucusunun çalıştığından emin olun (port 5003)
2. Terminal'de bot dizinine gidin:
   ```bash
   cd /home/ubuntu/info_collector_bot/bot
   ```
3. Bot'u çalıştırın:
   ```bash
   python telegram_bot.py
   ```

## Bot Komutları

- `/start` - Botu başlat
- `/link_olustur` - Yeni takip bağlantısı oluştur
- `/bilgilerim` - Toplanan verileri görüntüle
- `/help` - Yardım menüsü

## Güvenlik Notları

- Bot token'ınızı kimseyle paylaşmayın
- Production ortamında token'ı environment variable olarak saklayın
- Bot'u yalnızca yasal ve etik amaçlar için kullanın


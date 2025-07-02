
## Web Sunucusu Endpointleri ve Veri Akışı

### `GET /track`
- **Amaç:** Kullanıcının (alıcının) tıkladığı takip bağlantısı.
- **Parametreler:** `tracking_id` (benzersiz bağlantı ID'si), `sender_id` (bağlantıyı oluşturan Telegram kullanıcısının ID'si).
- **İşleyiş:**
  1. `tracking_id` ve `sender_id`'yi doğrular.
  2. Kullanıcıya (alıcıya) rıza formunu içeren bir HTML sayfası sunar.
  3. Bu sayfada, hangi bilgilerin (IP, User-Agent) toplanacağı ve kime (bağlantıyı oluşturan kullanıcıya) gönderileceği açıkça belirtilir.
  4. Kullanıcıdan (alıcıdan) onayı (Evet/Hayır butonu) ister.

### `POST /collect_data`
- **Amaç:** Rıza formundan gelen onayı işlemek ve bilgileri kaydetmek.
- **Parametreler (Form Verisi):** `tracking_id`, `sender_id`, `consent` (boolean: true/false).
- **İşleyiş:**
  1. `consent` true ise:
     - İsteği yapan cihazın IP adresini ve User-Agent bilgisini alır.
     - `tracking_id`, `sender_id`, IP adresi ve User-Agent bilgilerini veritabanına kaydeder.
     - Telegram botuna, toplanan verileri içeren bir bildirim (POST isteği) gönderir.
     - Kullanıcıya (alıcıya) bir teşekkür veya onay mesajı gösterir.
  2. `consent` false ise:
     - Veri toplamaz.
     - Kullanıcıya (alıcıya) bir bilgilendirme mesajı gösterir.

### `POST /notify_bot` (Botun API endpoint'i)
- **Amaç:** Web sunucusunun, toplanan verileri Telegram botuna bildirmesi.
- **Parametreler (JSON Body):** `tracking_id`, `sender_telegram_id`, `ip_address`, `user_agent`.
- **İşleyiş:**
  1. Bot, bu isteği alır.
  2. `sender_telegram_id`'ye sahip kullanıcıya, toplanan IP adresi ve User-Agent bilgisini içeren bir mesaj gönderir.



## Bot Komutları ve Akışı

### `/start`
- Botu başlatan komut. Kullanıcıya botun ne işe yaradığını ve nasıl kullanılacağını açıklar.
- Kullanıcıya `/link_olustur` komutunu kullanmasını önerir.

### `/link_olustur`
- Kullanıcının benzersiz bir takip bağlantısı oluşturmasını sağlar.
- Bot, web sunucusundan bir takip ID'si alır ve bu ID ile birlikte kullanıcının Telegram ID'sini içeren bir URL oluşturur.
- Oluşturulan URL'yi ve bu URL'nin ne işe yaradığını, hangi bilgileri toplayacağını ve rıza mekanizmasını açıklayan bir uyarı mesajını kullanıcıya gönderir.
- Örnek Uyarı Mesajı:
  ```
  ⚠️ DİKKAT: Bu bağlantı, tıkladığınızda veya başkaları tıkladığında cihazın IP adresini ve temel tarayıcı bilgilerini (işletim sistemi, tarayıcı türü) toplayacaktır. Bu bilgiler, bağlantıyı oluşturan kullanıcıya iletilecektir. Telefon numarası veya kamera gibi hassas bilgilere erişilmeyecektir. Lütfen bu bağlantıyı yalnızca bilgilerin toplanmasına rıza gösteren kişilerle paylaşın.

  Bağlantınız: [Oluşturulan URL]
  ```

### `/bilgilerim`
- Kullanıcının oluşturduğu bağlantılar aracılığıyla toplanan bilgileri listeler.
- Her bir bağlantı için kaç kez tıklandığını ve toplanan IP/cihaz bilgilerini gösterir.

### Web Sunucusundan Gelen Bildirim Akışı
- Web sunucusu, bir bağlantıya tıklandığında ve rıza alındığında, botun bir API endpoint'ine (örneğin, `/notify_collected_data`) POST isteği gönderir.
- Bu istek, takip ID'sini, gönderen kullanıcının Telegram ID'sini, toplanan IP adresini ve User-Agent bilgisini içerir.
- Bot, bu bilgiyi alır ve ilgili kullanıcıya (sender_telegram_id) toplanan verileri içeren bir mesaj gönderir.



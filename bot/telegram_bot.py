import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Web sunucusu URL'si
WEB_SERVER_URL = "http://localhost:5004"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot başlatma komutu"""
    welcome_message = """
🤖 **Bilgi Toplama Botu'na Hoş Geldiniz!**

Bu bot, size özel takip bağlantıları oluşturarak, bu bağlantılara tıklayan kişilerin cihaz bilgilerini (IP adresi ve tarayıcı bilgisi) toplamanıza yardımcı olur.

⚠️ **ÖNEMLİ UYARI:**
- Bu bot, yalnızca yasal ve etik amaçlar için kullanılmalıdır
- Bağlantıyı paylaştığınız kişilerin rızası alınmalıdır
- Toplanan veriler, kişisel veri koruma yasalarına uygun şekilde kullanılmalıdır

**Kullanılabilir Komutlar:**
/link_olustur - Yeni bir takip bağlantısı oluştur
/bilgilerim - Toplanan verileri görüntüle
/help - Yardım menüsü

Başlamak için /link_olustur komutunu kullanın.
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def create_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yeni takip bağlantısı oluştur"""
    user_id = update.effective_user.id
    
    try:
        # Web sunucusundan yeni bağlantı iste
        response = requests.post(
            f"{WEB_SERVER_URL}/api/create_link",
            json={"sender_telegram_id": user_id},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            tracking_url = data['tracking_url']
            tracking_id = data['tracking_id']
            
            message = f"""
✅ **Takip Bağlantınız Oluşturuldu!**

🔗 **Bağlantı:** `{tracking_url}`

📋 **Takip ID:** `{tracking_id}`

⚠️ **UYARI VE BİLGİLENDİRME:**

**Bu bağlantı ne yapar?**
• Tıklayan kişinin IP adresini toplar
• Tarayıcı ve işletim sistemi bilgisini alır
• Telefon numarası veya kamera gibi hassas bilgilere ERİŞMEZ

**Nasıl çalışır?**
1. Bu bağlantıyı istediğiniz kişiye gönderin
2. Kişi bağlantıya tıkladığında bir rıza formu görecek
3. Kişi izin verirse, bilgiler size gönderilecek
4. Kişi izin vermezse, hiçbir veri toplanmayacak

**Yasal Sorumluluk:**
• Bu bağlantıyı yalnızca izin verilen kişilerle paylaşın
• Kötüye kullanım durumunda sorumluluk size aittir
• KVKK ve diğer veri koruma yasalarına uygun hareket edin

Toplanan verileri görmek için /bilgilerim komutunu kullanın.
            """
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Bağlantı oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Web sunucusu bağlantı hatası: {e}")
        await update.message.reply_text(
            "❌ Web sunucusuna bağlanılamadı. Lütfen daha sonra tekrar deneyin."
        )
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        await update.message.reply_text(
            "❌ Beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin."
        )

async def get_my_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kullanıcının toplanan verilerini göster"""
    user_id = update.effective_user.id
    
    try:
        # Web sunucusundan kullanıcının verilerini al
        response = requests.get(
            f"{WEB_SERVER_URL}/api/get_collected_data/{user_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if not data:
                await update.message.reply_text(
                    "📊 Henüz hiç veri toplanmamış.\n\n"
                    "Yeni bir takip bağlantısı oluşturmak için /link_olustur komutunu kullanın."
                )
                return
            
            message = "📊 **Toplanan Veriler:**\n\n"
            
            for link_data in data:
                tracking_id = link_data['tracking_id']
                collected_data = link_data['collected_data']
                
                message += f"🔗 **Takip ID:** `{tracking_id}`\n"
                message += f"📈 **Toplam Tıklanma:** {len(collected_data)}\n\n"
                
                if collected_data:
                    message += "**Toplanan Bilgiler:**\n"
                    for i, data_entry in enumerate(collected_data, 1):
                        ip = data_entry['ip_address']
                        user_agent = data_entry['user_agent']
                        message += f"**{i}.** IP: `{ip}`\n"
                        message += f"   Cihaz: `{user_agent[:50]}...`\n\n"
                else:
                    message += "Henüz bu bağlantıya tıklanmamış.\n\n"
                
                message += "─" * 30 + "\n\n"
            
            # Telegram mesaj uzunluk sınırı nedeniyle böl
            if len(message) > 4000:
                parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
                for part in parts:
                    await update.message.reply_text(part, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
                
        else:
            await update.message.reply_text(
                "❌ Veriler alınırken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Web sunucusu bağlantı hatası: {e}")
        await update.message.reply_text(
            "❌ Web sunucusuna bağlanılamadı. Lütfen daha sonra tekrar deneyin."
        )
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        await update.message.reply_text(
            "❌ Beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yardım komutu"""
    help_text = """
🤖 **Bilgi Toplama Botu - Yardım**

**Kullanılabilir Komutlar:**

/start - Botu başlat ve hoş geldin mesajını gör
/link_olustur - Yeni bir takip bağlantısı oluştur
/bilgilerim - Toplanan verileri görüntüle
/help - Bu yardım menüsünü göster

**Bot Nasıl Çalışır?**

1. `/link_olustur` komutuyla bir takip bağlantısı oluşturun
2. Bu bağlantıyı istediğiniz kişiye gönderin
3. Kişi bağlantıya tıkladığında rıza formu görecek
4. Kişi izin verirse, IP adresi ve tarayıcı bilgisi toplanır
5. Toplanan bilgiler size gönderilir
6. `/bilgilerim` komutuyla toplanan verileri görüntüleyebilirsiniz

**Güvenlik ve Gizlilik:**

• Yalnızca IP adresi ve tarayıcı bilgisi toplanır
• Telefon numarası, kamera veya kişisel dosyalara erişim YOKTUR
• Kullanıcının açık rızası olmadan veri toplanmaz
• Yasal sorumluluk kullanıcıya aittir

**Destek:**
Herhangi bir sorun yaşarsanız, bot geliştiricisi ile iletişime geçin.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Bot'u başlat"""
    # Bot token'ını buraya girin (gerçek kullanımda environment variable kullanın)
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ HATA: Bot token'ı ayarlanmamış!")
        print("Bot token'ınızı telegram_bot.py dosyasındaki BOT_TOKEN değişkenine girin.")
        print("Bot token almak için @BotFather'a mesaj gönderin.")
        return
    
    # Application oluştur
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Komut handler'larını ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("link_olustur", create_link))
    application.add_handler(CommandHandler("bilgilerim", get_my_data))
    application.add_handler(CommandHandler("help", help_command))
    
    # Bot'u başlat
    print("🤖 Bot başlatılıyor...")
    print("Web sunucusunun çalıştığından emin olun!")
    print("Durdurmak için Ctrl+C tuşlarına basın.")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()


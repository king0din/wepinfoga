from flask import Blueprint, request, render_template_string, jsonify, redirect, url_for
from src.models.tracking import db, TrackingLink, CollectedData
import requests
import os

tracking_bp = Blueprint('tracking', __name__)

# Rıza formu HTML template'i
CONSENT_FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bilgi Toplama Rızası</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .warning {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .info {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .buttons {
            text-align: center;
            margin-top: 30px;
        }
        .btn {
            padding: 12px 30px;
            margin: 0 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .btn-accept {
            background-color: #28a745;
            color: white;
        }
        .btn-decline {
            background-color: #dc3545;
            color: white;
        }
        .btn:hover {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔒 Bilgi Toplama Rızası</h2>
        
        <div class="warning">
            <strong>⚠️ DİKKAT:</strong> Bu bağlantı, cihazınızdan belirli bilgileri toplayacaktır.
        </div>
        
        <div class="info">
            <h3>Toplanacak Bilgiler:</h3>
            <ul>
                <li><strong>IP Adresi:</strong> Cihazınızın internet bağlantı adresi</li>
                <li><strong>Tarayıcı Bilgisi:</strong> Kullandığınız tarayıcı ve işletim sistemi bilgisi</li>
            </ul>
            
            <h3>Toplanmayacak Bilgiler:</h3>
            <ul>
                <li>❌ Telefon numaranız</li>
                <li>❌ Kameradan görüntü</li>
                <li>❌ Kişisel dosyalarınız</li>
                <li>❌ Şifreleriniz</li>
            </ul>
            
            <p><strong>Bu bilgiler, bağlantıyı oluşturan kullanıcıya gönderilecektir.</strong></p>
        </div>
        
        <p>Bu bilgilerin toplanmasına ve paylaşılmasına izin veriyor musunuz?</p>
        
        <div class="buttons">
            <form method="POST" action="/collect_data" style="display: inline;">
                <input type="hidden" name="tracking_id" value="{{ tracking_id }}">
                <input type="hidden" name="sender_id" value="{{ sender_id }}">
                <input type="hidden" name="consent" value="true">
                <button type="submit" class="btn btn-accept">✅ Evet, İzin Veriyorum</button>
            </form>
            
            <form method="POST" action="/collect_data" style="display: inline;">
                <input type="hidden" name="tracking_id" value="{{ tracking_id }}">
                <input type="hidden" name="sender_id" value="{{ sender_id }}">
                <input type="hidden" name="consent" value="false">
                <button type="submit" class="btn btn-decline">❌ Hayır, İzin Vermiyorum</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teşekkürler</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
            text-align: center;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>✅ Teşekkürler!</h2>
        <div class="success">
            {{ message }}
        </div>
    </div>
</body>
</html>
"""

@tracking_bp.route('/track')
def track():
    """Takip bağlantısına tıklandığında rıza formunu göster"""
    tracking_id = request.args.get('tracking_id')
    sender_id = request.args.get('sender_id')
    
    if not tracking_id or not sender_id:
        return "Geçersiz bağlantı parametreleri", 400
    
    # Tracking ID'nin geçerli olup olmadığını kontrol et
    link = TrackingLink.query.filter_by(tracking_id=tracking_id).first()
    if not link:
        return "Geçersiz takip bağlantısı", 404
    
    return render_template_string(CONSENT_FORM_TEMPLATE, 
                                tracking_id=tracking_id, 
                                sender_id=sender_id)

@tracking_bp.route('/collect_data', methods=['POST'])
def collect_data():
    """Rıza formundan gelen verileri işle"""
    tracking_id = request.form.get('tracking_id')
    sender_id = request.form.get('sender_id')
    consent = request.form.get('consent') == 'true'
    
    if not tracking_id or not sender_id:
        return "Geçersiz form verileri", 400
    
    # Tracking ID'nin geçerli olup olmadığını kontrol et
    link = TrackingLink.query.filter_by(tracking_id=tracking_id).first()
    if not link:
        return "Geçersiz takip bağlantısı", 404
    
    if consent:
        # Kullanıcı rıza verdi, bilgileri topla
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'Bilinmiyor')
        
        # Veritabanına kaydet
        collected_data = CollectedData(
            link_id=link.id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(collected_data)
        db.session.commit()
        
        # Bot'a bildirim gönder (şimdilik placeholder)
        # TODO: Bot API endpoint'ini çağır
        try:
            # Bot bildirim endpoint'i (daha sonra implement edilecek)
            bot_notification_data = {
                'tracking_id': tracking_id,
                'sender_telegram_id': link.sender_telegram_id,
                'ip_address': ip_address,
                'user_agent': user_agent
            }
            # requests.post('http://localhost:6000/notify_collected_data', json=bot_notification_data)
        except Exception as e:
            print(f"Bot bildirim hatası: {e}")
        
        message = "Bilgileriniz başarıyla toplandı ve bağlantıyı oluşturan kullanıcıya gönderildi."
    else:
        # Kullanıcı rıza vermedi
        message = "Bilgi toplama işlemi iptal edildi. Hiçbir veri toplanmadı."
    
    return render_template_string(SUCCESS_TEMPLATE, message=message)

@tracking_bp.route('/api/create_link', methods=['POST'])
def create_link():
    """Bot için yeni takip bağlantısı oluştur"""
    data = request.get_json()
    sender_telegram_id = data.get('sender_telegram_id')
    
    if not sender_telegram_id:
        return jsonify({'error': 'sender_telegram_id gerekli'}), 400
    
    # Yeni takip bağlantısı oluştur
    link = TrackingLink(sender_telegram_id=sender_telegram_id)
    db.session.add(link)
    db.session.commit()
    
    # Tam URL oluştur
    base_url = request.host_url.rstrip('/')
    tracking_url = f"{base_url}/track?tracking_id={link.tracking_id}&sender_id={sender_telegram_id}"
    
    return jsonify({
        'tracking_id': link.tracking_id,
        'tracking_url': tracking_url
    })

@tracking_bp.route('/api/get_collected_data/<int:sender_telegram_id>')
def get_collected_data(sender_telegram_id):
    """Belirli bir kullanıcının toplanan verilerini getir"""
    links = TrackingLink.query.filter_by(sender_telegram_id=sender_telegram_id).all()
    
    result = []
    for link in links:
        link_data = link.to_dict()
        link_data['collected_data'] = [data.to_dict() for data in link.collected_data]
        result.append(link_data)
    
    return jsonify(result)


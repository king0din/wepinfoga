import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.tracking import db, TrackingLink, CollectedData
from src.routes.tracking import tracking_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# CORS'u etkinleştir
CORS(app)

app.register_blueprint(tracking_bp)

# Veritabanı ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Bilgi Toplama Botu Web Sunucusu Çalışıyor!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)


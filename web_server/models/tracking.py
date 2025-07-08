from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class TrackingLink(db.Model):
    __tablename__ = 'tracking_links'
    
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    sender_telegram_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişki
    collected_data = db.relationship('CollectedData', backref='link', lazy=True)

    def __repr__(self):
        return f'<TrackingLink {self.tracking_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tracking_id': self.tracking_id,
            'sender_telegram_id': self.sender_telegram_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CollectedData(db.Model):
    __tablename__ = 'collected_data'
    
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('tracking_links.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 için 45 karakter
    user_agent = db.Column(db.Text, nullable=False)
    collected_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CollectedData {self.ip_address}>'

    def to_dict(self):
        return {
            'id': self.id,
            'link_id': self.link_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None
        }


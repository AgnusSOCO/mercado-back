from src.models.user import db
from datetime import datetime

class Client(db.Model):
    """Client model for MercadoCredito"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    curp = db.Column(db.String(18), nullable=True)  # Mexican CURP
    rfc = db.Column(db.String(13), nullable=True)   # Mexican RFC
    address = db.Column(db.Text, nullable=True)
    
    # Promoter relationship
    promoter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status tracking
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with bank credentials
    bank_credentials = db.relationship('BankCredential', backref='client', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert client to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'curp': self.curp,
            'rfc': self.rfc,
            'address': self.address,
            'promoter_id': self.promoter_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'bank_count': len(self.bank_credentials)
        }
    
    def __repr__(self):
        return f'<Client {self.first_name} {self.last_name}>'


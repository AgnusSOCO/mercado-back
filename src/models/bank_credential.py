from src.models.user import db
from datetime import datetime
from cryptography.fernet import Fernet
import os
import base64

class BankCredential(db.Model):
    """Bank credential model with encryption for MercadoCredito"""
    __tablename__ = 'bank_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    
    # Encrypted fields
    username_encrypted = db.Column(db.Text, nullable=False)
    password_encrypted = db.Column(db.Text, nullable=False)
    
    # Additional bank-specific fields (encrypted)
    card_number_encrypted = db.Column(db.Text, nullable=True)
    account_number_encrypted = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_cipher():
        """Get encryption cipher"""
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # Generate a key for development (not recommended for production)
            key = Fernet.generate_key()
        else:
            # Ensure key is bytes
            if isinstance(key, str):
                key = key.encode()
        return Fernet(key)
    
    def set_username(self, username):
        """Encrypt and set username"""
        cipher = self.get_cipher()
        self.username_encrypted = cipher.encrypt(username.encode()).decode()
    
    def get_username(self):
        """Decrypt and get username"""
        cipher = self.get_cipher()
        return cipher.decrypt(self.username_encrypted.encode()).decode()
    
    def set_password(self, password):
        """Encrypt and set password"""
        cipher = self.get_cipher()
        self.password_encrypted = cipher.encrypt(password.encode()).decode()
    
    def get_password(self):
        """Decrypt and get password"""
        cipher = self.get_cipher()
        return cipher.decrypt(self.password_encrypted.encode()).decode()
    
    def set_card_number(self, card_number):
        """Encrypt and set card number"""
        if card_number:
            cipher = self.get_cipher()
            self.card_number_encrypted = cipher.encrypt(card_number.encode()).decode()
    
    def get_card_number(self):
        """Decrypt and get card number"""
        if self.card_number_encrypted:
            cipher = self.get_cipher()
            return cipher.decrypt(self.card_number_encrypted.encode()).decode()
        return None
    
    def set_account_number(self, account_number):
        """Encrypt and set account number"""
        if account_number:
            cipher = self.get_cipher()
            self.account_number_encrypted = cipher.encrypt(account_number.encode()).decode()
    
    def get_account_number(self):
        """Decrypt and get account number"""
        if self.account_number_encrypted:
            cipher = self.get_cipher()
            return cipher.decrypt(self.account_number_encrypted.encode()).decode()
        return None
    
    def to_dict(self, include_credentials=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'client_id': self.client_id,
            'bank_name': self.bank_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_credentials:
            # Only include decrypted credentials for authorized access
            data.update({
                'username': self.get_username(),
                'password': '***HIDDEN***',  # Never expose actual password
                'card_number': self.get_card_number(),
                'account_number': self.get_account_number()
            })
        
        return data
    
    def __repr__(self):
        return f'<BankCredential {self.bank_name} for Client {self.client_id}>'


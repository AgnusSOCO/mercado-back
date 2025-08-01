import os
import sys
from datetime import timedelta

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models
from src.models.user import db, User
from src.models.client import Client
from src.models.bank_credential import BankCredential

# Import routes
from src.routes.auth import auth_bp
from src.routes.clients import clients_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mercadocredito-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-mercadocredito')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production database (Railway PostgreSQL)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development database (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
# CORS configuration - update for production
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '').split(',')
if allowed_origins == ['']:
    CORS(app, origins=['*'])  # Development - allow all origins
else:
    CORS(app, origins=allowed_origins)  # Production - specific origins only

jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(clients_bp, url_prefix='/api/clients')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Initialize database
with app.app_context():
    db.init_app(app)
    db.create_all()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'service': 'MercadoCredito API',
        'version': '1.0.0',
        'cors': 'enabled',
        'database': 'connected',
        'features': ['auth', 'bank_credentials', 'admin_panel'],
        'timestamp': '2025-08-01T15:41:51.894659'
    }, 200

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


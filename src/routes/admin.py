from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.client import Client
from src.models.bank_credential import BankCredential
import os

admin_bp = Blueprint('admin', __name__)

def is_admin(user_email):
    """Check if user is admin"""
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    return user_email == admin_username

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login"""
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_username and password == admin_password:
            return jsonify({
                'message': 'Admin login exitoso',
                'admin': True,
                'username': username
            }), 200
        else:
            return jsonify({'error': 'Credenciales de admin inválidas'}), 401
            
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        total_users = User.query.count()
        total_clients = Client.query.count()
        total_credentials = BankCredential.query.count()
        
        # Recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_clients = Client.query.order_by(Client.created_at.desc()).limit(5).all()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_clients': total_clients,
                'total_credentials': total_credentials
            },
            'recent_activity': {
                'users': [user.to_dict() for user in recent_users],
                'clients': [client.to_dict() for client in recent_clients]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users (admin only)"""
    try:
        users = User.query.all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@admin_bp.route('/clients', methods=['GET'])
def get_all_clients():
    """Get all clients (admin only)"""
    try:
        clients = Client.query.all()
        
        return jsonify({
            'clients': [client.to_dict() for client in clients],
            'total': len(clients)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.client import Client
from src.models.bank_credential import BankCredential

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/', methods=['GET'])
@jwt_required()
def get_clients():
    """Get all clients for current promoter"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        clients = Client.query.filter_by(promoter_id=user_id).all()
        
        return jsonify({
            'clients': [client.to_dict() for client in clients],
            'total': len(clients)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@clients_bp.route('/', methods=['POST'])
@jwt_required()
def create_client():
    """Create a new client"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'phone_number', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Create new client
        client = Client(
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            phone_number=data['phone_number'].strip(),
            email=data['email'].strip().lower(),
            curp=data.get('curp', '').strip() if data.get('curp') else None,
            rfc=data.get('rfc', '').strip() if data.get('rfc') else None,
            address=data.get('address', '').strip() if data.get('address') else None,
            promoter_id=user_id
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente creado exitosamente',
            'client': client.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

@clients_bp.route('/<int:client_id>/bank-credentials', methods=['POST'])
@jwt_required()
def add_bank_credentials():
    """Add bank credentials for a client"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['bank_name', 'username', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Verify client belongs to current promoter
        client = Client.query.filter_by(id=client_id, promoter_id=user_id).first()
        if not client:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        # Create bank credential
        credential = BankCredential(
            client_id=client_id,
            bank_name=data['bank_name']
        )
        
        # Set encrypted fields
        credential.set_username(data['username'])
        credential.set_password(data['password'])
        
        if data.get('card_number'):
            credential.set_card_number(data['card_number'])
        
        if data.get('account_number'):
            credential.set_account_number(data['account_number'])
        
        db.session.add(credential)
        db.session.commit()
        
        return jsonify({
            'message': 'Credenciales bancarias agregadas exitosamente',
            'credential': credential.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

@clients_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client():
    """Get specific client details"""
    try:
        user_id = get_jwt_identity()
        
        client = Client.query.filter_by(id=client_id, promoter_id=user_id).first()
        if not client:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        return jsonify({'client': client.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


#  (create a new file: src/routes/banks.py)

from flask import Blueprint, jsonify

banks_bp = Blueprint('banks', __name__)

@banks_bp.route('/', methods=['GET'])
def get_banks():
    """Get list of available Mexican banks"""
    try:
        # List of major Mexican banks
        banks = [
            {
                'id': 'banamex',
                'name': 'Banamex',
                'full_name': 'Banco Nacional de México',
                'logo': '/assets/bank-logos/banamex.png',
                'fields': ['username', 'password']
            },
            {
                'id': 'bbva',
                'name': 'BBVA México',
                'full_name': 'BBVA México',
                'logo': '/assets/bank-logos/bbva.png',
                'fields': ['username', 'password']
            },
            {
                'id': 'banorte',
                'name': 'Banorte',
                'full_name': 'Banco Mercantil del Norte',
                'logo': '/assets/bank-logos/banorte.png',
                'fields': ['username', 'password']
            },
            {
                'id': 'santander',
                'name': 'Santander',
                'full_name': 'Banco Santander México',
                'logo': '/assets/bank-logos/santander.png',
                'fields': ['username', 'password']
            },
            {
                'id': 'hsbc',
                'name': 'HSBC',
                'full_name': 'HSBC México',
                'logo': '/assets/bank-logos/hsbc.png',
                'fields': ['username', 'password']
            },
            {
                'id': 'scotiabank',
                'name': 'Scotiabank',
                'full_name': 'Scotiabank México',
                'logo': '/assets/bank-logos/scotiabank.png',
                'fields': ['username', 'password']
            },
            {
                'id': 'azteca',
                'name': 'Banco Azteca',
                'full_name': 'Banco Azteca',
                'logo': '/assets/bank-logos/azteca.png',
                'fields': ['username', 'password', 'card_number']
            }
        ]
        
        return jsonify({
            'banks': banks,
            'total': len(banks)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


# Also add this to your main.py file in the blueprint registration section:
# from src.routes.banks import banks_bp
# app.register_blueprint(banks_bp, url_prefix='/api/banks')


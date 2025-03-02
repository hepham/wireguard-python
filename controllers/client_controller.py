from flask import Blueprint, request, jsonify, send_file
from services.client_service import ClientService
from utils.auth import require_auth
from utils.exceptions import InvalidRequestError, NotFoundError, InternalServerError
import tempfile
import os

client_bp = Blueprint('client', __name__)
service = ClientService()

@client_bp.route('/clients', methods=['POST'])
@require_auth(role='admin')
def create_client():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Client name is required'}), 400
    
    try:
        client = service.create_client(data['name'])
        config = service.generate_client_config(client)
        return jsonify({
            'name': client['name'],
            'config': config,
            'ip': client['ip']
        }), 201
    except InvalidRequestError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@client_bp.route('/clients', methods=['GET'])
@require_auth()
def list_clients():
    clients = service.client_model.load_clients()
    return jsonify([{
        'name': c['name'],
        'ip': c['ip'],
        'publicKey': c['public_key']
    } for c in clients])

@client_bp.route('/clients/<name>/config', methods=['GET'])
@require_auth()
def download_config(name):
    clients = service.client_model.load_clients()
    client = next((c for c in clients if c['name'] == name), None)
    if not client:
        raise NotFoundError(f'Client {name} not found')
    
    config = service.generate_client_config(client)
    
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(config)
        return send_file(
            path,
            as_attachment=True,
            download_name=f"{name}.conf"
        )
    finally:
        os.remove(path)
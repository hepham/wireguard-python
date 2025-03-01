from functools import wraps
from flask import request, jsonify
from config import Config

def require_auth(role: str = None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            api_key = request.headers.get('X-API-KEY')
            if not api_key:
                return jsonify({'error': 'API key missing'}), 401
                
            if api_key not in Config.API_KEYS.values():
                return jsonify({'error': 'Invalid API key'}), 401
                
            if role == 'admin' and api_key != Config.API_KEYS['admin']:
                return jsonify({'error': 'Insufficient privileges'}), 403
                
            return f(*args, **kwargs)
        return wrapped
    return decorator
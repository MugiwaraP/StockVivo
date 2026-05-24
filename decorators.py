from functools import wraps
from flask import request, jsonify
from auth_manager import auth

def requiere_rol(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return jsonify({'error': 'Token requerido'}), 401
            payload = auth.verificar_token(token)
            if not payload:
                return jsonify({'error': 'Token invalido o expirado'}), 401
            from models.usuario import Usuario
            usuario = Usuario.query.get(payload['id'])
            if not usuario or usuario.rol not in roles:
                return jsonify({'error': 'No tienes permiso para esta accion'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
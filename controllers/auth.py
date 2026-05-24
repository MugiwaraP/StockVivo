from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from extensions import db
from auth_manager import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/registro', methods=['POST'])
def registro():
    data = request.get_json()
    
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400

    nuevo = Usuario(
        nombre   = data['nombre'],
        email    = data['email'],
        password = auth.encriptar_password(data['password']),
        rol      = data.get('rol', 'vendedor')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not auth.verificar_password(data['password'], usuario.password):
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    token = auth.generar_token(usuario.id, usuario.email)
    return jsonify({
        'token': token,
        'usuario': usuario.to_dict()
    })
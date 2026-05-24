import os  # <-- ¡IMPORTANTE! Agrega esta importación arriba
from flask import Blueprint, redirect, url_for
from authlib.integrations.flask_client import OAuth
from models.usuario import Usuario
from extensions import db
from auth_manager import auth

# Blueprint
google_bp = Blueprint('google_auth', __name__)

# Instancia global de OAuth (sin pasar app)
oauth = OAuth()

# Configuración del proveedor Google
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),       
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@google_bp.route('/auth/google')
def google_login():
    redirect_uri = url_for('google_auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@google_bp.route('/auth/google/callback')
def google_callback():
    token = google.authorize_access_token()
    userinfo = token['userinfo']

    email = userinfo['email']
    nombre = userinfo['name']

    # Buscar usuario existente
    usuario = Usuario.query.filter_by(email=email).first()

    # Si no existe, crearlo
    if not usuario:
        usuario = Usuario(
            nombre=nombre,
            email=email,
            password=auth.encriptar_password('google_oauth'),
            rol='vendedor'
        )
        db.session.add(usuario)
        db.session.commit()

    # Generar JWT
    jwt_token = auth.generar_token(usuario.id, usuario.email)

    # Redirigir al frontend
    return redirect(
        f'/?token={jwt_token}'
        f'&nombre={nombre}'
        f'&rol={usuario.rol}'
        f'&id={usuario.id}'
    )
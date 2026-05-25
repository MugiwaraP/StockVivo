import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template
from flask_cors import CORS
from extensions import db

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Google OAuth
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')

# Inicializar base de datos
db.init_app(app)

# Importar OAuth y conectarlo con Flask
from controllers.google_auth import google_bp, oauth
oauth.init_app(app)

# Importar y registrar blueprints
with app.app_context():
    from models.producto import Producto
    from models.usuario import Usuario
    from models.movimiento import Movimiento
    from models.categoria import Categoria
    from controllers.productos import productos_bp
    from controllers.auth import auth_bp
    from controllers.movimientos import movimientos_bp
    from controllers.reportes import reportes_bp
    from controllers.google_auth import google_bp
    from controllers.categorias import categorias_bp
    app.register_blueprint(productos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(movimientos_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(google_bp)
    app.register_blueprint(categorias_bp)
    db.create_all()


# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Ejecutar aplicación Web
if __name__ == '__main__':
    app.run(debug=True)
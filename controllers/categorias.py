from flask import Blueprint, jsonify, request
from extensions import db
from models.categoria import Categoria
from decorators import requiere_rol

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias])

@categorias_bp.route('/api/categorias', methods=['POST'])
@requiere_rol('admin')
def crear_categoria():
    data = request.get_json()
    if Categoria.query.filter_by(nombre=data['nombre']).first():
        return jsonify({'error': 'La categoria ya existe'}), 400
    nueva = Categoria(nombre=data['nombre'])
    db.session.add(nueva)
    db.session.commit()
    return jsonify(nueva.to_dict()), 201

@categorias_bp.route('/api/categorias/<int:id>', methods=['DELETE'])
@requiere_rol('admin')
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'mensaje': 'Categoria eliminada'})
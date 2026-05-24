from flask import Blueprint, jsonify, request
from extensions import db
from models.categoria import Categoria

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias])

@categorias_bp.route('/api/categorias', methods=['POST'])
def crear_categoria():
    data = request.get_json()
    if Categoria.query.filter_by(nombre=data['nombre']).first():
        return jsonify({'error': 'La categoría ya existe'}), 400
    nueva = Categoria(nombre=data['nombre'])
    db.session.add(nueva)
    db.session.commit()
    return jsonify(nueva.to_dict()), 201

@categorias_bp.route('/api/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'mensaje': 'Categoría eliminada'})
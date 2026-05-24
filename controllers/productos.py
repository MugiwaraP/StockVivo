from flask import Blueprint, jsonify, request
from repositories.producto_repo import ProductoRepository
from decorators import requiere_rol

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = ProductoRepository.obtener_todos()
    return jsonify([p.to_dict() for p in productos])

@productos_bp.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = ProductoRepository.obtener_por_id(id)
    return jsonify(producto.to_dict())

@productos_bp.route('/api/productos', methods=['POST'])
@requiere_rol('admin')
def crear_producto():
    data = request.get_json()
    producto, alertas = ProductoRepository.crear(data)
    respuesta = producto.to_dict()
    respuesta['alertas'] = alertas
    return jsonify(respuesta), 201

@productos_bp.route('/api/productos/<int:id>', methods=['PUT'])
@requiere_rol('admin')
def actualizar_producto(id):
    data = request.get_json()
    producto, alertas = ProductoRepository.actualizar(id, data)
    respuesta = producto.to_dict()
    respuesta['alertas'] = alertas
    return jsonify(respuesta)

@productos_bp.route('/api/productos/<int:id>', methods=['DELETE'])
@requiere_rol('admin')
def eliminar_producto(id):
    ProductoRepository.eliminar(id)
    return jsonify({'mensaje': 'Producto eliminado'})
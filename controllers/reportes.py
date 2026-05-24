from flask import Blueprint, jsonify
from models.movimiento import Movimiento
from models.producto import Producto
from extensions import db
from sqlalchemy import func

reportes_bp = Blueprint('reportes', __name__)

# Productos con stock bajo
@reportes_bp.route('/api/reportes/stock-bajo', methods=['GET'])
def stock_bajo():
    productos = Producto.query.filter(Producto.cantidad <= Producto.stock_minimo).all()
    return jsonify([p.to_dict() for p in productos])

# Productos más vendidos
@reportes_bp.route('/api/reportes/mas-vendidos', methods=['GET'])
def mas_vendidos():
    resultados = db.session.query(
        Producto.nombre,
        func.sum(Movimiento.cantidad).label('total_vendido')
    ).join(Movimiento).filter(
        Movimiento.tipo == 'salida'
    ).group_by(Producto.id).order_by(
        func.sum(Movimiento.cantidad).desc()
    ).limit(10).all()

    return jsonify([
        {'producto': r.nombre, 'total_vendido': int(r.total_vendido)}
        for r in resultados
    ])

# Todos los movimientos
@reportes_bp.route('/api/reportes/movimientos', methods=['GET'])
def movimientos():
    movs = Movimiento.query.order_by(Movimiento.fecha.desc()).limit(50).all()
    return jsonify([m.to_dict() for m in movs])

# Resumen general
@reportes_bp.route('/api/reportes/resumen', methods=['GET'])
def resumen():
    total_productos = Producto.query.count()
    stock_bajo      = Producto.query.filter(Producto.cantidad <= Producto.stock_minimo).count()
    total_entradas  = db.session.query(func.sum(Movimiento.cantidad)).filter(Movimiento.tipo == 'entrada').scalar() or 0
    total_salidas   = db.session.query(func.sum(Movimiento.cantidad)).filter(Movimiento.tipo == 'salida').scalar() or 0
    valor_inventario = db.session.query(
        func.sum(Producto.cantidad * Producto.precio_compra)
    ).scalar() or 0

    return jsonify({
        'total_productos':  total_productos,
        'stock_bajo':       stock_bajo,
        'total_entradas':   int(total_entradas),
        'total_salidas':    int(total_salidas),
        'valor_inventario': round(float(valor_inventario), 2)
    })
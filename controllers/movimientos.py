from flask import Blueprint, jsonify, request
from repositories.movimiento_repo import MovimientoRepository

movimientos_bp = Blueprint('movimientos', __name__)

@movimientos_bp.route('/api/movimientos', methods=['GET'])
def obtener_movimientos():
    movimientos = MovimientoRepository.obtener_todos()
    return jsonify([m.to_dict() for m in movimientos])

@movimientos_bp.route('/api/movimientos', methods=['POST'])
def registrar_movimiento():
    data = request.get_json()
    movimiento, resultado = MovimientoRepository.registrar(data)
    if movimiento is None:
        return jsonify({'error': resultado}), 400
    respuesta = movimiento.to_dict()
    respuesta['alertas'] = resultado
    return jsonify(respuesta), 201
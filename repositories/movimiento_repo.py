from extensions import db
from models.movimiento import Movimiento
from models.producto import Producto
from observer import gestor

class MovimientoRepository:

    @staticmethod
    def obtener_todos():
        return Movimiento.query.order_by(Movimiento.fecha.desc()).all()

    @staticmethod
    def registrar(data):
        producto = Producto.query.get_or_404(data['producto_id'])
        cantidad = data['cantidad']
        tipo     = data['tipo']

        if tipo == 'entrada':
            producto.cantidad += cantidad
        elif tipo == 'salida':
            if producto.cantidad < cantidad:
                return None, 'Stock insuficiente'
            producto.cantidad -= cantidad

        movimiento = Movimiento(
            producto_id = producto.id,
            tipo        = tipo,
            cantidad    = cantidad,
            descripcion = data.get('descripcion', '')
        )
        db.session.add(movimiento)
        db.session.commit()
        alertas = gestor.notificar(producto)
        return movimiento, alertas
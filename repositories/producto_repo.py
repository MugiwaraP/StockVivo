from extensions import db
from models.producto import Producto
from observer import gestor

class ProductoRepository:

    @staticmethod
    def obtener_todos():
        return Producto.query.all()

    @staticmethod
    def obtener_por_id(id):
        return Producto.query.get_or_404(id)

    @staticmethod
    def crear(data):
        nuevo = Producto(
            nombre        = data['nombre'],
            descripcion   = data.get('descripcion', ''),
            cantidad      = data['cantidad'],
            precio_compra = data['precio_compra'],
            precio_venta  = data['precio_venta'],
            stock_minimo  = data.get('stock_minimo', 5),
            categoria_id  = data.get('categoria_id') or None
        )
        db.session.add(nuevo)
        db.session.commit()
        alertas = gestor.notificar(nuevo)
        return nuevo, alertas

    @staticmethod
    def actualizar(id, data):
        producto = Producto.query.get_or_404(id)
        producto.nombre        = data.get('nombre', producto.nombre)
        producto.descripcion   = data.get('descripcion', producto.descripcion)
        producto.cantidad      = data.get('cantidad', producto.cantidad)
        producto.precio_compra = data.get('precio_compra', producto.precio_compra)
        producto.precio_venta  = data.get('precio_venta', producto.precio_venta)
        producto.stock_minimo  = data.get('stock_minimo', producto.stock_minimo)
        producto.categoria_id  = data.get('categoria_id') or None
        db.session.commit()
        alertas = gestor.notificar(producto)
        return producto, alertas

    @staticmethod
    def eliminar(id):
        producto = Producto.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
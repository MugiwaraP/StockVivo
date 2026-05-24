from extensions import db
from datetime import datetime

class Movimiento(db.Model):
    __tablename__ = 'movimientos'

    id          = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tipo        = db.Column(db.String(10), nullable=False)  # 'entrada' o 'salida'
    cantidad    = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(255))
    fecha       = db.Column(db.DateTime, default=datetime.utcnow)

    producto = db.relationship('Producto', backref='movimientos')

    def to_dict(self):
        return {
            'id':           self.id,
            'producto_id':  self.producto_id,
            'producto':     self.producto.nombre,
            'tipo':         self.tipo,
            'cantidad':     self.cantidad,
            'descripcion':  self.descripcion,
            'fecha':        self.fecha.strftime('%Y-%m-%d %H:%M')
        }
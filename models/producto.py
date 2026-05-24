from extensions import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id            = db.Column(db.Integer, primary_key=True)
    nombre        = db.Column(db.String(100), nullable=False)
    descripcion   = db.Column(db.String(255))
    cantidad      = db.Column(db.Integer, default=0)
    precio_compra = db.Column(db.Float, nullable=False)
    precio_venta  = db.Column(db.Float, nullable=False)
    stock_minimo  = db.Column(db.Integer, default=5)
    categoria_id  = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)

    def to_dict(self):
        return {
            'id':            self.id,
            'nombre':        self.nombre,
            'descripcion':   self.descripcion,
            'cantidad':      self.cantidad,
            'precio_compra': self.precio_compra,
            'precio_venta':  self.precio_venta,
            'stock_minimo':  self.stock_minimo,
            'categoria_id':  self.categoria_id,
            'categoria':     self.categoria.nombre if self.categoria else 'Sin categoría'
        }
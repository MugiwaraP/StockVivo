from extensions import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id     = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    productos = db.relationship('Producto', backref='categoria', lazy=True)

    def to_dict(self):
        return {
            'id':     self.id,
            'nombre': self.nombre
        }
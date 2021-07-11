from sqlalchemy.orm import relationship
from tienda import db ,bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))





class Usuarios(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100))
    email= db.Column(db.String(100),unique=True)
    telefono=db.Column(db.Integer(),nullable=True)
    contrasenia=db.Column(db.String(100))
    cantidad_pedidos=db.Column(db.Integer(),nullable=True)
    admin = db.Column(db.Boolean, default=False)
    chofer= db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'Email:{self.email}'
"""

class EntregasChoferes(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    id_chofer=db.Column(db.Integer(),db.ForeignKey('usuarios.id'))
    chofer=relationship("Usuarios")
    id_cliente=db.Column(db.Integer(),db.ForeignKey('usuarios.id'))
    cliente=relationship("Usuarios")
    id_factura=db.Column(db.Integer(),nullable=False)
    condicion=db.Column(db.String(length=50))
"""

class Pedidos(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    id_cliente=db.Column(db.Integer(),db.ForeignKey('usuarios.id'),nullable=False)
    cliente=relationship("Usuarios")
    id_producto=db.Column(db.Integer(),db.ForeignKey('productos.id'),nullable=False)
    producto=relationship("Productos")
    id_factura=db.Column(db.Integer(),nullable=False)
    precio=db.Column(db.Float(),nullable=False)
    cantidad=db.Column(db.Integer(),nullable=False)
    
class Productos(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    nombre=db.Column(db.String(length=500),nullable=False,unique=True)
    categoria=db.Column(db.String(length=100),nullable=False)
    precio=db.Column(db.Float(),nullable=False)
    stock=db.Column(db.Integer(),nullable=False)
    oferta=db.Column(db.Integer(),nullable=True)
    precioFinal=db.Column(db.Float(),nullable=False)
    imagen=db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'Producto {self.nombre}'

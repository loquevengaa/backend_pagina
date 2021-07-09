
import random
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import relationship
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='j4hfb32dAKNDs9jf56bsa8dljfña@uNUKjBbKJHG78'
db=SQLAlchemy(app)


class Productos(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    nombre=db.Column(db.String(length=100),nullable=False,unique=True)
    categoria=db.Column(db.String(length=100),nullable=False)
    precio=db.Column(db.Float(),nullable=False)
    stock=db.Column(db.Integer(),nullable=False)
    oferta=db.Column(db.Integer(),nullable=True)
    precioFinal=db.Column(db.Float(),nullable=False)

    def __repr__(self):
        return f'Producto {self.name}'


class Usuarios(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100))
    email= db.Column(db.String(100),unique=True)
    telefono=db.Column(db.Integer(),nullable=True)
    contrasenia=db.Column(db.String(100))
    cantidad_pedidos=db.Column(db.Integer(),nullable=True)

    def __repr__(self):
        return f'Email:{self.email}'


class Pedidos(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    id_cliente=db.Column(db.Integer(),db.ForeignKey('usuarios.id'),nullable=False)
    cliente=relationship("Usuarios")
    id_producto=db.Column(db.Integer(),db.ForeignKey('productos.id'),nullable=False)
    producto=relationship("Productos")
    id_factura=db.Column(db.Integer(),nullable=False)
    precio=db.Column(db.Float(),nullable=False)
    cantidad=db.Column(db.Integer(),nullable=False)
    


class Choferes(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    nombre= db.Column(db.String(length=100))
    email= db.Column(db.String(length=100),unique=True)
    telefono=db.Column(db.Integer(),nullable=True)
    contrasenia=db.Column(db.String(length=100))


class EntregasChoferes(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    id_chofer=db.Column(db.Integer(),db.ForeignKey('choferes.id'))
    chofer=relationship("Choferes")
    id_cliente=db.Column(db.Integer(),db.ForeignKey('usuarios.id'))
    cliente=relationship("Usuarios")
    id_factura=db.Column(db.Integer(),nullable=False)
    condicion=db.Column(db.String(length=50))

print("se creo base de datos")
db.create_all()


"""

for i in range(5):
    nombre='Usuario'+str(i+1)
    email=nombre+'@gmail.com'
    telefono=random.randint(2230000000,2239999999)
    contrasenia='holapaola'
    cantidad_pedidos=0
    usuarios =Usuarios(nombre=nombre,email=email,telefono=telefono,contrasenia=contrasenia,cantidad_pedidos=cantidad_pedidos)
    db.session.add(usuarios)
    db.session.commit()

    """
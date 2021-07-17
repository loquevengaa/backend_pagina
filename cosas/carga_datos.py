
import random
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import relationship
import pandas as pd


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='j4hfb32dAKNDs9jf56bsa8dljfña@uNUKjBbKJHG78'
db=SQLAlchemy(app)


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
    nombre=db.Column(db.String(length=100),nullable=False,unique=True)
    categoria=db.Column(db.String(length=100),nullable=False)
    precio=db.Column(db.Float(),nullable=False)
    stock=db.Column(db.Integer(),nullable=False)
    oferta=db.Column(db.Integer(),nullable=True)
    precioFinal=db.Column(db.Float(),nullable=False)
    imagen=db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'Producto {self.name}'


db.drop_all()
db.create_all()


df=pd.read_excel('tienda\productos.xlsx')

for i in range(len(df)):
    producto=Productos(nombre=df['nombre'][i],categoria=df['categoria'][i],
                       precio=df['precio'][i],stock=int(df['stock'][i]),oferta=int(df['oferta'][i]),
                       precioFinal=df['precio'][i],imagen=df['imagen'][i])
    db.session.add(producto)
    db.session.commit()
    



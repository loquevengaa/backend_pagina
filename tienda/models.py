from tienda import db ,bcrypt,login_manager
from flask_login import UserMixin
import sqlalchemy.types as types
import pandas as pd
import json


@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

def meFijoStock():
    combos=Combos.query.all()

    for combo in combos:
        cantidades=[]
        datos=json.loads(combo.datos_combo)
        for producto in datos:
            pid=producto['id']
            pcant=producto['cantidad']
            stock_producto=Productos.query.get(pid).stock
            cantidades.append(stock_producto//pcant)
        combo.stock=min(cantidades)   

    db.session.commit()
        
class Usuarios(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100))
    email= db.Column(db.String(100),unique=True)
    telefono=db.Column(db.Integer(),nullable=True)
    contrasenia_cifrada=db.Column(db.String(100))
    cantidad_pedidos=db.Column(db.Integer(),nullable=True)
    admin = db.Column(db.Boolean, default=False)
    chofer = db.Column(db.Boolean, default=False)
    pedidos=db.relationship('Pedidos',backref='chofer_asociado')
    
    @property
    def contrasenia(self):
        return self.contrasenia
    
    @contrasenia.setter
    def contrasenia(self,plain_text_password):
        self.contrasenia_cifrada=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_contrasenia(self,contrasenia_ingresada):
        return bcrypt.check_password_hash(self.contrasenia_cifrada,contrasenia_ingresada)
      
    def __repr__(self):
        return f'Email:{self.email}'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        return self.admin

    def is_chofer(self):
        return self.chofer



class Pedidos(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    direccion=db.Column(db.String(length=200),nullable=False)
    nombre=db.Column(db.String(length=100),nullable=False)
    telefono=db.Column(db.Integer(),nullable=True)
    email= db.Column(db.String(100))
    fechaHoraPedido=db.Column(db.String(100))
    fechaHoraEntrega=db.Column(db.String(100))
    estado=db.Column(db.String(length=50),nullable=False) #estado de envio
    chofer=db.Column(db.Integer(),db.ForeignKey('usuarios.id'))
    descripcion=db.Column(db.String(length=500),nullable=False)
    formaPago=db.Column(db.String(length=100),nullable=False)
    estadoPago=db.Column(db.String(length=100),nullable=False)
    datos_pedido= db.Column(types.JSON(),nullable=False)
    costo=db.Column(db.Float(),nullable=False) 
    #costo=db.relationship('Costo_pedido',backref='pedido')
"""
class Costo_pedido(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    id_pedido=db.Column(db.Integer(),db.ForeignKey('pedidos.id'))
    costo=db.Column(db.Float(),nullable=False) 
    def __repr__(self):
        return f'{self.costo}'
"""
    
class Productos(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    nombre=db.Column(db.String(length=500),nullable=False)
    categoria=db.Column(db.String(length=100),nullable=False)
    precio=db.Column(db.Float(),nullable=False)
    stock=db.Column(db.Integer(),nullable=False)
    oferta=db.Column(db.Integer(),nullable=True)
    precioFinal=db.Column(db.Float(),nullable=False)
    imagen=db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'{self.nombre}'

class Combos(db.Model):
    id=db.Column(db.Integer(),primary_key=True) 
    nombre=db.Column(db.String(length=500),nullable=False)
    datos_combo= db.Column(types.JSON(),nullable=False)  # id del producto y cantidad
    precioFinal=db.Column(db.Float(),nullable=False)
    stock=db.Column(db.Integer(),nullable=False)
    imagen=db.Column(db.String(),nullable=False)
    
"""
db.drop_all()
db.create_all()

df = pd.read_excel("tienda\cosas.xlsx")
for i in range(len(df)):
    producto=Productos(nombre=str(df['nombre'][i]).title(),
                       categoria=str(df['categoria'][i]).title(),
                       precio=int(df['precio'][i]),
                       stock=int(df['stock'][i]),
                       oferta=int(df['oferta'][i]),
                       precioFinal=int(df['precioFinal'][i]),
                       imagen=df['imagen'][i])
    db.session.add(producto)
    db.session.commit()

usuario=Usuarios(nombre="a",
                 email="tincho@gmail.com" ,
                 telefono=123456,
                 contrasenia="adminadmin",
                 cantidad_pedidos=0,
                 admin=True,
                 chofer=False
                 )


db.session.add(usuario)
db.session.commit()

chofer=Usuarios(nombre="chofer",
                 email="nico@gmail.com" ,
                 telefono=12363456,
                 contrasenia="adminadmin",
                 cantidad_pedidos=0,
                 admin=False,
                 chofer=True
                 )
db.session.add(chofer)
db.session.commit()
"""


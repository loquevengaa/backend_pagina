from tienda import db ,bcrypt,login_manager
from flask_login import UserMixin
import sqlalchemy.types as types
import pandas as pd

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))


class Usuarios(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100))
    email= db.Column(db.String(100),unique=True)
    telefono=db.Column(db.Integer(),nullable=True)
    contrasenia_cifrada=db.Column(db.String(100))
    cantidad_pedidos=db.Column(db.Integer(),nullable=True)
    admin = db.Column(db.Boolean, default=False)
    chofer = db.Column(db.Boolean, default=False)
    
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
    direccion=db.Column(db.String(length=100),nullable=False)
    nombre=db.Column(db.String(length=100),nullable=False)
    telefono=db.Column(db.Integer(),nullable=True)
    email= db.Column(db.String(100))
    fechaHoraPedido=db.Column(db.String(100))
    fechaHoraEntrega=db.Column(db.String(100))
    estado=db.Column(db.String(length=50),nullable=False)
    chofer=db.Column(db.Integer())
    descripcion=db.Column(db.String(length=500),nullable=False)
    formaPago=db.Column(db.String(length=100),nullable=False)
    datos_pedido= db.Column(types.JSON())

    
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
    

"""
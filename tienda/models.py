from sqlalchemy.orm import relationship
from tienda import db ,bcrypt,login_manager
from flask_login import UserMixin

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

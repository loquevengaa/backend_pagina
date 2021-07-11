from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import EqualTo, Length,EqualTo,Email,DataRequired,ValidationError
from tienda.models import Usuarios

 
class RegisterForm(FlaskForm):

    def validate_email(self,email_to_check):
        email=Usuarios.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('El correo ya existe')
    def validate_telefono(self,telefono_to_check):
        telefono=Usuarios.query.filter_by(telefono=telefono_to_check.data).first()
        if telefono:
            raise ValidationError('El numero ya existe')
            
    nombre =StringField(label='Nombre',validators=[Length(min= 2, max= 50),DataRequired()])
    email =StringField(label='Correo',validators=[Email(),DataRequired()])
    telefono=IntegerField(label='Telefono',validators=[Length(min=7),DataRequired()])
    contrasenia=PasswordField(label='Contraseña',validators=[Length(min=6),DataRequired()])
    contrasenia2=PasswordField(label='Repita Contraseña',validators=[EqualTo('contrasenia'),DataRequired()])
    submit=SubmitField(label='Registrarme') 


class LoginForm(FlaskForm):
    email =StringField(label='Correo',validators=[Email(),DataRequired()])
    contrasenia=PasswordField(label='Contraseña',validators=[Length(min=6),DataRequired()])
    submit=SubmitField(label='Ingresar') 




class ComprarProductoForm(FlaskForm):
    id=IntegerField(label='id')
    cantidad=IntegerField(label='cantidad',validators=[DataRequired()])
    submit=SubmitField(label='Agregar al carrito')






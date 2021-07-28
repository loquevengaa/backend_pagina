from flask_wtf import FlaskForm 
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import  Length,Email,DataRequired
from flask_wtf.recaptcha import RecaptchaField


class PedidoForm(FlaskForm):
    direccion=StringField(label='Direccion',validators=[Length(min= 2, max= 50),DataRequired()])
    nombre =StringField(label='Nombre',validators=[Length(min= 2, max= 50),DataRequired()])
    telefono=IntegerField(label='Telefono',validators=[DataRequired()])
    email =StringField(label='Correo',validators=[Email(),DataRequired()])
    descripcion=StringField(label='Descripcion',validators=[DataRequired()]) 
    medioDePago=StringField(label='Medio de Pago',validators=[Length(min= 2, max= 50),DataRequired()])
   # recaptcha = RecaptchaField()
    submit=SubmitField(label='Comfirmar') 
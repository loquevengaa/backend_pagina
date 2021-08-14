from flask_wtf import FlaskForm 
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import  Length,Email,DataRequired
from flask_wtf.recaptcha import RecaptchaField


class PedidoForm(FlaskForm):
    direccion=StringField(label='Direccion',validators=[Length(min= 2, max= 50),DataRequired()])
    nombre =StringField(label='Nombre',validators=[Length(min= 2, max= 50),DataRequired()])
    email =StringField(label='Correo',validators=[Email(),DataRequired()])
    descripcion=StringField(label='Descripcion',validators=[DataRequired()]) 
    submit=SubmitField(label='Comfirmar') 
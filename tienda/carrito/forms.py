from flask_wtf import FlaskForm , RecaptchaField
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import  Length,Email,DataRequired




class PedidoForm(FlaskForm):
    direccion=StringField(label='Direccion',validators=[Length(min= 2, max= 50),DataRequired()])
    nombre =StringField(label='Nombre',validators=[Length(min= 2, max= 50),DataRequired()])
    telefono=IntegerField(label='Telefono',validators=[DataRequired()])
    mail =StringField(label='Correo',validators=[Email(),DataRequired()])
    descripcion=StringField(label='Descripcion',validators=DataRequired()) 
    medioDePago=StringField(label='Medio de Pago',validators=[Length(min= 2, max= 50),DataRequired()])
    recaptcha = RecaptchaField()
    submit=SubmitField(label='Comfirmar') 
from flask_wtf import FlaskForm 
from wtforms import SubmitField,IntegerField
from wtforms.validators import DataRequired



class ComprarProductoForm(FlaskForm):
    id=IntegerField(label='id')
    cantidad=IntegerField(label='cantidad',validators=[DataRequired()])
    submit=SubmitField(label='Agregar al carrito')






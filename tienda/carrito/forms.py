from flask_wtf import FlaskForm 
from wtforms import SubmitField,IntegerField,HiddenField
from wtforms.validators import NumberRange,Required




class FormCarrito(FlaskForm):
    id = HiddenField()
    cantidad = IntegerField('Cantidad', default=1,
                            validators=[NumberRange(min=1,
                                                    message="Debe ser un núme"
                                                            "ro positivo"),
                                        Required("Tienes que introducir el "
                                                 "dato")])
    submit = SubmitField('Aceptar')


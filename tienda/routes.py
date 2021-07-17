from tienda import app,db
from tienda.models import Productos
from tienda.carrito.forms import FormCarrito
from flask import render_template

@app.route('/')
@app.route('/home',methods=['GET','POST'])#aca se muestran lo productos
def tienda_page():
	agregar_al_carrito=FormCarrito()
	items= Productos.query.all()
	return render_template('home.html',items=items,carrito=agregar_al_carrito,cat='null')



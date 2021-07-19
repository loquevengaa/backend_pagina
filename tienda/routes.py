from tienda import app,db
from tienda.models import Productos
from tienda.carrito.forms import FormCarrito
from flask import render_template, request, redirect

@app.route('/')
@app.route('/home',methods=['POST','GET'])#aca se muestran lo productos
def tienda_page():
	agregar_al_carrito=FormCarrito()
	items= Productos.query.all()
	return render_template('home.html',items=items,carrito=agregar_al_carrito)


@app.route('/categoria/<categoria>',methods=['POST','GET'])#aca se muestran lo productos
def categorias(categoria):
	agregar_al_carrito=FormCarrito()
	items= Productos.query.filter_by(categoria=categoria)


	if request.method=='POST':
		indice = int(request.form['indice'])
		cantidad = int(request.form['cantidad'])
		print(indice)
		print(cantidad)
		
		return redirect(request.referrer)


	return render_template('home.html',items=items,carrito=agregar_al_carrito)



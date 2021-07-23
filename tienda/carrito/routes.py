from tienda.routes import tienda_page
from tienda import app,db
from flask import render_template,redirect,url_for,request, make_response
from flask_login import current_user,login_required
from tienda.models import Productos

import json

@app.route('/carrito/add',methods=['GET','POST'])
def carrito_add():

	if request.method=='POST':
		indice = (request.form['indice'])
		print(indice)
		cantidad = int(request.form['cantidad'])
		art=Productos.query.get(indice)
		print(art)
		if art is None:
			print("Articulo no existe")
			return redirect(request.referrer) #No hay articulo		
		if art.stock <= 0:
			print("No stock")
			return redirect(request.referrer) #No hay stock
		try:
			datos = json.loads(request.cookies.get("carrito"))	 #str(current_user.get_id()			
		except:
			datos=[]
		actualizar = False
		for dato in datos:
			if dato["id"] == indice:
				dato["cantidad"] +=cantidad
				actualizar = True
		if not actualizar:
			datos.append({"id": indice,"cantidad":cantidad})
			print(datos)					 						 
		resp=make_response(redirect(request.referrer))
		resp.set_cookie("carrito", json.dumps(datos)) #str(current_user.get_id()
		return resp
	return redirect(request.referrer)






@app.route('/carrito')
def carrito():
	try:
		datos = json.loads(request.cookies.get("carrito"))
	except:
		datos = []
	imagen=[]
	articulos=[]
	cantidades=[]
	total=[]
	totalfinal=0
	for articulo in datos:
		try:
			art = Productos.query.get(articulo["id"])
			imagen.append(art.imagen)
			articulos.append(art.nombre)
			cantidades.append(articulo["cantidad"])
			aux = art.precioFinal*articulo["cantidad"]
			total.append(aux)
			totalfinal=totalfinal+aux
		except:
			pass
		
	articulos=zip(imagen,articulos,cantidades,total)
	return render_template("carrito.html",articulos=articulos,totalfinal=totalfinal)



@app.route('/carrito_delete/<id>')
def carrito_delete(id):
	try:
		datos = json.loads(request.cookies.get("carrito"))
	except:
		datos = []
	new_datos=[]
	for dato in datos:
		if dato["id"]!=id:
			new_datos.append(dato)
	resp = make_response(redirect(url_for('carrito')))
	resp.set_cookie("carrito",json.dumps(new_datos))
	return resp


@app.route('/pedido')
@login_required
def pedido():
	try:
		datos = json.loads(request.cookies.get("carrito"))
	except:
		datos = []
	total=0
	for articulo in datos:
		total=total+Productos.query.get(articulo["id"]).precio_final()*articulo["cantidad"]
		Productos.query.get(articulo["id"]).stock-=articulo["cantidad"]
		db.session.commit()
	resp = make_response(render_template("pedido.html",total=total))
	resp.set_cookie("carrito","",expires=0)
	return resp






@app.context_processor
def contar_carrito():
	try:
		if request.cookies.get("carrito") is None:
			return {'num_articulos': 0}
		else:
			#print("no se rompio")
			datos = json.loads(request.cookies.get("carrito"))
			#print(datos)
			return {'num_articulos': len(datos)}
	except:
			#print("se rompio")
			return {'num_articulos': 0}
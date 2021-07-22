from tienda import app,db
from flask import render_template,redirect,url_for,request, make_response
from flask_login import current_user,login_required
from tienda.models import Productos


import json

@app.route('/carrito/add',methods=['GET','POST'])
@login_required
def carrito_add():
	print(current_user.nombre)
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
			datos = json.loads(request.cookies.get(str(current_user.get_id())))					
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
		resp=make_response(redirect(url_for('tienda_page')))
		resp.set_cookie(str(current_user.get_id()), json.dumps(datos))
		return resp
	return redirect(request.referrer)





@app.route('/carrito')
def carrito():
	try:
		datos = json.loads(request.cookies.get(str(current_user.id)))
	except:
		datos = []
	articulos=[]
	cantidades=[]
	total=0
	for articulo in datos:
		articulos.append(Productos.query.get(articulo["id"]))
		cantidades.append(articulo["cantidad"])
		total=total+Productos.query.get(articulo["id"]).precio_final()*articulo["cantidad"]
	articulos=zip(articulos,cantidades)
	return render_template("carrito.html",articulos=articulos,total=total)



app.route('/carrito_delete/<id>')
def carrito_delete(id):
	try:
		datos = json.loads(request.cookies.get(str(current_user.id)))
	except:
		datos = []
	new_datos=[]
	for dato in datos:
		if dato["id"]!=id:
			new_datos.append(dato)
	resp = make_response(redirect(url_for('carrito')))
	resp.set_cookie(str(current_user.id),json.dumps(new_datos))
	return resp


@app.route('/pedido')
@login_required
def pedido():
	try:
		datos = json.loads(request.cookies.get(str(current_user.id)))
	except:
		datos = []
	total=0
	for articulo in datos:
		total=total+Productos.query.get(articulo["id"]).precio_final()*articulo["cantidad"]
		Productos.query.get(articulo["id"]).stock-=articulo["cantidad"]
		db.session.commit()
	resp = make_response(render_template("pedido.html",total=total))
	resp.set_cookie(str(current_user.id),"",expires=0)
	return resp
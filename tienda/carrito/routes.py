from tienda import app,db
from flask import render_template,redirect,url_for,request, make_response
from flask_login import current_user,login_required
from tienda.models import Productos


import json

@app.route('/carrito/add',methods=["GET","POST"])
def carrito_add():
	print(current_user)
	if request.method=='POST':
		indice = int(request.form['indice'])
		cantidad = int(request.form['cantidad'])
		art=Productos.query.get(request.form["id"])
		if art:
			if art.stock:
				try:
					datos = json.loads(request.cookies.get(str(current_user.id)))
				except:
					datos=[]
				actualizar = False
				for dato in datos:
					if dato["id"] == id:
						dato["cantidad"] =dato["cantidad"] +cantidad
					actualizar = True
					if not actualizar:
						datos.append({"id": indice,"cantidad":cantidad})					 
			else:
				pass #No hay stock
		else:
			pass #no exite articulo
		return make_response(redirect(url_for('tienda_page'))).set_cookie(str(current_user.id), json.dumps(datos))	
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



@app.context_processor
def contar_carrito():
	if not current_user.is_authenticated:
		return {'num_articulos':0}
	if request.cookies.get(str(current_user.id))==None:
		return {'num_articulos':0}
	else:
		datos = json.loads(request.cookies.get(str(current_user.id)))
		return {'num_articulos':len(datos)}

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
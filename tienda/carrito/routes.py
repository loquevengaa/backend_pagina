from tienda import app
from flask import render_template,redirect,url_for,request, make_response
from flask_login import current_user,login_required
from tienda.models import Productos
from tienda.forms import ComprarProductoForm

import json

@app.route('/carrito/add/<id>',methods=["get","post"])
@login_required
def carrito_add(id):
	art=Productos.query.get(id)	
	form=ComprarProductoForm()
	form.id.data=id
	if form.validate_on_submit():
		if art.stock>=int(form.cantidad.data):
			try:
				datos = json.loads(request.cookies.get(str(current_user.id)))
			except:
				datos = []
			actualizar= False
			for dato in datos:
				if dato["id"]==id:
					dato["cantidad"]=form.cantidad.data
					actualizar = True
			if not actualizar:
				datos.append({"id":form.id.data,"cantidad":form.cantidad.data})
			resp = make_response(redirect(url_for('inicio')))
			resp.set_cookie(str(current_user.id),json.dumps(datos))
			return resp
		form.cantidad.errors.append("No hay artículos suficientes.")
	return render_template("carrito_add.html",form=form,art=art)





@app.route('/carrito')
@login_required
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
@login_required
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
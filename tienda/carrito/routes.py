from datetime import datetime
from tienda import app,db
from flask import render_template,redirect,request, make_response,url_for
from tienda.models import Productos,Pedidos
import json

@app.route('/carrito/add',methods=['GET','POST'])
def carrito_add():
	if request.method=='POST':
		indice = (request.form['indice'])
		cantidad = abs(int(request.form['cantidad']))
		tipo=request.form['tipo']
		if tipo == 'producto':
			art=Productos.query.get(indice)
			if art is None:
				return redirect(request.referrer) #No hay articulo
			stock=art.stock
		else:
			stock=1 # esto hay que modificarlo cuando exista stock en combos		
		try:
			datos = json.loads(request.cookies.get("carrito"))	 #str(current_user.get_id()			
		except:
			datos=[]			
		actualizar = False
		aux=0
		for dato in datos:
			
			if dato["id"] == indice and dato['tipo']==tipo:
				dato["cantidad"] +=cantidad
				aux=dato["cantidad"]
				actualizar = True
		if  (stock-aux) < 0:
			return redirect(request.referrer) #No hay stock	
		if not actualizar:
			datos.append({"id": indice,"cantidad":cantidad,"tipo":tipo})					 						 
		resp=make_response(redirect(request.referrer))
		resp.set_cookie("carrito", json.dumps(datos)) #str(current_user.get_id()
		return resp
	return redirect(request.referrer)



@app.route('/carrito/modify',methods=['GET','POST'])
def carrito_modify():
	if request.method=='POST':
		indice = (request.form['indice'])
		tipo=request.form['tipo']
		cantidad = abs(int(request.form['cantidad']))
		if tipo == 'producto':
			art=Productos.query.get(indice)
			if art is None:
				return redirect(request.referrer) #No hay articulo
			stock=art.stock
		else:
			stock=1 # esto hay que modificarlo cuando exista stock en combos
		try:
			datos = json.loads(request.cookies.get("carrito"))	 #str(current_user.get_id()			
		except:
			datos=[]
		if art is None:
			return redirect(request.referrer) #No hay articulo		
		actualizar = False
		aux=0
		for dato in datos:
			if dato["id"] == indice and dato['tipo']==tipo:
				dato["cantidad"] =cantidad
				aux=dato["cantidad"]
				actualizar = True
		if  (stock-aux) < 0:
			return redirect(request.referrer) #No hay stock	
		if not actualizar:
			datos.append({"id": indice,"cantidad":cantidad,"tipo":tipo})					 						 
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
	pid=[]
	totalfinal=0
	for articulo in datos:
		try:
			art = Productos.query.get(articulo["id"])
			pid.append([articulo["id"]])
			imagen.append(art.imagen)
			articulos.append(art.nombre)
			cantidades.append(articulo["cantidad"])
			aux = art.precioFinal*articulo["cantidad"]
			total.append(aux)
			totalfinal=totalfinal+aux
		except:
			pass
	d = len(imagen)	
	articulos=zip(imagen,articulos,cantidades,total,pid)
	return render_template("carrito.html",articulos=articulos,totalfinal=totalfinal,d=d)



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
	resp = make_response(redirect(request.referrer))
	resp.set_cookie("carrito",json.dumps(new_datos))
	return resp


@app.route('/pedido',methods=['GET','POST'])
def pedido():
		try:
			cookies=request.cookies.get("carrito")
			datos = json.loads(cookies)
		except:
			return redirect(url_for("tienda_page"))
		if len(datos)==0:
			return redirect(url_for("tienda_page"))
		if request.method=='POST':	#finaliza la compra
			nombre = request.form['nombre']
			telefono=request.form['cod-int']+request.form['cod-area']+request.form['telefono']
			email = request.form['email']
			direccion = request.form['direccion']
			comentarios = request.form['comentarios']
			mediopago = request.form['mediopago']
			######################################
			total=0
			try:
				for articulo in datos:
					total += Productos.query.get(articulo["id"]).precioFinal*articulo["cantidad"]
				#####################################
			except:
				pass
			if cookies:	
				nuevoPedido=Pedidos(direccion=direccion,
									nombre=nombre,
									telefono=telefono,
									email=email,
									formaPago=mediopago,
									fechaHoraPedido=str(datetime.now()),
									fechaHoraEntrega="",
									estado="En Espera",
									chofer=None,
									descripcion=comentarios,
									datos_pedido=cookies,
									costo=total
									)
				db.session.add(nuevoPedido)
				db.session.commit()
				resp = make_response(redirect('/'))
				resp.set_cookie("carrito","",expires=0)
		else:
			resp = make_response(render_template("finalizar-pedido.html"))
		return resp



@app.context_processor
def contar_carrito():
	try:
		if request.cookies.get("carrito") is None:
			return {'num_articulos': 0}
		else:
			datos = json.loads(request.cookies.get("carrito"))
			return {'num_articulos': len(datos)}
	except:
			return {'num_articulos': 0}
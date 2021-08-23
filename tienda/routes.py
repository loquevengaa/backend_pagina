from tienda import app
from tienda.models import Productos,Usuarios,Combos
import json
from flask import render_template, request, redirect,make_response,url_for
from flask_login import current_user,LoginManager


login_manager = LoginManager(app)
login_manager.login_view="login"



@login_manager.user_loader
def load_user(user_id):
	aux=Usuarios.query.get(int(user_id))
	return aux




@app.route('/')
@app.route('/home',methods=['POST','GET'])#aca se muestran lo productos
def tienda_page():

	try:
		datos = json.loads(request.cookies.get("carrito"))
	except:
		datos = []

	imagen=[]
	articulos=[]
	cantidades=[]
	total=[]
	pid=[]
	stock=[]
	tipo=[]
	totalfinal=0
	for articulo in datos:
		try:

			if articulo['tipo']=='producto':
				art = Productos.query.get(articulo["id"])
				
				pid.append([articulo["id"]])
				imagen.append(art.imagen)
				articulos.append(art.nombre)
				cantidades.append(abs(articulo["cantidad"]))
				aux = art.precioFinal*cantidades[-1]
				stock.append(art.stock)
				total.append(aux)
				totalfinal=totalfinal+aux
				tipo.append("producto")
			else:
				art = Combos.query.get(articulo["id"])
				pid.append([articulo["id"]])
				imagen.append(art.imagen)
				articulos.append(art.nombre)
				cantidades.append(abs(articulo["cantidad"]))
				aux = art.precioFinal*cantidades[-1]
				stock.append(art.stock)
				total.append(aux)
				totalfinal=totalfinal+aux
				tipo.append("combo")
		except:
			pass
	d = len(imagen)	
	articulos=zip(imagen,articulos,cantidades,total,pid,stock,tipo)

	items= Productos.query.all()
	
	return render_template('home.html',items=items,articulos=articulos,totalfinal=totalfinal,d=d)



@app.route('/categoria/<categoria>',methods=['GET','POST'])#aca se muestran lo productos
def categorias(categoria):

	categoria = categoria.title()

	try:
		datos = json.loads(request.cookies.get("carrito"))
	except:
		datos = []

	imagen=[]
	articulos=[]
	cantidades=[]
	total=[]
	pid=[]
	stock=[]
	tipo=[]
	totalfinal=0
	for articulo in datos:
		try:

			if articulo['tipo']=='producto':
				art = Productos.query.get(articulo["id"])
				
				pid.append([articulo["id"]])
				imagen.append(art.imagen)
				articulos.append(art.nombre)
				cantidades.append(abs(articulo["cantidad"]))
				aux = art.precioFinal*cantidades[-1]
				stock.append(art.stock)
				total.append(aux)
				totalfinal=totalfinal+aux
				tipo.append("producto")
			else:
				art = Combos.query.get(articulo["id"])
				pid.append([articulo["id"]])
				imagen.append(art.imagen)
				articulos.append(art.nombre)
				cantidades.append(abs(articulo["cantidad"]))
				aux = art.precioFinal*cantidades[-1]
				stock.append(art.stock)
				total.append(aux)
				totalfinal=totalfinal+aux
				tipo.append("combo")
		except:
			pass
	d = len(imagen)	
	articulos=zip(imagen,articulos,cantidades,total,pid,stock,tipo)

	items= Productos.query.all()
	
	return render_template('home.html',items=items,articulos=articulos,totalfinal=totalfinal,d=d)


@app.route('/categoria/Combos',methods=['GET','POST'])#aca se muestran lo productos
def combos_cliente():

	############################################################# START CARRITO
	try:
		datos = json.loads(request.cookies.get("carrito"))
	except:
		datos = []

	imagen=[]
	articulos=[]
	cantidades=[]
	total=[]
	pid=[]
	stock=[]
	tipo=[]
	totalfinal=0
	for articulo in datos:
		try:

			if articulo['tipo']=='producto':
				art = Productos.query.get(articulo["id"])
				
				pid.append([articulo["id"]])
				imagen.append(art.imagen)
				articulos.append(art.nombre)
				cantidades.append(abs(articulo["cantidad"]))
				aux = art.precioFinal*cantidades[-1]
				stock.append(art.stock)
				total.append(aux)
				totalfinal=totalfinal+aux
				tipo.append("producto")
			else:
				art = Combos.query.get(articulo["id"])
				pid.append([articulo["id"]])
				imagen.append(art.imagen)
				articulos.append(art.nombre)
				cantidades.append(abs(articulo["cantidad"]))
				aux = art.precioFinal*cantidades[-1]
				stock.append(art.stock)
				total.append(aux)
				totalfinal=totalfinal+aux
				tipo.append("combo")
		except:
			pass
	d = len(imagen)	
	articulos=zip(imagen,articulos,cantidades,total,pid,stock,tipo)

	############################################################# END CARRITO
	#------------------------------------------------------------------------#
	############################################################# START COMBOS
	productos = Productos.query.all()
	combos= Combos.query.all()

	info = [None]*1000 #aca van los datos del carrito
	prod = [None]*1000 #aca van los datos del carrito
	for items in combos:
		info[items.id] = json.loads(items.datos_combo)
	for items in  productos:
		prod[items.id]=items

    ############################################################# END COMBOS
	
	return render_template('combos.html',items=combos,articulos=articulos,totalfinal=totalfinal,d=d,info=info,prod=prod)

	#	return redirect(request.referrer)


@app.route('/buscar/<nombre>')
def buscar(nombre):

	res = select([Productos]).where(Productos.c.nombre.like('%foobar%'))

	return res



@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404



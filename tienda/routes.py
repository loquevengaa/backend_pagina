from tienda import app
from tienda.models import Productos,Usuarios
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
	items= Productos.query.all()
	return render_template('home.html',items=items)


@app.route('/categoria/<categoria>',methods=['GET','POST'])#aca se muestran lo productos
def categorias(categoria):

	categoria = categoria.lower()

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


	items= Productos.query.filter_by(categoria=categoria)
	
	return render_template('home.html',items=items,articulos=articulos,totalfinal=totalfinal,d=d)

	#	return redirect(request.referrer)





@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404



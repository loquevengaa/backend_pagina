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

	items= Productos.query.filter_by(categoria=categoria)
	return render_template('home.html',items=items)

	#	return redirect(request.referrer)





@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404



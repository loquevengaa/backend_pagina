from tienda import app,db
from tienda.models import Productos,Usuarios

from flask import render_template, request, redirect
from flask_login import current_user,LoginManager
login_manager = LoginManager(app)
login_manager.login_view="login"



@login_manager.user_loader
def load_user(user_id):
	print(user_id)
	aux=Usuarios.query.get(int(user_id))
	print(aux)
	return aux




@app.route('/')
@app.route('/home',methods=['POST','GET'])#aca se muestran lo productos
def tienda_page():
	
	items= Productos.query.all()
	return render_template('home.html',items=items)


@app.route('/categoria/<categoria>',methods=['POST','GET'])#aca se muestran lo productos
def categorias(categoria):

	items= Productos.query.filter_by(categoria=categoria)


	if request.method=='POST':
		indice = int(request.form['indice'])
		cantidad = int(request.form['cantidad'])
		print(indice)
		print(cantidad)
		print(current_user)
		return redirect(request.referrer)


	return render_template('home.html',items=items)



@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404
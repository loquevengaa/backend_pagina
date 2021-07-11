from flask.helpers import flash
from tienda import app
import json
from flask import render_template,redirect,url_for,flash,request,session, make_response

from tienda.models import Productos,Usuarios
from tienda.forms import RegisterForm,LoginForm,ComprarProductoForm
from tienda import db
from flask_login import login_user,logout_user,current_user,login_required

""" 
login_required es para prohibir que la gente agregue cosas al carrito hasta que se registren
y se usa arriba de la funcion de esta manera
@login_required
"""

@app.route('/set_cookie')
def set_cookie():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index )  
    response.set_cookie('carrito',value=[])
    return response






@app.route('/')
@app.route('/home',methods=['GET','POST'])#aca se muestran lo productos
def tienda_page():
    items= Productos.query.all()
    return render_template('home.html.html',items=items,carrito=agregar_al_carrito)

@app.route('/registro',methods=['GET','POST'])
def pagina_registro():
    form=RegisterForm()
    if form.validate_on_submit():
        usuario_nuevo=Usuarios(
            nombre=form.nombre.data,
            email=form.email.data,
            contrasenia=form.contrasenia.data,
            telefono=form.telefono.data,
            cantidad_pedidos=0
        )
        db.session.add(usuario_nuevo)
        db.session.commit()
        login_user(usuario_nuevo)
        flash(f"Cuenta creada sactifatoriamente! estas logeado",category='success')
        return redirect(url_for('tienda_page'))
    if form.error!={}:#si no hay errores en la validacion
        for errores in form.error.values():
            flash(f'Error al crear el usuario :{errores}',category='danger')

    return render_template('registro.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        usuario_a_validar= Usuarios.query.filter_by(email=form.email.data).first()
        if usuario_a_validar and usuario_a_validar.check_contrasenia(
            contrasenia_ingresada=form.contrasenia.data
        ):
            login_user(usuario_a_validar)
            flash(f'Ingreso exitoso! {usuario_a_validar.nombre}',category='success')
            return redirect(url_for('tienda_page'))
        else:
            flash('Correo y contraseña no coinciden!! intente otra vez',category='danger')

    return render_template('login.html',form=form)
""" 
    para modificar la cabezera de la pagina y mostrar que se esta logeado hay que poner una condicion de {% if current_user.is_authenticated %}
"""
    
    
@app.route('/logout')
def logout_page():
    logout_user()
    flash('Sesion cerrada con exito',category='info')
    return redirect(url_for('home_page'))



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
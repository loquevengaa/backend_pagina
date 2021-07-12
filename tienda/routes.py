from warnings import catch_warnings
from flask.helpers import flash
from tienda import app
import json
from flask import render_template,redirect,url_for,flash,request,session, make_response

from tienda.models import Productos,Usuarios
from tienda.forms import RegisterForm,LoginForm,ComprarProductoForm
from tienda import db
from flask_login import login_user,logout_user,current_user,login_required

from sqlalchemy import update
""" 
login_required es para prohibir que la gente agregue cosas al carrito hasta que se registren
y se usa arriba de la funcion de esta manera
@login_required
"""
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from datetime import datetime
import os
import pandas as pd

@app.route('/set_cookie')
def set_cookie():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index )  
    response.set_cookie('carrito',value=[])
    return response




basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/media/productos/')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


df = pd.read_excel('tienda/productos.xlsx')
df['preciofinal']=round((100-df.oferta)*(df.precio/100),2)
d = len(df['id'])

@app.route('/categoria/<categoria>')
def categoria(categoria):
    return render_template('home.html',df=df,d=d,cat=categoria)

@app.route('/panel', methods = ['POST','GET'])
def panel():
    items= Productos.query.all()
    d=len(df)
    if request.method == 'POST':
        indice = int(request.form['indice'])
        tipo = request.form['tipo']
        producto=Productos.query.filter_by(id=indice).first()
        print(tipo)

        ######################################### CAMBIA NOMBRE
        if tipo == 'cambianombre':
            producto.nombre = request.form['nombre']
            
        ######################################### CAMBIA STOCK
        elif tipo == 'cambiastock':
            try:
                producto.stock+= int(request.form['cantidad'])
            except:
                pass
        ######################################### CAMBIA PRECIO
        elif tipo == 'cambiaprecio':
            producto.precio=float(request.form['precio'])
            producto.precioFinal= round((100-producto.oferta)*(producto.precio/100),2)

            
        ######################################### CAMBIA OFERTA
        elif tipo == 'cambiaoferta':
            producto.oferta = int(request.form['oferta'])
            producto.precioFinal = round((100-producto.oferta)*(producto.precio/100),2)

        ######################################### CAMBIA CATEGORIA
        elif tipo == 'cambiacategoria':
            print(indice)
            print(request.form['categoria'])
            producto.categoria = request.form['categoria']

        ######################################### ELIMINAR
        elif tipo == 'eliminar':
            db.session.delete(producto)

        ######################################### CAMBIA IMAGEN
        elif tipo == 'cambiaimagen':
            img_name = str(producto.imagen)
            print(img_name)
            if img_name!='default.png':
                try:
                    os.remove('tienda/static/media/productos'+img_name)#tienda\static\media\productos
                except Exception as e:
                    pass       

            now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
            now = now.replace(':','');now = now.replace('.','')
            extension = request.files['image'].filename.split('.')
            photos.save(request.files.get('image'),name=now+'.')

            producto.imagen = now+'.'+extension[1]

        db.session.commit()
    else:
        print('GET METHOD RECEIVED')
    return render_template('paneldatatable.html',items=Productos.query.all() ) 

@app.route('/panel/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['n-nombre']
        categoria = request.form['n-categoria']
        stock = int(request.form['n-stock'])
        precio = float(request.form['n-precio'])
        oferta = int(request.form['n-oferta'])
        precioFinal=precio*float(oferta/100)

        try:
            now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
            now = now.replace(':','');now = now.replace('.','')
            extension = request.files['n-image'].filename.split('.')
            photos.save(request.files.get('n-image'),name=now+'.')
            imgnombre = now+'.'+extension[1]

       

            producto=Productos(nombre=nombre,
                           categoria=categoria,
                           precio=precio,
                           stock=stock,
                           oferta=oferta,
                           precioFinal=precioFinal,
                           imagen=imgnombre)
            db.session.add(producto)
            db.session.commit()
        except:
            raise Exception
        return redirect(url_for('panel'))







@app.route('/')
@app.route('/home',methods=['GET','POST'])#aca se muestran lo productos
def tienda_page():
	agregar_al_carrito=ComprarProductoForm()
	items= Productos.query.all()
	return render_template('home.html',items=items,carrito=agregar_al_carrito,cat='null')

@app.route('/registro',methods=['GET','POST'])
def pagina_registro():
    form=RegisterForm()
    print("validate on submite")
    if form.validate_on_submit():
        print("entro ñieri")
        usuario_nuevo=Usuarios(
            nombre=form.nombre.data,
            email=form.email.data,
            contrasenia=form.contrasenia.data,
            telefono=form.telefono.data,
            cantidad_pedidos=0,
            admin=False,
            chofer=False
        )
        db.session.add(usuario_nuevo)
        db.session.commit()
        login_user(usuario_nuevo)
        flash(f"Cuenta creada sactifatoriamente! estas logeado",category='success')
        return redirect(url_for('tienda_page'))
    else:
        flash(f'Error al crear el usuario ',category='danger')

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
    return redirect(url_for('tienda_page'))



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
from tienda import app
import json
from flask import render_template,redirect,url_for,request,abort,flash
from flask_login import current_user,login_required,login_user,LoginManager
from tienda.models import Productos,Usuarios,Pedidos,Combos

from tienda import db



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
"""
@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

"""
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, '../static/media/productos/')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)



@app.route('/panel', methods = ['POST','GET'])
@login_required
def panel():
    if not current_user.is_admin():
        abort(404)
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
                    os.remove('tienda/static/media/productos/'+img_name)#tienda\static\media\productos
                except Exception as e:
                    print('algo pasooooooooooo')
                    pass       

            now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
            now = now.replace(':','');now = now.replace('.','')
            extension = request.files['image'].filename.split('.')
            photos.save(request.files.get('image'),name=now+'.')

            producto.imagen = now+'.'+extension[-1]

        db.session.commit()
    else:
        print('GET METHOD RECEIVED')
    return render_template('paneldatatable.html',items=Productos.query.all() ) 


@app.route('/panel/pedidos', methods=['GET','POST'])
@login_required
def tablapedidos():
    pedidos = Pedidos.query.all()
    productos = Productos.query.all()
    info = [None]*1000 #aca van los datos del carrito
    prod = [None]*1000 #aca van los datos del carrito
    for items in pedidos:
        info[items.id] = json.loads(items.datos_pedido)
    for items in  productos:
        prod[items.id]=items


    return render_template('paneltablapedidos.html',data=pedidos,info=info,productos=productos,prod=prod)












@app.route('/panel/agregar', methods=['GET','POST'])
@login_required
def agregar():
    if not current_user.is_admin():
        abort(404)
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
            imgnombre = now+'.'+extension[-1]

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
            pass
        return redirect(url_for('panel'))





@app.route('/panel/combos', methods=['GET','POST'])
@login_required

def combos():

    productos = Productos.query.all()

    return render_template('panelcombos.html',productos=productos)

@app.route('/panel/combos/agregar', methods=['GET','POST'])
@login_required
def combos_agregar():

    productos = Productos.query.all()

    if request.method=='POST':
        print("agrego combo")
        items=request.form.getlist('skills')
        datos=[]
        for item in items:
            datos.append({"id":item,"cantidad":0})
        print(datos)
        datos=json.dumps(datos)
        try:
            now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
            now = now.replace(':','');now = now.replace('.','')
            extension = request.files['n-image'].filename.split('.')
            photos.save(request.files.get('n-image'),name=now+'.')
            imgnombre = now+'.'+extension[-1]
        except:
            imgnombre ="a" 

        nuevoCombo=Combos(
                    datos_combo=datos,
                    precioFinal=0,
                    imagen=imgnombre    
                    )
        db.session.add(nuevoCombo)
        db.session.commit()        
        
    return render_template('panelcombos.html',productos=productos)
        
@app.route('/panel/combos/modifica', methods=['GET','POST'])
@login_required
def combos_modifica():
    productos = Productos.query.all()

    if request.method=='POST':
        indice = int(request.form['indice'])
        tipo = request.form['tipo']
        combo=Combos.query.filter_by(id=indice).first()    

        if tipo == 'cambianombre':
            combo.nombre=request.form['nombre']

        elif tipo == 'cambiaprecio':
            combo.precio=float(request.form['precio'])
        
        elif tipo == 'eliminar':
            db.session.delete(combo)  


        elif tipo == 'cambio stock':
            
            info=json.load(combo.datos_combo)
            for Produ in info:
                if Produ["id"]==request.form["indice_producto"]:
                   Produ["camtidad"]=int(request.form["cantidad"]) 
            combo.datos_combo=json.dumps(info)        
            
        elif tipo == 'cambiaimagen':
            img_name = str(combo.imagen)
            print(img_name)
            if img_name!='default.png':
                try:
                    os.remove('tienda/static/media/productos/'+img_name)#tienda\static\media\productos
                except Exception as e:
                    print('algo pasooooooooooo')
                    pass       

            now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
            now = now.replace(':','');now = now.replace('.','')
            extension = request.files['image'].filename.split('.')
            photos.save(request.files.get('image'),name=now+'.')

            combo.imagen = now+'.'+extension[-1]

        db.session.commit()
    return render_template('panelcombos.html',productos=productos)



@app.route('/panel/choferes/crear_chofer', methods=['GET','POST'])
@login_required
def crear_chofer():
    if not current_user.is_admin():
        abort(404)
    if request.method == 'POST':
        try:
            nombre= request.form['nombre-chofer']
            email= request.form['email-chofer']
            telefono=request.form['telefono-chofer']
            contrasenia= request.form['contrasenia-chofer']
            chofer=Usuarios(nombre=nombre,
                        email=email,
                        telefono=telefono,
                        contrasenia_cifrada=contrasenia,
                        cantidad_pedidos=0,
                        admin=False,
                        chofer=True,
                        )
            db.session.add(chofer)
            db.commit()
            flash(f'Chofer creado con exito')
        except:
            flash(f'Error al crear Chofer')
        return redirect(url_for('panel'))


@app.route('/panel/choferes', methods=['GET','POST'])
@login_required
def choferes():
    if not current_user.is_admin():
        abort(404)
        
    


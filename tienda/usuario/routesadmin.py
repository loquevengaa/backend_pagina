from tienda import app
import json
from flask import render_template,redirect,url_for,request,abort,flash
from flask_login import current_user,login_required,login_user,LoginManager
from tienda.models import Productos,Usuarios,Pedidos,Combos,meFijoStock

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

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

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

###################################################################### INICIO TABLA PEDIDOS

@app.route('/panel/pedidos', methods=['GET','POST'])
@login_required
def tablapedidos():
    pedidos = Pedidos.query.all()
    productos = Productos.query.all()
    combos = Combos.query.all()
    info = [None]*1000 #aca van los datos del carrito
    prod = [None]*1000 #aca van los datos del carrito
    comb = [None]*1000
    infocombos = [None]*1000

    for items in pedidos:
        info[items.id] = json.loads(items.datos_pedido)

    for items in  productos:
        prod[items.id]=items

    for items in  combos:
        comb[items.id]=items
        infocombos[items.id] = json.loads(items.datos_combo)

    choferes=Usuarios.query.filter(Usuarios.chofer==1)


    return render_template('paneltablapedidos.html',data=pedidos,info=info,productos=productos,prod=prod,choferes=choferes,combos=combos,comb=comb,infocombos=infocombos)


@app.route('/panel/pedidos/chofer', methods=['GET','POST'])
@login_required
def tablapedidos_eligechofer():
    
    if request.method == 'POST':
        chofer = request.form['chofer']
        indice = request.form['indice']
        pedidos = Pedidos.query.filter_by(id=indice).first()
        pedidos.chofer = chofer
        pedidos.estado = 'Enviando'
        db.session.commit()

    return redirect(url_for('tablapedidos'))

@app.route('/panel/pedidos/estadoenvio', methods=['GET','POST'])
@login_required
def tablapedidos_elige_estado_envio():
    
    if request.method == 'POST':
        estado = request.form['estadoenvio']
        indice = request.form['indice']
        pedidos = Pedidos.query.filter_by(id=indice).first()
        pedidos.estado = estado

        if estado == 'Cancelado':

            productos_pedido = json.loads(pedidos.datos_pedido)

            for articulo in productos_pedido:

                try:

                    if articulo['tipo'] == 'producto': # si es un producto, retira stock del producto
                        producto = Productos.query.get(articulo["id"])
                        producto.stock += articulo['cantidad']
                        
                    elif articulo['tipo'] == 'combo': # SI ES UN COMBO, ITERA LOS PRODUCTOS QUE LO CONFORMAn Y LUEGO LOS RETIRA
                        combo = Combos.query.get(articulo['id'])
                        datos_combo = json.loads(combo.datos_combo)

                        for prod in datos_combo:
                            producto = Productos.query.get(prod["id"])
                            producto.stock += articulo['cantidad']*prod['cantidad']   

                except:
                    pass    

        db.session.commit()

    return redirect(url_for('tablapedidos'))

@app.route('/panel/pedidos/estadopago', methods=['GET','POST'])
@login_required
def tablapedidos_elige_estado_pago():
    
    if request.method == 'POST':
        estado = request.form['estadopago']
        indice = request.form['indice']
        pedidos = Pedidos.query.filter_by(id=indice).first()
        pedidos.estadoPago = estado
        db.session.commit()

    return redirect(url_for('tablapedidos'))

################################################################### FIN TABLA PEDIDOS

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

    meFijoStock()

    productos = Productos.query.all()
    combos= Combos.query.all()

    info = [None]*1000 #aca van los datos del carrito
    prod = [None]*1000 #aca van los datos del carrito
    for items in combos:
        info[items.id] = json.loads(items.datos_combo)
    for items in  productos:
        prod[items.id]=items

    return render_template('panelcombos.html',productos=productos,combos=combos,info=info,prod=prod)

@app.route('/panel/combos/agregar', methods=['GET','POST'])
@login_required
def combos_agregar():

    if request.method=='POST':
        print("agrego combo")
        items=request.form.getlist('productos')
        datos=[]
        for item in items:
            datos.append({"id":item,"cantidad":1})
        print(datos)
        datos=json.dumps(datos)
        
        now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
        now = now.replace(':','');now = now.replace('.','')
        extension = request.files['n-image'].filename.split('.')
        photos.save(request.files.get('n-image'),name=now+'.')
        imgnombre = now+'.'+extension[-1]
        
        #imgnombre ="default.png" 

        nuevoCombo=Combos(
                    nombre=request.form['nombre'],
                    datos_combo=datos,
                    precioFinal=float(request.form['precio']),
                    stock=1,
                    imagen=imgnombre    
                    )
        db.session.add(nuevoCombo)
        db.session.commit()

        meFijoStock()
    return redirect(url_for('combos'))


        
@app.route('/panel/combos/modifica', methods=['GET','POST'])
@login_required
def combos_modifica():

    if request.method=='POST':
        indice = int(request.form['indice'])
        tipo = request.form['tipo']
        combo=Combos.query.filter_by(id=indice).first()
        
   

        if tipo == 'cambianombre':
            combo.nombre=request.form['nombre']

        elif tipo == 'agrega_producto':
            indice_producto=request.form['idproducto']
            
            info=json.loads(combo.datos_combo)
            for Produ in info:
                if Produ["id"]==indice_producto:
                        return redirect(url_for('combos'))
            info.append({"id":indice_producto,"cantidad":1})
            combo.datos_combo=json.dumps(info)

           
        elif tipo == 'cambiaprecio':
            combo.precioFinal=float(request.form['precio'])
        
        elif tipo == 'eliminar':
            print('llegue')
            db.session.delete(combo)  


        elif tipo == 'cambiastock':

            idproducto = request.form["idproducto"]
            cantidad = int(request.form["cantidad"])
            
            info=json.loads(combo.datos_combo)
            for Produ in info:
                if Produ["id"]==idproducto:
                   Produ["cantidad"]=cantidad

            combo.datos_combo=json.dumps(info) 

        elif tipo == 'eliminaproducto':

            idproducto = request.form["idproducto"]        
            nuevainfo = []

            info=json.loads(combo.datos_combo)
            for Produ in info:
                if Produ["id"]!=idproducto:
                    nuevainfo.append(Produ)

            combo.datos_combo=json.dumps(nuevainfo)        
            
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
            extension = request.files['n-image'].filename.split('.')
            photos.save(request.files.get('n-image'),name=now+'.')

            combo.imagen = now+'.'+extension[-1]


        db.session.commit()
        meFijoStock()
    return redirect(url_for('combos'))


################################################################### INICIA CHOFERES
@app.route('/panel/choferes', methods=['GET','POST'])
@login_required
def choferes():
    if not current_user.is_admin():
        abort(404)

    choferes=Usuarios.query.filter(Usuarios.chofer==1)

    return render_template('choferes.html',choferes=choferes)

@app.route('/panel/choferes/eliminar', methods=['GET','POST'])
@login_required
def choferes_eliminar():
    if not current_user.is_admin():
        abort(404)

    if request.method=='POST':
        indice = request.form['idchofer']
        chofer=Usuarios.query.filter_by(id=indice).first()
        db.session.delete(chofer)
        db.session.commit()

    return redirect(url_for('choferes'))


@app.route('/panel/choferes/agregar', methods=['GET','POST'])
@login_required
def crear_chofer():
    if not current_user.is_admin():
        abort(404)
    if request.method == 'POST':
        try:
            nombre= request.form['nombre']
            email= request.form['email']
            telefono=request.form['telefono']
            contrasenia= request.form['contrasenia']
            chofer=Usuarios(nombre=nombre,
                        email=email,
                        telefono=telefono,
                        contrasenia=contrasenia,
                        cantidad_pedidos=0,
                        admin=False,
                        chofer=True,
                        )
            db.session.add(chofer)
            db.session.commit()
            flash(f'Chofer creado con exito')
        except:
            flash(f'Error al crear Chofer')   

    return redirect(url_for('choferes'))

@app.route('/panel/choferes/perfil/<chofer_id>', methods=['GET','POST'])
@login_required
def choferes_perfil(chofer_id):
    if not current_user.is_admin() and not current_user.is_chofer():
        abort(404)

    if  not current_user.is_admin():
        if current_user.id!=chofer_id:
            abort(404)

    chofer_id=int(chofer_id)

    pedidos=Pedidos.query.filter(Pedidos.chofer==chofer_id)
    productos = Productos.query.all()
    combos = Combos.query.all()
    info = [None]*1000 #aca van los datos del carrito
    prod = [None]*1000 #aca van los datos del carrito
    comb = [None]*1000
    infocombos = [None]*1000

    for items in pedidos:
        info[items.id] = json.loads(items.datos_pedido)

    for items in  productos:
        prod[items.id]=items

    for items in  combos:
        comb[items.id]=items
        infocombos[items.id] = json.loads(items.datos_combo)

    choferes=Usuarios.query.filter(Usuarios.chofer==1)


    return render_template('choferes_perfil.html',data=pedidos,info=info,productos=productos,prod=prod,choferes=choferes,combos=combos,comb=comb,infocombos=infocombos)
 
        
############################################################################# FIN CHOFERES


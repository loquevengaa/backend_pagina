
from tienda import app

from flask import render_template,redirect,url_for,request

from tienda.models import Productos
from tienda.forms import ComprarProductoForm
from tienda import db


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



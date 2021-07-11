from flask import Flask,render_template, session,request,redirect,url_for
import pandas as pd 
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/media/productos/')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


df = pd.read_excel('db/productos.xlsx')
df['preciofinal']=round((100-df.oferta)*(df.precio/100),2)
d = len(df['id'])

@app.route('/')
def home():
    return render_template('home.html',df=df,d=d,cat='null')

@app.route('/categoria/<categoria>')
def categoria(categoria):
    return render_template('home.html',df=df,d=d,cat=categoria)

@app.route('/panel', methods = ['POST','GET'])
def panel():
    d = len(df['id'])
    if request.method == 'POST':
        indice = int(request.form['indice'])
        tipo = request.form['tipo']
        print(tipo)

        ######################################### CAMBIA NOMBRE
        if tipo == 'cambianombre':
            df.iat[indice,1] = request.form['nombre']

        ######################################### CAMBIA STOCK
        elif tipo == 'cambiastock':
            try:
                df.iat[indice,4] = df.iat[indice,4] + int(request.form['cantidad'])
            except:
                pass

        ######################################### CAMBIA PRECIO
        elif tipo == 'cambiaprecio':
            df.iat[indice,3] = float(request.form['precio'])
            df.iat[indice,7] = round((100-df.iat[indice,5])*(df.iat[indice,3]/100),2)

        ######################################### CAMBIA OFERTA
        elif tipo == 'cambiaoferta':
            df.iat[indice,5] = int(request.form['oferta'])
            df.iat[indice,7] = round((100-df.iat[indice,5])*(df.iat[indice,3]/100),2)

        ######################################### CAMBIA CATEGORIA
        elif tipo == 'cambiacategoria':
            print(indice)
            print(request.form['categoria'])
            df.iat[indice,2] = request.form['categoria']

        ######################################### ELIMINAR
        elif tipo == 'eliminar':
            df.drop(indice, inplace = True)
            df.reset_index(drop=True,inplace = True)
            d = len(df['id'])

        ######################################### CAMBIA IMAGEN
        elif tipo == 'cambiaimagen':
            img_name = str(df.iat[indice,6])
            if img_name!='default.png':
                try:
                    os.remove('static/media/productos/'+img_name)
                except Exception as e:
                    pass       
            now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
            now = now.replace(':','');now = now.replace('.','')
            extension = request.files['image'].filename.split('.')
            photos.save(request.files.get('image'),name=now+'.')
            df.iat[indice,6] = now+'.'+extension[1]
    else:
        print('GET METHOD RECEIVED')
            
    df.to_csv('db/productos.csv', index=False)
    return render_template('paneldatatable.html',df=df,d=d) 

@app.route('/panel/agregar', methods=['GET','POST'])
def agregar():
    dfn=df
    if request.method == 'POST':
        nombre = request.form['n-nombre']
        categoria = request.form['n-categoria']
        stock = int(request.form['n-stock'])
        precio = float(request.form['n-precio'])
        oferta = int(request.form['n-oferta'])
        extension = request.files['n-image'].filename.split('.')
        now = str(datetime.now());now = now.replace('-','');now = now.replace(' ','')
        now = now.replace(':','');now = now.replace('.','')
        imgnombre = now+'.'+extension[1]
        newid = dfn.iat[-1,0] + 1

        dfn = dfn.append([newid,nombre,categoria,precio,stock,oferta,imgnombre,0])

    df.to_csv('db/productos.csv', index=False)
    return render_template('panel.html',df=df,d=d)   

@app.route('/login')
def login():
    return render_template('layout.html',title="Registro")

@app.route('/carrito')
def carrito():
    return "zona de carrito"

@app.route('/pedidos_realizados')
def pedidos():
    return "donde ve los pedidos"

if __name__=="__main__":
    app.run(debug=True)
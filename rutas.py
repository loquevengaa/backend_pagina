from flask import Flask,render_template, session,request,redirect,url_for
import pandas as pd 

app = Flask(__name__)

df = pd.read_excel('db/productos.xlsx')
df['preciofinal']=round((100-df.oferta)*(df.precio/100),0)
d = len(df['id'])

@app.route('/')
def home():
    return render_template('home.html',df=df,d=d,cat='null')

@app.route('/categoria/<categoria>')
def categoria(categoria):
    return render_template('home.html',df=df,d=d,cat=categoria)

@app.route('/panel')
def panel():
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
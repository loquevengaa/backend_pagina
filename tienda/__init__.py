from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='j4hfb32dAKNDs9jf56bsa8dljfña@uNUKjBbKJHG78'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"

from tienda import routes
from tienda.usuario import routes
from tienda.carrito import routes
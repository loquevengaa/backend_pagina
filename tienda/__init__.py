from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

##########################################
#from flask_script import Manager
#from flask_migrate import Migrate,MigrateCommand

#####################################3
app= Flask(__name__)

app.config['RECAPTCHA_PUBLIC_KEY']="6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='j4hfb32dAKNDs9jf56bsa8dljfña@uNUKjBbKJHG78'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
#migrate=Migrate(app,db)
#manager =Manager(app)

from tienda import routes
from tienda.usuario import routes
from tienda.carrito import routes
from tienda.usuario import routesadmin
from tienda.usuario import routeschoferes
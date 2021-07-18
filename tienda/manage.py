from flask import Flask
from flask_script import Manager
from tienda import app, db
from tienda.models import *
from getpass import getpass

manager = Manager(app)
app.config['DEBUG'] = True  # Ensure debugger will load.



@manager.command
def create_admin():
    usuario = {"username": input("Usuario:"),
               "password": getpass("Password:"),
               "nombre": input("Nombre completo:"),
               "email": input("Email:"),
               "admin": True,
               "chofer":False}
    usu = Usuarios(**usuario)
    db.session.add(usu)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
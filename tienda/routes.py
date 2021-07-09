from flask.helpers import flash
from tienda import app
from flask import render_template,redirect,url_for,flash,request
from tienda.models import Productos,Usuarios
from tienda.forms import RegisterForm,LoginForm,ComprarProductoForm
from tienda import db
from flask_login import login_user,logout_user,current_user,login_required

""" 
login_required es para prohibir que la gente agregue cosas al carrito hasta que se registren
y se usa arriba de la funcion de esta manera
@login_required
"""

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/tienda',methods=['GET','POST'])#aca se muestran lo productos
def tienda_page():
    agregar_al_carrito=ComprarProductoForm()
    if request.method == 'POST':
        producto=request.form.get('id')
        cantidad=request.form.get('cantidad')
        producto=Productos.query.filter_by(id=producto).first()
        if producto:
            #aca iria la logica del carrito
            pass

    items= Productos.query.all()
    return render_template('tienda.html',items=items,carrito=agregar_al_carrito)

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
















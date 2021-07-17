from tienda import app,db

from tienda.usuario.forms import RegisterForm,LoginForm
from tienda.models import Usuarios
from flask import flash,render_template,redirect,url_for
from flask_login import login_user,logout_user


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


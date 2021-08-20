from tienda import app,db

from tienda.usuario.forms import RegisterForm,LoginForm,FormUsuario,FormChangePassword
from tienda.models import Usuarios
from flask import flash,render_template,redirect,url_for,abort,request
from flask_login import login_user,logout_user,login_required,current_user
"""
@app.route('/registro',methods=['GET','POST'])
def pagina_registro():
    if current_user.is_authenticated:
        return redirect(url_for("tienda_page"))
    form=RegisterForm()
    print("validate on submite")
    if form.validate_on_submit():
        print("entro ñieri")
        existe_usuario = Usuarios.query.filter_by(email=form.email.data).first()
        if existe_usuario is None:
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
            flash(f"Cuenta creada sactifatoriamente! estas logeado")
            return redirect(url_for('tienda_page'))
        form.username.errors.append("Correo de usuario ya existe.")
    else:
        flash(f'Error al crear el usuario ',category='danger')

    return render_template('registro.html',form=form)

"""



@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tienda_page"))
    form=LoginForm()
    if form.validate_on_submit():
        usuario_a_validar= Usuarios.query.filter_by(email=form.email.data).first()
        if usuario_a_validar and usuario_a_validar.check_contrasenia(
            contrasenia_ingresada=form.contrasenia.data
        ):
            login_user(usuario_a_validar)
            flash(f'Ingreso exitoso! {usuario_a_validar.nombre}',category='success')
            return redirect(url_for('panel'))
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
"""
@app.route('/perfil/<email>', methods=["get","post"])
def perfil(email):
	user=Usuarios.query.filter_by(email=email).first()
	if user is None:
		abort(404)	

	form=FormUsuario(request.form,obj=user)
	del form.password	
	if form.validate_on_submit():
		form.populate_obj(user)
		db.session.commit()
		return redirect(url_for("tienda_page"))	

	return render_template("usuarios.html",form=form,perfil=True)



@app.route('/changepassword/<email>', methods=["get","post"])
@login_required
def changepassword(email):
	user=Usuarios.query.filter_by(email=email).first()
	if user is None:
		abort(404)	

	form=FormChangePassword()
	if form.validate_on_submit():
		form.populate_obj(user)
		db.session.commit()
		return redirect(url_for("inicio"))	

	return render_template("changepassword.html",form=form)




@app.route('/set_admin')
def set_admin():
    usuario_nuevo=Usuarios(
            nombre="Sol",
            email="sol@gmail.com",
            contrasenia="adminadmin",
            telefono=2236168614,
            cantidad_pedidos=0,
            admin=True,
            chofer=False
        )
    db.session.add(usuario_nuevo)
    db.session.commit()
    return redirect(url_for('tienda_page'))"""
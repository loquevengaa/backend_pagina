from tienda import app
import json
from flask import render_template,redirect,url_for,request,abort,flash
from flask_login import current_user,login_required,login_user,LoginManager
from tienda.models import Productos,Usuarios,Pedidos,Combos

from tienda import db



@app.route("/pedidos/choferes")
@login_required
def mostrar_pedidos():
    if not current_user.is_chofer():
        abort(404)
    else:
        sin_entregar=()
        pedidos=Pedidos.query.filter_by(chofer=current_user)
        for pedido in pedidos:
            if pedido.estado != "entregado":
                sin_entregar.append(pedido)
        
            

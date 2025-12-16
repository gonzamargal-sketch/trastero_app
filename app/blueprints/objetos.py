
from flask import Blueprint, render_template, request, redirect, url_for


objetos_bp = Blueprint(
    'objetos',
    __name__,
    url_prefix='/objetos'
)


# Lista temporal en memoria
objetos = []

@objetos_bp.route('/')
def inicio():
    return render_template('index.html', objetos=objetos)

@objetos_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        obj = {
            'nombre': request.form['nombre'],
            'categoria': request.form['categoria'],
            'ubicacion': request.form['ubicacion'],
            'cantidad': request.form['cantidad'],
            'notas': request.form['notas'], 
            'foto': request.form['foto']
        }
        objetos.append(obj)
        return redirect(url_for('objetos.inicio'))

    return render_template('agregar.html')
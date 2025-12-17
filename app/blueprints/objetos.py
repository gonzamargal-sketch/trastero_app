
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Objeto, db

objetos_bp = Blueprint(
    'objetos',
    __name__,
    url_prefix='/objetos'
)


# Listar objetos
@objetos_bp.route('/')
def inicio():
    objetos = Objeto.query.all()
    return render_template('index.html', objetos=objetos)

# Agregar objeto
@objetos_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            # Si no hay nombre, mostramos un mensaje y no guardamos
            flash("El nombre es obligatorio", "error")
            return redirect(url_for('objetos.agregar'))

        obj = Objeto(
            nombre=nombre,
            categoria=request.form.get('categoria', '').strip(),
            ubicacion=request.form.get('ubicacion', '').strip(),
            cantidad=int(request.form.get('cantidad', 1)),
            notas=request.form.get('notas', '').strip()
        )
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('objetos.inicio'))

    return render_template('agregar.html')

# Eliminar objeto
@objetos_bp.route('/<int:objeto_id>/eliminar', methods=['GET', 'POST'])
def eliminar(objeto_id):
    objeto = Objeto.query.get_or_404(objeto_id)

    if request.method == 'POST':
        if request.form.get('_method') != 'DELETE':
            return 'Method Not Allowed', 405

        # Guardamos datos ANTES de borrar
        nombre = objeto.nombre
        cantidad_actual = objeto.cantidad

        try:
            cantidad = int(request.form.get('cantidad', 1))
        except ValueError:
            flash("Cantidad inválida", "danger")
            return redirect(url_for('objetos.inicio'))

        if cantidad <= 0:
            flash("Cantidad inválida", "danger")
            return redirect(url_for('objetos.inicio'))

        try:
            if cantidad >= cantidad_actual:
                db.session.delete(objeto)
                mensaje = f"Objeto '{nombre}' eliminado"
            else:
                objeto.cantidad = cantidad_actual - cantidad
                mensaje = f"Se eliminaron {cantidad} de '{nombre}'"

            db.session.commit()
            flash(mensaje, "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Error interno: {e}", "danger")

        return redirect(url_for('objetos.inicio'))

    return render_template('eliminar.html', objeto=objeto)

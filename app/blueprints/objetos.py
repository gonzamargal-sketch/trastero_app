
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

# Editar objeto
@objetos_bp.route('/<int:objeto_id>/editar', methods=['GET', 'POST'])
def editar(objeto_id):
    objeto = Objeto.query.get_or_404(objeto_id)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return redirect(url_for('objetos.editar', objeto_id=objeto.id))

        objeto.nombre = nombre
        objeto.categoria = request.form.get('categoria', '').strip()
        objeto.ubicacion = request.form.get('ubicacion', '').strip()
        objeto.notas = request.form.get('notas', '').strip()

        try:
            db.session.commit()
            flash(f"Objeto '{objeto.nombre}' actualizado", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al editar: {e}", "danger")

        return redirect(url_for('objetos.inicio'))

    return render_template('editar.html', objeto=objeto)

@objetos_bp.route("/<int:objeto_id>/cantidad", methods=["POST"])
def modificar_cantidad(objeto_id):
    objeto = Objeto.query.get_or_404(objeto_id)

    try:
        valor = int(request.form.get("valor", 1))
        if valor < 1:
            flash("El valor debe ser mayor que 0", "danger")
            return redirect(url_for("objetos.inicio"))

        accion = request.form.get("accion")
        if accion == "sumar":
            objeto.cantidad += valor
            flash(f"Se añadieron {valor} a '{objeto.nombre}'", "success")
        elif accion == "restar":
            if objeto.cantidad - valor < 0:
                objeto.cantidad = 0
            else:
                objeto.cantidad -= valor
            flash(f"Se restaron {valor} de '{objeto.nombre}'", "success")
        else:
            return "Acción no válida", 400

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar cantidad: {e}", "danger")

    return redirect(url_for("objetos.inicio"))





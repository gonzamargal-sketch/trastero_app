
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
@objetos_bp.route("/<int:objeto_id>/eliminar", methods=["POST"])
def eliminar(objeto_id):
    objeto = Objeto.query.get_or_404(objeto_id)
    try:
        db.session.delete(objeto)
        db.session.commit()
        flash(f"Objeto '{objeto.nombre}' eliminado completamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar objeto: {e}", "danger")
    return redirect(url_for("objetos.inicio"))

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


# =====================
# RUTAS API
# =====================

@objetos_bp.route("/api", methods=["GET"])
def api_listar_objetos():
    objetos = Objeto.query.all()
    return jsonify([obj.to_dict() for obj in objetos])

@objetos_bp.route("/api", methods=["POST"])
def api_agregar_objeto():
    data = request.json
    if not data.get("nombre"):
        return jsonify({"error": "Nombre obligatorio"}), 400
    obj = Objeto(
        nombre=data["nombre"],
        cantidad=data.get("cantidad", 1),
        categoria=data.get("categoria"),
        ubicacion=data.get("ubicacion"),
        notas=data.get("notas")
    )
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), 201

@objetos_bp.route("/api/<int:objeto_id>", methods=["PUT"])
def api_editar_objeto(objeto_id):
    obj = Objeto.query.get_or_404(objeto_id)
    data = request.json
    obj.nombre = data.get("nombre", obj.nombre)
    obj.categoria = data.get("categoria", obj.categoria)
    obj.ubicacion = data.get("ubicacion", obj.ubicacion)
    obj.notas = data.get("notas", obj.notas)
    db.session.commit()
    return jsonify(obj.to_dict())

@objetos_bp.route("/api/<int:objeto_id>/cantidad", methods=["PATCH"])
def api_modificar_cantidad(objeto_id):
    obj = Objeto.query.get_or_404(objeto_id)
    data = request.json
    valor = data.get("valor", 1)
    accion = data.get("accion")
    if accion == "sumar":
        obj.cantidad += valor
    elif accion == "restar":
        obj.cantidad = max(obj.cantidad - valor, 0)
    else:
        return jsonify({"error": "Acción no válida"}), 400
    db.session.commit()
    return jsonify(obj.to_dict())

@objetos_bp.route("/api/<int:objeto_id>", methods=["DELETE"])
def api_eliminar_objeto(objeto_id):
    obj = Objeto.query.get_or_404(objeto_id)
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"mensaje": f"Objeto {obj.nombre} eliminado"})




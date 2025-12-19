
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.models import Objeto, db
from werkzeug.utils import secure_filename
import os

objetos_bp = Blueprint(
    'objetos',
    __name__,
    url_prefix='/objetos'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = "static/uploads"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Listar objetos
@objetos_bp.route('/')
def inicio():
    objetos = Objeto.query.all()
    return render_template('index.html', objetos=objetos)

# Agregar objeto
@objetos_bp.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        categoria = request.form.get("categoria")
        ubicacion = request.form.get("ubicacion")
        cantidad = int(request.form.get("cantidad", 1))

        archivo = request.files.get("foto")
        ruta_foto = None
        if archivo and allowed_file(archivo.filename):
            filename = secure_filename(archivo.filename)
            upload_path = os.path.join(current_app.root_path, "static/uploads", filename)
            archivo.save(upload_path)
            ruta_foto = f"uploads/{filename}"

        nuevo_objeto = Objeto(
            nombre=nombre,
            categoria=categoria,
            ubicacion=ubicacion,
            cantidad=cantidad,
            foto=ruta_foto
        )
        db.session.add(nuevo_objeto)
        db.session.commit()
        flash("Objeto agregado correctamente", "success")
        return redirect(url_for("objetos.inicio"))

    return render_template("agregar.html")

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
@objetos_bp.route("/<int:objeto_id>/editar", methods=["GET", "POST"])
def editar(objeto_id):
    objeto = Objeto.query.get_or_404(objeto_id)

    if request.method == "POST":
        try:
            objeto.nombre = request.form["nombre"]
            objeto.categoria = request.form.get("categoria")
            objeto.ubicacion = request.form.get("ubicacion")

            # Manejo de foto
            if "foto" in request.files:
                file = request.files["foto"]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    objeto.foto = filename

            db.session.commit()
            flash(f"Objeto '{objeto.nombre}' editado correctamente.", "success")
            return redirect(url_for("objetos.inicio"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al editar objeto: {e}", "danger")
            return redirect(url_for("objetos.editar", objeto_id=objeto_id))

    return render_template("editar.html", objeto=objeto)

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

    return jsonify({"mensaje": f"Objeto {obj.nombre} eliminado"})




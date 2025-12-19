from flask import Blueprint, request, jsonify, current_app, url_for
from .. import db
from .. blueprints.objetos import Objeto
import os

api_bp = Blueprint('api_objetos', __name__, url_prefix='/objetos/api')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Listar objetos
@api_bp.route('/', methods=['GET'])
def listar_objetos():
    objetos = Objeto.query.all()
    resultado = []
    for obj in objetos:
        resultado.append({
            'id': obj.id,
            'nombre': obj.nombre,
            'categoria': obj.categoria,
            'ubicacion': obj.ubicacion,
            'cantidad': obj.cantidad,
            'foto': url_for('static', filename=f'uploads/{obj.foto}', _external=True) if obj.foto else None
        })
    return jsonify(resultado), 200

# Crear objeto
@api_bp.route("", methods=["POST"])
def crear_objeto():
    data = request.get_json()

    if not data:
        return {"error": "JSON vacío"}, 400

    nombre = data.get("nombre")
    if not nombre:
        return {"error": "El campo 'nombre' es obligatorio"}, 400

    obj = Objeto(
        nombre=nombre,
        categoria=data.get("categoria"),
        ubicacion=data.get("ubicacion"),
        cantidad=data.get("cantidad", 1)
    )

    db.session.add(obj)
    db.session.commit()

    return {
        "id": obj.id,
        "nombre": obj.nombre
    }, 201

#Obtener objeto por ID
@api_bp.route("/<int:objeto_id>", methods=["GET"])
def obtener_objeto(objeto_id):
    obj = Objeto.query.get_or_404(objeto_id)

    return {
        "id": obj.id,
        "nombre": obj.nombre,
        "categoria": obj.categoria,
        "ubicacion": obj.ubicacion,
        "cantidad": obj.cantidad,
        "foto": obj.foto
    }


# Modificar cantidad
@api_bp.route("/<int:objeto_id>/cantidad", methods=["PATCH"])
def modificar_cantidad(objeto_id):
    obj = Objeto.query.get_or_404(objeto_id)
    data = request.get_json()

    accion = data.get("accion")
    valor = int(data.get("valor", 1))

    if accion not in ("sumar", "restar"):
        return {"error": "Acción no válida"}, 400

    if valor < 1:
        return {"error": "Valor inválido"}, 400

    if accion == "sumar":
        obj.cantidad += valor
    else:
        obj.cantidad = max(0, obj.cantidad - valor)

    db.session.commit()

    return {
        "id": obj.id,
        "cantidad": obj.cantidad
    }

# Eliminar objeto
@api_bp.route("/<int:objeto_id>", methods=["DELETE"])
def eliminar_objeto(objeto_id):
    obj = Objeto.query.get_or_404(objeto_id)

    db.session.delete(obj)
    db.session.commit()

    return {"mensaje": "Objeto eliminado"}

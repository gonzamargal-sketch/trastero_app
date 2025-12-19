import requests

# URL base de la API de objetos
BASE_URL = "http://127.0.0.1:5000/objetos/api"

def listar_objetos():
    r = requests.get(BASE_URL)
    if r.ok:
        print("Lista de objetos:")
        for obj in r.json():
            print(f"{obj['id']}: {obj['nombre']} - Cantidad: {obj['cantidad']}")
    else:
        print("Error al listar objetos:", r.status_code, r.text)

def crear_objeto():
    data = {
        "nombre": "Caja de herramientas",
        "categoria": "Herramientas",
        "ubicacion": "Estantería A",
        "cantidad": 3,
        "notas": "Caja pesada"
    }
    r = requests.post(BASE_URL, json=data)
    if r.ok:
        print("Objeto creado:", r.json())
        return r.json()["id"]
    else:
        print("Error al crear objeto:", r.status_code, r.text)
        return None

def modificar_cantidad(objeto_id, accion, valor):
    data = {"accion": accion, "valor": valor}
    r = requests.patch(f"http://127.0.0.1:5000/objetos/api/{objeto_id}/cantidad", json=data)
    if r.ok:
        print(f"Cantidad modificada ({accion} {valor}):", r.json())
    else:
        print("Error al modificar cantidad:", r.status_code, r.text)

def eliminar_objeto(objeto_id):
    r = requests.delete(f"http://127.0.0.1:5000/objetos/api/{objeto_id}")
    if r.ok:
        print("Objeto eliminado:", r.json())
    else:
        print("Error al eliminar objeto:", r.status_code, r.text)

if __name__ == "__main__":
    # 1. Listar objetos existentes
    listar_objetos()

    # 2. Crear un objeto nuevo
    objeto_id = crear_objeto()
    if objeto_id is None:
        exit()

    # 3. Sumar 2 unidades al objeto
    modificar_cantidad(objeto_id, "sumar", 2)

    # 4. Restar 1 unidad al objeto
    modificar_cantidad(objeto_id, "restar", 1)

    # 5. Eliminar el objeto
    eliminar_objeto(objeto_id)

    # 6. Listar objetos finales
    listar_objetos()


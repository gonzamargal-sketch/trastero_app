import requests

BASE_URL = "http://127.0.0.1:5000/objetos/api"


# ========= FUNCIONES =========

def listar_objetos():
    print("📋 Listando objetos...")
    r = requests.get(BASE_URL)
    if r.ok:
        for obj in r.json():
            print(obj)
    else:
        print("❌ Error:", r.status_code, r.text)


def crear_objeto():
    print("➕ Creando objeto...")
    data = {
        "nombre": "Caja de pruebas",
        "categoria": "Test",
        "ubicacion": "Estantería Z",
        "cantidad": 2
    }

    r = requests.post(BASE_URL, json=data)
    if r.ok:
        obj = r.json()
        print("✅ Objeto creado:", obj)
        return obj["id"]
    else:
        print("❌ Error:", r.status_code, r.text)


def obtener_objeto(objeto_id):
    print(f"🔍 Obteniendo objeto {objeto_id}...")
    r = requests.get(f"{BASE_URL}/{objeto_id}")
    if r.ok:
        print("✅ Objeto:", r.json())
    else:
        print("❌ Error:", r.status_code, r.text)


def modificar_cantidad(objeto_id, accion, valor):
    print(f"✏️ {accion.upper()} {valor} unidades...")
    data = {
        "accion": accion,
        "valor": valor
    }

    r = requests.patch(f"{BASE_URL}/{objeto_id}/cantidad", json=data)
    if r.ok:
        print("✅ Resultado:", r.json())
    else:
        print("❌ Error:", r.status_code, r.text)


def eliminar_objeto(objeto_id):
    print(f"🗑 Eliminando objeto {objeto_id}...")
    r = requests.delete(f"{BASE_URL}/{objeto_id}")
    if r.ok:
        print("✅ Eliminado:", r.json())
    else:
        print("❌ Error:", r.status_code, r.text)


# ========= EJECUCIÓN CONTROLADA =========

if __name__ == "__main__":

    # 1️⃣ Listar objetos
    #listar_objetos()

    # 2️⃣ Crear objeto
    #objeto_id = crear_objeto()

    # ⚠️ COPIA EL ID QUE IMPRIME Y PÉGALO AQUÍ
    objeto_id = 3

    # 3️⃣ Obtener objeto
    #obtener_objeto(objeto_id)

    # 4️⃣ Sumar cantidad
    #modificar_cantidad(objeto_id, "sumar", 3)

    # 5️⃣ Restar cantidad
    #modificar_cantidad(objeto_id, "restar", 1)

    # 6️⃣ Eliminar objeto
    eliminar_objeto(objeto_id)

    # 7️⃣ Listar objetos finales
    # listar_objetos()


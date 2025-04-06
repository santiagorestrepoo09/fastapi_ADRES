from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data.json"

# Inicializar el archivo data.json con la estructura adecuada
def inicializar_archivo():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({"adquisiciones": [], "eventos": []}, file, indent=4, ensure_ascii=False)

inicializar_archivo()

# Modelo de datos para adquisiciones
class Adquisicion(BaseModel):
    presupuesto: str
    unidad: str
    tipo_bien_servicio: str
    cantidad: int
    valor_unitario: float
    valor_total: float
    fecha_adquisicion: str  
    proveedor: str
    estado: str 
    documentacion: str
    numero_orden: str
    factura: str

# Modelo de datos para eventos
class Evento(BaseModel):
    factura: str
    tipo_evento: str
    descripcion: str
    datos_afectados: dict = None

# Función para guardar adquisiciones en JSON
def guardar_dato(data):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)
    contenido["adquisiciones"].append(data)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)

# Función para agregar eventos al JSON
def agregar_evento(factura,tipo_evento, descripcion, datos_afectados=None):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)

    evento = {
        "factura": factura,
        "fecha_hora": datetime.datetime.now().isoformat(),
        "tipo_evento": tipo_evento,
        "descripcion": descripcion,
        "datos_afectados": datos_afectados,
    }
    contenido["eventos"].append(evento)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)

# Endpoint POST para guardar adquisición
@app.post("/adquisiciones")
def crear_adquisicion(item: Adquisicion):
    guardar_dato(item.dict())
    factura = item.factura
    agregar_evento(factura, "creación", "Se creó una nueva adquisición.", item.dict())
    return {"mensaje": "Adquisición registrada exitosamente", "datos": item}

# Endpoint PUT para actualizar el estado (activo/inactivo)
@app.put("/adquisiciones/{indice}/estado")
def actualizar_estado(indice: int, nuevo_estado: str):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)

    if indice < 0 or indice >= len(contenido["adquisiciones"]):
        raise HTTPException(status_code=404, detail="Índice fuera de rango.")

    contenido["adquisiciones"][indice]["estado"] = nuevo_estado

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)

    agregar_evento(
        "actualización",
        f"Se actualizó el estado de la adquisición en el índice {indice}.",
        {"estado_nuevo": nuevo_estado}
    )

    return {
        "mensaje": f"Estado actualizado correctamente a '{nuevo_estado}'",
        "registro_actualizado": contenido["adquisiciones"][indice]
    }

# Endpoint GET para obtener todas las adquisiciones
@app.get("/adquisiciones")
def obtener_adquisiciones():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)
    return contenido.get("adquisiciones", [])

# Endpoint DELETE para eliminar una adquisición por índice
@app.delete("/adquisiciones/{indice}")
def eliminar_adquisicion(indice: int):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)

    if indice < 0 or indice >= len(contenido["adquisiciones"]):
        raise HTTPException(status_code=404, detail="Índice fuera de rango.")

    eliminado = contenido["adquisiciones"].pop(indice)
    factura = eliminado.get("factura", "Factura no disponible")

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)

    agregar_evento(
        factura,
        "eliminación",
        f"Se eliminó la adquisición en el índice {indice}.",
        eliminado
    )

    return {
        "mensaje": "Registro eliminado correctamente.",
        "registro_eliminado": eliminado
    }

# Endpoint PUT para actualizar la adquisición completa
@app.put("/adquisiciones/{indice}")
def actualizar_adquisicion(indice: int, item: Adquisicion):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)

    if indice < 0 or indice >= len(contenido["adquisiciones"]):
        raise HTTPException(status_code=404, detail="Índice fuera de rango.")

    actualziaco = contenido["adquisiciones"].pop(indice)
    contenido["adquisiciones"][indice] = item.dict()
    factura = actualziaco.get("factura", "Factura no disponible")
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)

    agregar_evento(
            factura,
            "Actualización",
            f"Se actualizo la adquisición en el índice {indice}.",
            actualziaco
        )

    return {
        "mensaje": "Adquisición actualizada correctamente.",
        "registro_actualizado": contenido["adquisiciones"][indice]
    }

# Endpoint POST para registrar un evento manualmente
@app.post("/eventos")
def crear_evento(evento: Evento):
    agregar_evento(evento.factura, evento.tipo_evento, evento.descripcion, evento.datos_afectados)
    return {"mensaje": "Evento registrado exitosamente", "evento": evento}

# Endpoint GET para obtener todos los eventos
@app.get("/eventos")
def obtener_eventos():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        contenido = json.load(file)
    return contenido.get("eventos", [])
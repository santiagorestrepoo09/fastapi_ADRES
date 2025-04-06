# API de Gestión de Adquisiciones y Eventos

Este proyecto es una API desarrollada con **FastAPI** para gestionar adquisiciones y registrar eventos relacionados. La API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre adquisiciones y registrar eventos en un archivo JSON.

## Características

- Gestión de adquisiciones (crear, leer, actualizar, eliminar).
- Registro de eventos relacionados con las adquisiciones.
- Validación automática de datos usando **Pydantic**.
- Documentación automática generada por **FastAPI**.
- Soporte para CORS (Cross-Origin Resource Sharing).

---

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.9 o superior**: [Descargar Python](https://www.python.org/downloads/)
- **Pip**: Administrador de paquetes de Python (viene con Python).
- **Virtualenv** (opcional): Para crear un entorno virtual.

---

## Configuración del proyecto

 1. Clonar el repositorio

Clona este repositorio en tu máquina local:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```
2. Crear un entorno virtual
Crea un entorno virtual para aislar las dependencias del proyecto:
```bash
python -m venv venv
```
Activa el entorno virtual:
```bash
venv\Scripts\activate
```
3. Instalar dependencias
Instala las dependencias necesarias desde el archivo requirements.txt:
```bash
pip install -r requirements.txt
```

Ejecución del proyecto
1. Inicializar el archivo data.json
El proyecto utiliza un archivo data.json para almacenar adquisiciones y eventos. Si el archivo no existe, se creará automáticamente con la estructura inicial
{
  "adquisiciones": [],
  "eventos": []
}
2. Ejecutar el servidor
Inicia el servidor FastAPI con Uvicorn:
```bash
uvicorn main:app --reload
```
El servidor estará disponible en: http://127.0.0.1:8000
La documentación interactiva estará en:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

--------------------------------------------------------------------------

Endpoints disponibles
Adquisiciones
1. Crear una adquisición
  POST /adquisiciones
  Body:
  {
    "presupuesto": "2000000000",
    "unidad": "Dirección de Medicamentos y Tecnologías en Salud",
    "tipo_bien_servicio": "Medicamentos",
    "cantidad": 1000,
    "valor_unitario": 5800.0,
    "valor_total": 5800000.0,
    "fecha_adquisicion": "2024-09-30",
    "proveedor": "Formación Empresarial Ltda.",
    "estado": "activo",
    "documentacion": "contrato de adquisicion",
    "numero_orden": "2024-09-30-001",
    "factura": "2024-09-30-001"

2. Obtener todas las adquisiciones
  GET /adquisiciones

3. Actualizar el estado de una adquisición
PUT /adquisiciones/{indice}/estado
Body:
  {
    "nuevo_estado": "inactivo"
  }

   
4. Actualizar una adquisición completa
PUT /adquisiciones/{indice}
Body: Igual al modelo de creación.

5. Eliminar una adquisición
DELETE /adquisiciones/{indice}


Eventos
1. Registrar un evento manualmente
POST /eventos
Body:
{
  "factura": "2024-09-30-001",
  "tipo_evento": "actualización",
  "descripcion": "Se actualizó el estado de la adquisición.",
  "datos_afectados": {
    "estado_anterior": "activo",
    "estado_nuevo": "inactivo"
  }
}

2. Obtener todos los eventos
GET /eventos

c:\Users\David Santiago\OneDrive\Escritorio\DEVELOP\PYTHON\API ADRES\
│
├── [main.py](http://_vscodecontentref_/0)               # Código principal de la API
├── [data.json](http://_vscodecontentref_/1)             # Archivo de datos (adquisiciones y eventos)
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto

Dependencias principales
FastAPI: Framework para construir APIs rápidas y modernas.
Uvicorn: Servidor ASGI para ejecutar la aplicación.
Pydantic: Validación y gestión de modelos de datos.

Autor
David Santiago
Desarrollador Python
GitHub | LinkedIn

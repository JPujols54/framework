from server.server import HTTPServer
from server.router import Router
from core.exception import (
    BadRequestError,
    UnauthorizedError
)
from datetime import datetime

app = Router(static_dir="public")

@app.get("/")
def home(request):
    return "public/index.html"

@app.get("/contacto")
def contacto(request):
    return "public/contacto.html"

@app.get("/users/{user_id}")
def get_user(req, user_id: int, active: bool = True, page: int = 1): 
    return {
        "user_id": user_id,
        "activate": active,
        "page": page
    }

@app.get("/usuarios/{id}")
def obtener_usuario(request):
    user_id = request.params.get("id")
    return {"id": user_id, "nombre": f"Usuario {user_id}", "rol": "Admin"}

@app.get("/productos/{categoria}/{id}")
def detalle_producto(request,categoria,id):
    categoria = request.params.get("categoria")
    producto_id = request.params.get("id")
    
    return {
        "categoria": categoria,
        "producto_id": producto_id,
        "stock": 15
    }

@app.get("/buscar")
def buscar_productos(request):
    categoria = request.query_params.get("categoria", "todas")
    limite = request.query_params.get("limite", "10")   
    return f"<h1>Búsqueda de {categoria}</h1><p>Mostrando {limite} resultados.</p>"

@app.get("/hora")
def hora(request):
    ahora = datetime.now()
    fecha_json = {
    "año": ahora.year,
    "mes": ahora.month,
    "día": ahora.day,
    "hora": ahora.hour,
    "minuto": ahora.minute,
    "segundo": ahora.second,
    "microsegundo": ahora.microsecond
    }
    return fecha_json

@app.get("/register")
def register(request):
    return "public/register.html"

@app.post("/api/login")
def login_handler(request):
    usuario = request.data.get("usuario")
    password = request.data.get("password")

    try:
        with open("usuarios_logueados.txt", "a", encoding="utf-8") as archivo:
            # Escribimos los datos en formato texto o JSON
            registro = f"Usuario: {usuario} | Password: {password}\n"
            archivo.write(registro)

        return {
            "status": "success",
            "mensaje": f"Bienvenido {usuario}, tu acceso quedó registrado.",
        }

    except Exception as e:
        return {
            "status": "error",
            "mensaje": f"Error al guardar en BD: {str(e)}",
        }

@app.get("/upload")
def upload_page(request):
    return "public/upload.html"

# Endpoint que recibe y procesa el archivo enviado
@app.post("/api/v1/files/upload")
def upload_large_file(request):
    data = request.data

if __name__ == "__main__":
    server = HTTPServer(app_handler=app)
    server.start(host="127.0.0.1", port=8080)
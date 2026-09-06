import requests

def test_usuario_login():
    # URL de tu servidor en ejecución (ajusta el puerto si usas otro, ej: 8080)
    url = "http://127.0.0.1:8080/api/login"
    
    # 1. El usuario ingresa sus datos
    datos_usuario = {
        "usuario": "admin",
        "password": "1234password"
    }

    print(f"[*] Enviando petición POST a {url}...")

    # 2. El cliente/usuario hace la petición POST
    respuesta = requests.post(url, json=datos_usuario)

    # 3. Imprimimos los resultados recibidos desde tu servidor
    print(f"[*] Código de Estado HTTP: {respuesta.status_code}")
    print(f"[*] Respuesta del servidor: {respuesta.text}")

    # 4. Validamos que el servidor devuelva el usuario correctamente
    assert respuesta.status_code == 200, f"Error: Se esperaba status 200 pero llegó {respuesta.status_code}"
    assert respuesta.text == "admin", f"Error: Se esperaba 'admin' pero llegó '{respuesta.text}'"
    
    print("\n[✔] Test completado con éxito: El usuario hizo el POST y recibió la respuesta correcta.")

# Ejecutar la función de prueba directamente
if __name__ == "__main__":
    test_usuario_login()
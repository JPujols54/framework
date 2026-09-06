import sys
import requests


class CORSTester:
    """Cliente de pruebas para verificar el soporte de CORS y Preflight OPTIONS en un servidor HTTP."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def probar_preflight_options(self, endpoint: str) -> bool:
        """Simula la solicitud Preflight que envía el navegador antes de un POST con JSON."""
        url = f"{self.base_url}{endpoint}"
        print(f"\n[1] Probando Solicitud OPTIONS (Preflight) en: {url}")

        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, Authorization",
        }

        try:
            # Petición OPTIONS explícita
            response = requests.options(url, headers=headers, timeout=3)

            print(f"    -> Código de Estado: {response.status_code}")
            print("    -> Encabezados recibidos:")
            for k, v in response.headers.items():
                if "access-control" in k.lower():
                    print(f"       - {k}: {v}")

            # Validaciones de cumplimiento
            es_valido = True
            if response.status_code not in (200, 204):
                print(
                    "    ❌ ERROR: El estado debió ser 204 No Content o 200 OK"
                )
                es_valido = False

            if (
                "Access-Control-Allow-Origin" not in response.headers
                or response.headers.get("Access-Control-Allow-Origin") != "*"
            ):
                print(
                    "    ❌ ERROR: Falta 'Access-Control-Allow-Origin: *' en la respuesta OPTIONS"
                )
                es_valido = False

            if "Access-Control-Allow-Methods" not in response.headers:
                print(
                    "    ❌ ERROR: Falta 'Access-Control-Allow-Methods' en la respuesta OPTIONS"
                )
                es_valido = False

            if "Access-Control-Allow-Headers" not in response.headers:
                print(
                    "    ❌ ERROR: Falta 'Access-Control-Allow-Headers' en la respuesta OPTIONS"
                )
                es_valido = False

            if es_valido:
                print("    ✅ ÉXITO: El Preflight OPTIONS responde correctamente")

            return es_valido

        except requests.exceptions.ConnectionError:
            print(
                f"    ❌ ERROR CRÍTICO: No se pudo conectar con el servidor en {self.base_url}. ¿Está encendido?"
            )
            return False

    def probar_peticion_post_cors(
        self, endpoint: str, payload: dict
    ) -> bool:
        """Simula la solicitud POST real enviada por un navegador tras validar el Preflight."""
        url = f"{self.base_url}{endpoint}"
        print(f"\n[2] Probando Solicitud POST real con JSON en: {url}")

        headers = {
            "Origin": "http://localhost:3000",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=3
            )

            print(f"    -> Código de Estado: {response.status_code}")
            print(f"    -> Respuesta del Servidor: {response.text}")
            print(
                f"    -> Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NO ENCONTRADO')}"
            )

            es_valido = True
            if response.headers.get("Access-Control-Allow-Origin") != "*":
                print(
                    "    ❌ ERROR: La respuesta POST no contiene el encabezado 'Access-Control-Allow-Origin: *'"
                )
                es_valido = False

            if es_valido:
                print(
                    "    ✅ ÉXITO: La solicitud POST incluye los permisos CORS necesarios"
                )

            return es_valido

        except requests.exceptions.ConnectionError:
            print("    ❌ ERROR: Fallo de conexión durante el POST")
            return False


# =====================================================================
# EJECUCIÓN DE LAS PRUEBAS
# =====================================================================
if __name__ == "__main__":
    # 1. Instanciar el cliente con la dirección de tu servidor
    cliente = CORSTester("http://127.0.0.1:8080")

    print("==================================================")
    print(" INICIANDO TEST DE INTEGRACIÓN: CORS & OPTIONS")
    print("==================================================")

    # 2. Llamada a la prueba de Preflight OPTIONS
    test_1 = cliente.probar_preflight_options("/api/login")

    # 3. Llamada a la prueba de Petición POST real con JSON
    test_2 = cliente.probar_peticion_post_cors(
        "/api/login",
        payload={"usuario": "admin", "password": "123"},
    )

    print("\n==================================================")
    if test_1 and test_2:
        print(" 🎉 RESULTADO FINAL: Tu servidor maneja CORS y OPTIONS correctamente.")
    else:
        print(" ⚠️ RESULTADO FINAL: Hay fallas en la configuración de CORS u OPTIONS.")
    print("==================================================")
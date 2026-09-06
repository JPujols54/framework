import socket
import time
from core.logger import logger
from concurrent.futures import ThreadPoolExecutor
from .http_utils import HTTPRequest, HTTPResponse 
from .exception import InternalServerError
class HTTPServer:
    def __init__(self, app_handler=None, max_workers: int = 20, timeout: float = 5.0, max_requests: int = 100):
        self.host = None
        self.port = None
        self.app_handler = app_handler 
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.timeout = timeout
        self.max_requests = max_requests

    def _process_client(self, client_socket: socket.socket, client_address):
        start_time = time.time()
        client_socket.settimeout(self.timeout)
        requests_count = 0
        keep_alive = True
        try:
            while keep_alive and requests_count < self.max_requests:
                try:
                    raw_data = client_socket.recv(4096)
                    if not raw_data:
                        break
                except (socket.timeout, TimeoutError):
                    break
                except ConnectionResetError:
                    break
                request = HTTPRequest(raw_data)
                if request.headers["connection"] == False:
                    keep_alive = False

                requests_count += 1
                remaining = self.max_requests - requests_count
                conn_header = request.headers.get("connection", "").lower() if hasattr(request, "headers") else ""
                if conn_header == "close" or remaining <= 0:
                    keep_alive = False

                if self.app_handler:
                    response = self.app_handler.handle_request(request)
                else:
                    response = HTTPResponse(estatus_code="200 OK", body=b"<h1>Server OK</h1>")
                elapsed_ms = (time.time() - start_time) * 1000

                logger.info(
                    f"{client_address[0]} - '{request.method} {request.path}' "
                    f"{response.estatus_code} ({elapsed_ms:.2f}ms)"
                )
                
                if keep_alive:
                    response.headers["connection"] = "keep-alive"
                    response.headers["keep-Alive"] = (
                        f"timeout={int(self.timeout)}, max={remaining}"
                    )
                else:
                    response.headers["connection"] = "close"
                
                client_socket.sendall(response.respuesta_http())

        except Exception as e:
            print(f"[ERROR] Error procesando cliente {client_address}: {e}")
            try:
                err_response = InternalServerError().to_response()
                err_response.headers["Connection"] = "close"
                client_socket.sendall(err_response.respuesta_http())
            except Exception:
                pass
            finally:
                client_socket.close()

    def start(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server.bind((self.host, self.port))
            server.listen(5)
            print(f"[*] Servidor escuchando en http://{self.host}:{self.port}")
            while True:
                client_socket, client_address = server.accept()
                self.executor.submit(self._process_client, client_socket, client_address)

        except KeyboardInterrupt:
            print("\n[*] Deteniendo servidor...")
        finally:
            server.close()
            self.executor.shutdown(wait=True)
            print("[*] Servidor detenido de manera limpia.")
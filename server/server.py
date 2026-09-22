import socket
import time
from concurrent.futures import ThreadPoolExecutor
from core.logger import logger
from .parser import HTTPRequestParser
from .response import HTTPResponse
from core.exception import InternalServerError

class HTTPServer:
    """Abre sockets TCP, administra concurrencia de clientes y envía respuestas de red."""
    def __init__(self, app_handler=None, max_workers: int = 20, timeout: float = 5.0, max_requests: int = 100):
        self.app_handler = app_handler
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.timeout = timeout
        self.max_requests = max_requests

    def start(self, host: str = "127.0.0.1", port: int = 8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server.bind((host, port))
            server.listen(128)
            print(f"[*] Servidor escuchando en http://{host}:{port}")
            while True:
                client_socket, client_address = server.accept()
                self.executor.submit(self._process_client, client_socket, client_address)
        except KeyboardInterrupt:
            print("\n[*] Apagando servidor...")
        finally:
            server.close()
            self.executor.shutdown(wait=True)

    def _process_client(self, client_socket: socket.socket, client_address: tuple):
        client_socket.settimeout(self.timeout)
        requests_count = 0

        try:
            while requests_count < self.max_requests:
                raw_data = client_socket.recv(4096)
                if not raw_data:
                    break

                request = HTTPRequestParser.parse(raw_data)
                requests_count += 1
                
                start_time = time.time()
                response = self._get_response(request)

                keep_alive = self._should_keep_alive(request, requests_count)
                self._apply_connection_headers(response, keep_alive, requests_count)

                client_socket.sendall(response.to_bytes())

                elapsed_ms = (time.time() - start_time) * 1000
                logger.info(
                    f"{client_address[0]} - '{request.method} {request.path}' "
                    f"{response.status_code} ({elapsed_ms:.2f}ms)"
                )

                if not keep_alive:
                    break

        except (socket.timeout, ConnectionResetError):
            pass
        except Exception as e:
            logger.error(f"Error procesando cliente {client_address}: {e}")
            self._send_error_response(client_socket)
        finally:
            client_socket.close()

    def _get_response(self, request) -> HTTPResponse:
        if self.app_handler:
            return self.app_handler.handle_request(request)
        return HTTPResponse(status_code="200 OK", body=b"<h1>Server OK</h1>")

    def _should_keep_alive(self, request, count: int) -> bool:
        conn = request.headers.get("connection", "").lower()
        if conn == "close" or count >= self.max_requests:
            return False
        return conn == "keep-alive" or request.version == "HTTP/1.1"

    def _apply_connection_headers(self, response: HTTPResponse, keep_alive: bool, count: int):
        if keep_alive:
            response.set_header("Connection", "keep-alive")
            response.set_header("Keep-Alive", f"timeout={int(self.timeout)}, max={self.max_requests - count}")
        else:
            response.set_header("Connection", "close")

    def _send_error_response(self, client_socket: socket.socket):
        try:
            err_response = InternalServerError().to_response()
            err_response.set_header("Connection", "close")
            client_socket.sendall(err_response.to_bytes())
        except Exception:
            pass
import socket
from concurrent.futures import ThreadPoolExecutor
from .http import HTTPRequest, HTTPResponse
from .router import Router

class HTTPServer:
    def __init__(self, max_workers: int = 20):
        self.host = None
        self.port = None
        self.router = Router()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def _process_client(self, client_socket: socket.socket, client_address):
        try:
            client_socket.settimeout(5.0)
            raw_data = client_socket.recv(4096)
            if raw_data:
                request = HTTPRequest(raw_data)
                response = self.router.handle_request(request)
                client_socket.sendall(response.to_bytes())
        except socket.timeout:
            pass
        except Exception as e:
            print(f"[ERROR] Error procesando cliente {client_address}: {e}")
            err_res = HTTPResponse(status_code=500, body=b"<h1>500 Internal Error</h1>")
            client_socket.sendall(err_res.to_bytes())
        finally:
            client_socket.close()

    def start(self, host: str = "127.0.0.1", port: int = 8080): 
        self.host = host
        self.port = port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(20)
            try:
                while True:
                    client_socket, client_address = server_socket.accept()
                    self.executor.submit(self._process_client, client_socket, client_address)
            except KeyboardInterrupt:
                print("\n[*] Apagando servidor...")
                self.executor.shutdown(wait=False)
from .http_utils import HTTPRequest, HTTPResponse
from pathlib import Path
from .factory.fabric_res import FabricRes
from .exception import (
    MethodNotAllowedError,
    NotFoundError,
)
import re
class Router:
    def __init__(self, static_dir: str = "public"):
        self.routes = {
            "GET": [],
            "POST": [],
            "PUT": [],
            "DELETE": []
        }
        self.static_dir = Path(static_dir).resolve()
        self.middlewares = []

    def _path_to_regex(self, path: str):
        pattern = re.sub(r'\{([^}/]+)\}', r'(?P<\1>[^/]+)', path)
        return re.compile(f"^{pattern}$")

    def use(self,middlefunc):
        self.middlewares.append(middlefunc)

    def add_route(self, method: str, path: str, handler):
        method = method.upper()
        if method in self.routes:
            regex_pattern = self._path_to_regex(path)
            self.routes[method].append({
                "pattern": regex_pattern,
                "handler": handler,
                "path": path
            })
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")

    def get(self, path: str):
        def decorator(handler):
            self.add_route("GET", path, handler)
            return handler
        return decorator

    def post(self, path: str):
        def decorator(handler):
            self.add_route("POST", path, handler)
            return handler
        return decorator

    def put(self, path: str):
        def decorator(handler):
            self.add_route("PUT", path, handler)
            return handler
        return decorator

    def delete(self, path: str):
        def decorator(handler):
            self.add_route("DELETE", path, handler)
            return handler
        return decorator

    def _inyectar_cors(self, response: HTTPResponse) -> HTTPResponse:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization"
        )
        return response

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        if request.method == "OPTIONS":
            response = HTTPResponse(
                estatus_code="204 No Content",
                content_type="text/plain",
                body=b"",
            )
            return self._inyectar_cors(response)
        
        method = request.method
        path = request.path
        def core_handler(req :  HTTPRequest) -> HTTPResponse:     
            if method in self.routes:
                for route in self.routes[method]:
                    match = route["pattern"].match(path)
                    if match:
                        req.params = match.groupdict()
                        handler = route["handler"]
                        resultado = handler(req)
                        if isinstance(resultado, HTTPResponse):
                            return resultado
                        return FabricRes.auto(resultado)

            for m in self.routes:
                if m != method:
                    for route in self.routes[m]:
                        if route["pattern"].match(path):
                            raise MethodNotAllowedError(f"El método {method} no está permitido para {path}")
            if method == "GET":
                relative_path = path.lstrip("/")
                file_path = (self.static_dir / relative_path).resolve()

                if file_path.is_relative_to(self.static_dir) and file_path.exists() and file_path.is_file():
                        return FabricRes.auto(str(file_path))
                raise NotFoundError(f"La ruta '{path}' no fue encontrada")

        def dispatch(indice: int,req: HTTPRequest) -> HTTPResponse:
            if indice < len(self.middlewares):
                middleware = self.middlewares[indice]
                return middleware(req, lambda r: dispatch(indice + 1, r))
            else:
                return core_handler(req)
        respuesta = dispatch(0,request)
        return self._inyectar_cors(respuesta)
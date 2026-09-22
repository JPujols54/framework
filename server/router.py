import re
from .request import HTTPRequest
from .response import HTTPResponse
from .pipeline import MiddlewarePipeline
from .factory import FabricRes
from .static import StaticFilesHandler
from core.exception import MethodNotAllowedError, NotFoundError
from .argument_resolver import ArgumentResolver  # Importamos la Factory/Resolver

class Router:
    """Gestiona el mapeo de URL y delega la ejecución al pipeline."""
    def __init__(self, static_dir: str = "public"):
        self.routes = {
            "GET": [], "POST": [], "PUT": [], "DELETE": []
        }
        self.pipeline = MiddlewarePipeline()
        self.static_handler = StaticFilesHandler(static_dir)

    def use(self, middleware_fn):
        self.pipeline.use(middleware_fn)

    def add_route(self, method: str, path: str, handler):
        method = method.upper()
        if method not in self.routes:
            raise ValueError(f"Método HTTP no soportado: {method}")

        pattern_str = re.sub(r'\{([^}/]+)\}', r'(?P<\1>[^/]+)', path)
        pattern = re.compile(f"^{pattern_str}$")
        self.routes[method].append({"pattern": pattern, "handler": handler})

    def get(self, path: str): return lambda h: self.add_route("GET", path, h) or h
    def post(self, path: str): return lambda h: self.add_route("POST", path, h) or h
    def put(self, path: str): return lambda h: self.add_route("PUT", path, h) or h
    def delete(self, path: str): return lambda h: self.add_route("DELETE", path, h) or h

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        def core_dispatch(req: HTTPRequest) -> HTTPResponse:
            handler = self._resolve_handler(req)
            if handler:
                kwargs = ArgumentResolver.resolve_kwargs(handler, req)
                res = handler(req,**kwargs)
                return res if isinstance(res, HTTPResponse) else FabricRes.auto(res)

            static_res = self.static_handler.serve(req)
            if static_res:
                return static_res

            self._check_method_allowed(req)
            raise NotFoundError(f"La ruta '{req.path}' no fue encontrada")

        return self.pipeline.execute(request, core_dispatch)

    def _resolve_handler(self, request: HTTPRequest):
        for route in self.routes.get(request.method, []):
            match = route["pattern"].match(request.path)
            if match:
                request.params = match.groupdict()
                return route["handler"]
        return None

    def _check_method_allowed(self, request: HTTPRequest):
        for m, routes in self.routes.items():
            if m != request.method:
                for r in routes:
                    if r["pattern"].match(request.path):
                        raise MethodNotAllowedError(f"El método {request.method} no está permitido para {request.path}")
from .request import HTTPRequest
from .response import HTTPResponse

class MiddlewarePipeline:
    """Administra y ejecuta el flujo encadenado de middlewares."""
    def __init__(self):
        self._middlewares = []

    def use(self, middleware_fn):
        self._middlewares.append(middleware_fn)

    def execute(self, request: HTTPRequest, target_handler) -> HTTPResponse:
        def dispatch(index: int, req: HTTPRequest) -> HTTPResponse:
            if index < len(self._middlewares):
                current = self._middlewares[index]
                return current(req, lambda r: dispatch(index + 1, r))
            return target_handler(req)

        return dispatch(0, request)
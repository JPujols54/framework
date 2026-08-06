from pathlib import Path
from http import HTTPRequest, HTTPResponse

class Router:
    def __init__(self,static_dir: str = "static"):
        self.routes = {}
        self.static_dir = Path(static_dir)

    def add_route(self, method: str, path: str, handler):
        self.routes[(method.upper(), path)] = handler

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        handler = self.routes.get((request.method.upper(), request.path))
        if handler:
            return handler(request)
        if request.method == "GET":
            relative_path = request.path.lstrip("/")
            if not relative_path:
                relative_path = "index.html"
            target_file = self.static_dir / relative_path
            return HTTPResponse.from_file(target_file)
        return HTTPResponse(status_code=404, body=b"<h1>404 Not Found</h1>")
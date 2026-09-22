from pathlib import Path
from .request import HTTPRequest
from .response import HTTPResponse
from .factory import FabricRes

class StaticFilesHandler:
    """Maneja la resolución y entrega de archivos estáticos."""
    def __init__(self, static_dir: str = "public"):
        self.static_dir = Path(static_dir).resolve()

    def serve(self, request: HTTPRequest) -> HTTPResponse | None:
        if request.method != "GET":
            return None

        relative_path = request.path.lstrip("/")
        file_path = (self.static_dir / relative_path).resolve()

        if file_path.is_relative_to(self.static_dir) and file_path.exists() and file_path.is_file():
            return FabricRes.auto(str(file_path))
        
        return None
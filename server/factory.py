import json
from pathlib import Path
from .response import HTTPResponse

class CreadorRespuesta:
    def crear(self, datos, status: str) -> HTTPResponse:
        raise NotImplementedError

class CreadorJSON(CreadorRespuesta):
    def crear(self, datos, status: str) -> HTTPResponse:
        return HTTPResponse(
            status_code=status,
            content_type="application/json; charset=utf-8",
            body=json.dumps(datos)
        )

class CreadorArchivo(CreadorRespuesta):
    MIME_TYPES = {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".svg": "image/svg+xml; charset=utf-8",
    }

    def crear(self, datos: str, status: str) -> HTTPResponse:
        path = Path(datos)
        if path.is_file():
            ext = path.suffix.lower()
            mime = self.MIME_TYPES.get(ext, "application/octet-stream")
            return HTTPResponse(status_code=status, content_type=mime, body=path.read_bytes())
        return HTTPResponse(status_code=status, content_type="text/html; charset=utf-8", body=datos)

class FabricRes:
    _CREADORES = {
        dict: CreadorJSON(),
        list: CreadorJSON(),
        str: CreadorArchivo(),
    }

    @classmethod
    def auto(cls, datos, status: str = "200 OK") -> HTTPResponse:
        creador = cls._CREADORES.get(type(datos))
        if not creador:
            raise TypeError(f"Sin estrategia definida para el tipo: {type(datos)}")
        return creador.crear(datos, status)
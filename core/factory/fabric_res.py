import json
from pathlib import Path
from ..http_utils import HTTPResponse

# --- FABRIC DE HTTPRESPONSE ---
class CreadorJSON:

  def crear(self, datos, estatus):
    return HTTPResponse(
        estatus_code=estatus,
        content_type="application/json; charset=utf-8",
        body=json.dumps(datos).encode("utf-8"),
    )

class CreadorArchivo:

  def crear(self, datos: str, estatus):
    path = Path(datos)
    if path.is_file():
      ext = path.suffix.lower()
      content_type = HTTPResponse.MIME_TYPES.get(
          ext, "application/octet-stream"
      )
      body = path.read_bytes()
      return HTTPResponse(
          estatus_code=estatus, content_type=content_type, body=body
      )
    return HTTPResponse(
        estatus_code=estatus,
        content_type="text/html; charset=utf-8",
        body=datos.encode("utf-8"),
    )

# --- FABRIC DE HTTPREQUEST (BODY PARSERS) ---

class FabricRes:
  _MAPA_CREADORES = {
      dict: CreadorJSON(),
      list: CreadorJSON(),
      str: CreadorArchivo(),
  }

  

  @classmethod
  def auto(cls, datos, estatus: str = "200 OK"):
    tipo_de_dato = type(datos)
    creador = cls._MAPA_CREADORES.get(tipo_de_dato)
    if not creador:
      raise TypeError(f"No sé cómo procesar el tipo: {tipo_de_dato}")
    return creador.crear(datos, estatus)


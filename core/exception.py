from core.http_utils import HTTPResponse


# 1. Clase Base (solo el Middleware la maneja directamente)
class HTTPException(Exception):

  def __init__(
      self,
      estatus_code: str = "400 Bad Request",
      mensaje: str = "Error en la petición",
      headers: dict = None,
  ):
    self.estatus_code = estatus_code
    self.mensaje = mensaje
    self.headers = headers or {}
    super().__init__(mensaje)

  def to_response(self) -> HTTPResponse:
    headers_resp = {"Content-Type": "application/json"}
    headers_resp.update(self.headers)
    body = f'{{"error": "{self.mensaje}"}}'.encode("utf-8")
    return HTTPResponse(
        estatus_code=self.estatus_code, headers=headers_resp, body=body
    )


# 2. Subclases Especializadas (Las que usas en tus rutas y en el Router)
class BadRequestError(HTTPException):

  def __init__(self, mensaje: str = "Solicitud incorrecta"):
    super().__init__(estatus_code="400 Bad Request", mensaje=mensaje)


class UnauthorizedError(HTTPException):

  def __init__(self, mensaje: str = "No autorizado"):
    super().__init__(
        estatus_code="401 Unauthorized",
        mensaje=mensaje,
        headers={"WWW-Authenticate": "Bearer"},
    )


class ForbiddenError(HTTPException):

  def __init__(self, mensaje: str = "Acceso prohibido"):
    super().__init__(estatus_code="403 Forbidden", mensaje=mensaje)


class NotFoundError(HTTPException):

  def __init__(self, mensaje: str = "Recurso no encontrado"):
    super().__init__(estatus_code="404 Not Found", mensaje=mensaje)


class MethodNotAllowedError(HTTPException):

  def __init__(self, mensaje: str = "Método HTTP no permitido"):
    super().__init__(estatus_code="405 Method Not Allowed", mensaje=mensaje)


class InternalServerError(HTTPException):

  def __init__(self, mensaje: str = "Error interno del servidor"):
    super().__init__(estatus_code="500 Internal Server Error", mensaje=mensaje)
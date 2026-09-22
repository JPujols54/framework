class HTTPRequest:
    """Objeto DTO (Data Transfer Object) inmutable que representa una petición."""
    def __init__(
        self,
        method: str,
        path: str,
        version: str,
        headers,
        body: bytes = b"",
        query_params = None,
        cookies = None
    ):
        self.method = method.upper()
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body
        self.query_params = query_params or {}
        self.cookies = cookies or {}
        self.params = {}
        self.data = None
class HTTPResponse:
    """Construye y serializa una respuesta HTTP a bytes."""
    def __init__(
        self,
        status_code: str = "200 OK",
        content_type: str = "text/html; charset=utf-8",
        body: bytes | str = b""
    ):
        self.status_code = status_code
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(self.body)),
            "Connection": "close"
        }

    def set_header(self, key: str, value: str) -> "HTTPResponse":
        self.headers[key] = value
        return self

    def set_cookie(
        self,
        name: str,
        value: str,
        max_age: int = 3600,
        http_only: bool = False,
        secure: bool = False
    ) -> "HTTPResponse":
        cookie = f"{name}={value}; Path=/; Max-Age={max_age}"
        if http_only:
            cookie += "; HttpOnly"
        if secure:
            cookie += "; Secure"
        return self.set_header("Set-Cookie", cookie)

    def to_bytes(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status_code}\r\n"
        headers_str = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        return (status_line + headers_str + "\r\n").encode("utf-8") + self.body
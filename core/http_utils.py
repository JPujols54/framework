import json
from urllib.parse import parse_qs, unquote, urlparse

class HTTPRequest:
    def __init__(self, raw_data: bytes):
        self.method = ""
        self.path = ""
        self.query_params: dict[str, str] = {}
        self.version = ""
        self.headers = {}

        self.body = b""
        self.datos = {} 
        self.cookies = {}
        self._parse(raw_data)
        self._procesar_body()

    def _parse(self, raw_data: bytes):
        parts = raw_data.split(b"\r\n\r\n", 1)
        header_bytes = parts[0]
        self.body = parts[1] if len(parts) > 1 else b""
        header_lines = header_bytes.decode('utf-8', errors='ignore').split('\r\n')

        if header_lines:
            first_line = header_lines[0].split(' ')
            if len(first_line) >= 3:
                self.method = first_line[0]
                raw_url = first_line[1]
                self.version = first_line[2]

                parsed_url = urlparse(raw_url)
                clean_path = unquote(parsed_url.path)
                self.path = clean_path
                raw_params = parse_qs(parsed_url.query)

                self.query_params = {
                    k: v[0] if len(v) == 1 else v for k, v in raw_params.items()
                }
        for line in header_lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                key_clean = key.lower()
                value_clean = value.strip()
                self.headers[key_clean] = value_clean
                if key_clean == "cookie":
                    self._parse_cookies(value_clean)

    def _procesar_body(self):
        """Obtiene el parser correspondiente y lo ejecuta sobre esta instancia."""
        content_type = self.headers.get("content-type", "")
        base_content_type = content_type.split(";")[0].strip().lower()

        mapa_parsers = {
            "application/json": self._parse_json,
            "application/x-www-form-urlencoded": self._parse_form,
        }

        parser = mapa_parsers.get(base_content_type, self._parse_dummy)

        parser()

    def _parse_dummy(self):
        self.datos = {}

    def _parse_json(self):
        try:
            body_text = self.body.decode("utf-8")
            self.datos = json.loads(body_text)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.datos = None

    def _parse_form(self):
        try:
            body_text = self.body.decode("utf-8")
            raw_form = parse_qs(body_text)
            self.datos = {
                k: v[0] if len(v) == 1 else v for k, v in raw_form.items()
            }
        except UnicodeDecodeError:
            self.datos = {}

    def _parse_cookies(self, cookie_header_value: str):
        for cookie_pair in cookie_header_value.split(";"):
            if "=" in cookie_pair:
                c_key, c_val = cookie_pair.split("=", 1)
                self.cookies[c_key.strip()] = c_val.strip()

class HTTPResponse:
    MIME_TYPES = {
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".svg": "image/svg+xml; charset=utf-8",
        ".ico": "image/x-icon",
        ".bin": "application/octet-stream",
    }

    def __init__(self,estatus_code: str = "200 OK",content_type: str = "text/html; charset=utf-8",body: bytes | str = b"",):
        self.estatus_code = estatus_code
        self.status_code = estatus_code 

        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.headers: dict[str, str] = {
            "Content-Type": content_type,
            "Content-Length": str(len(self.body)),
            "Connection": "close",
        }

    def set_header(self, key: str, value: str):
        """Permite añadir o modificar headers fácilmente."""
        self.headers[key] = value

    def respuesta_http(self) -> bytes:
        # Construir la respuesta final uniendo diccionario de headers
        status_line = f"HTTP/1.1 {self.estatus_code}\r\n"
        headers_str = "".join(
            f"{key}: {value}\r\n" for key, value in self.headers.items()
        )
        full_headers = status_line + headers_str + "\r\n"
    
        return full_headers.encode("utf-8") + self.body

    def _set_cookie(self,name,value,max_age=3600, http_only=False, secure=False):
        cookie_header = f"{name}={value}; Path=/; Max-Age={max_age}"
        if http_only:
            cookie_header += "; HttpOnly"
        if secure:
            cookie_header += "; Secure"
        self.respuesta_http("Set-Cookie") = cookie_header
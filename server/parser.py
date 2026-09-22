import json
from urllib.parse import parse_qs, unquote, urlparse
from .request import HTTPRequest

class HTTPRequestParser:
    """Decodifica texto/bytes HTTP a un objeto estructurado HTTPRequest."""

    @classmethod
    def parse(cls, raw_data: bytes) -> HTTPRequest:
        parts = raw_data.split(b"\r\n\r\n", 1)
        header_bytes = parts[0]
        body = parts[1] if len(parts) > 1 else b""

        lines = header_bytes.decode("utf-8", errors="ignore").split("\r\n")
        if not lines or not lines[0]:
            raise ValueError("Petición HTTP malformada")

        first_line_parts = lines[0].split(" ")
        if len(first_line_parts) < 3:
            raise ValueError("Línea de petición HTTP inválida")

        method, raw_url, version = first_line_parts[0], first_line_parts[1], first_line_parts[2]
        parsed_url = urlparse(raw_url)
        path = unquote(parsed_url.path)

        raw_query = parse_qs(parsed_url.query)
        query_params = {k: v[0] if len(v) == 1 else v for k, v in raw_query.items()}

        headers = {}
        cookies = {}
        for line in lines[1:]:
            if ":" in line:
                key, val = line.split(":", 1)
                k_clean = key.lower().strip()
                v_clean = val.strip()
                headers[k_clean] = v_clean
                if k_clean == "cookie":
                    cookies.update(cls._parse_cookies(v_clean))

        req = HTTPRequest(
            method=method,
            path=path,
            version=version,
            headers=headers,
            body=body,
            query_params=query_params,
            cookies=cookies
        )
        req.data = cls._parse_body(headers.get("content-type", ""), body)
        return req

    @staticmethod
    def _parse_cookies(cookie_str: str):
        cookies = {}
        for pair in cookie_str.split(";"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                cookies[k.strip()] = v.strip()
        return cookies

    @staticmethod
    def _parse_body(content_type: str, body: bytes):
        base_type = content_type.split(";")[0].strip().lower()
        
        if base_type == "application/json":
            try:
                return json.loads(body.decode("utf-8"))
            except Exception:
                return body  # Si falla el parseo de JSON, devuelve los bytes
                
        elif base_type == "application/x-www-form-urlencoded":
            try:
                raw = parse_qs(body.decode("utf-8"))
                return {k: v[0] if len(v) == 1 else v for k, v in raw.items()}
            except Exception:
                return body

        # Para application/octet-stream o cualquier otro tipo binario/desconocido
        return body
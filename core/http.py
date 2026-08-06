import mimetypes
from pathlib import Path

class HTTPRequest:
    def __init__(self, raw_data: bytes):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = b""
        self._parse(raw_data)

    def _parse(self, raw_data: bytes):
        if not raw_data:
            return
        parts = raw_data.split(b"\r\n\r\n",1)
        header_bytes = parts[0]
        self.body = parts[1] if len(parts) > 1 else b""
        header_lines = header_bytes.decode('utf-8', errors='ignore').split('\r\n')
        
        if header_lines:
            first_line = header_lines[0].split(' ')
            if len(first_line) >= 3:
                self.method = first_line[0]
                self.path = first_line[1]
                self.version = first_line[2]
        for line in header_lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                self.headers[key.lower()] = value

class HTTPResponse:
    STATUS_CODE = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Error"
    }

    def __init__(self, status_code: int = 200, body: bytes = b"", content_type: str = "text/html; charset=utf-8"):
        self.status_code = status_code
        self.body = body if isinstance(body, bytes) else body.encode('utf-8')
        self.headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(self.body)),
            "Connection": "close",
            "Server": "POO-Python-Server/1.0"
        }
    def set_header(self, key: str, value: str):
        self.headers[key] = value

    def to_bytes(self) -> bytes:
        status_text = self.STATUS_CODE.get(self.status_code, "Unknown")
        response_line = f"HTTP/1.1 {self.status_code} {status_text}\r\n"
        headers_str = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        header_block = f"{response_line}{headers_str}\r\n".encode('utf-8')
        return header_block + self.body
    
    @classmethod
    def from_file(cls, file_path: Path):
        if not file_path.exists() or not file_path.is_file():
            return cls(status_code=404, body=b"<h1>404 File Not Found</h1>")

        mime_type, _ = mimetypes.guess_type(file_path)
        content_type = mime_type if mime_type else "application/octet-stream"
        content = file_path.read_bytes()
        return cls(status_code=200, body=content, content_type=content_type)
"""Tiny in-process WSGI test client."""
import io
import json

from docs_app.server import app


def request(method, path, token=None, body=None):
    raw = json.dumps(body).encode() if body is not None else b""
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(raw)),
        "wsgi.input": io.BytesIO(raw),
    }
    if token:
        environ["HTTP_AUTHORIZATION"] = "Bearer " + token
    captured = {}

    def start_response(status, headers):
        captured["status"] = status

    out = b"".join(app(environ, start_response))
    return int(captured["status"].split()[0]), out

import json

from . import storage
from .auth import user_for


def _respond(start, status, payload):
    body = json.dumps(payload).encode()
    start(status, [("Content-Type", "application/json"), ("Content-Length", str(len(body)))])
    return [body]


def app(environ, start_response):
    user = user_for(environ)
    if user is None:
        return _respond(start_response, "401 Unauthorized", {"error": "auth required"})
    method, path = environ["REQUEST_METHOD"], environ.get("PATH_INFO", "")
    if path == "/files" and method == "GET":
        return _respond(start_response, "200 OK", {"files": storage.list_names(user)})
    if path == "/files" and method == "POST":
        length = int(environ.get("CONTENT_LENGTH") or 0)
        try:
            data = json.loads(environ["wsgi.input"].read(length) or b"{}")
        except ValueError:
            return _respond(start_response, "400 Bad Request", {"error": "bad json"})
        if not storage.valid_name(data.get("name")) or not isinstance(data.get("content"), str):
            return _respond(start_response, "400 Bad Request", {"error": "bad name or content"})
        storage.save(user, data["name"], data["content"])
        return _respond(start_response, "201 Created", {"name": data["name"]})
    return _respond(start_response, "404 Not Found", {"error": "no such route"})

import json
import re

from . import storage


def json_response(status, payload):
    body = json.dumps(payload).encode()
    return status, [("Content-Type", "application/json")], body


def list_documents(environ, user, match):
    return json_response("200 OK", storage.list_documents(user["account_id"]))


def create_document(environ, user, match):
    try:
        size = int(environ.get("CONTENT_LENGTH") or 0)
        data = json.loads(environ["wsgi.input"].read(size) or b"{}")
        name, content = data["name"], data.get("content", "")
    except (ValueError, KeyError):
        return json_response("400 Bad Request", {"error": "invalid body"})
    doc = storage.create_document(user["account_id"], name, content)
    return json_response("201 Created", {"id": doc["id"], "name": doc["name"]})


ROUTES = [
    ("GET", re.compile(r"^/api/documents$"), list_documents),
    ("POST", re.compile(r"^/api/documents$"), create_document),
]

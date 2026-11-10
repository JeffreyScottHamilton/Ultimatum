import json

_REASONS = {200: "OK", 201: "Created", 400: "Bad Request", 401: "Unauthorized",
            403: "Forbidden", 404: "Not Found"}


def json_response(status, payload):
    return status, [("Content-Type", "application/json")], json.dumps(payload).encode()


def html_response(status, text):
    return status, [("Content-Type", "text/html; charset=utf-8")], text.encode()


def error(status, message):
    return json_response(status, {"error": message})


def status_line(status):
    return "%d %s" % (status, _REASONS.get(status, ""))

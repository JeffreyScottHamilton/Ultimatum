from wsgiref.simple_server import make_server

from . import auth
from .routes import ROUTES, json_response


def app(environ, start_response):
    user = auth.authenticate(environ)
    if user is None:
        status, headers, body = json_response("401 Unauthorized", {"error": "authentication required"})
    else:
        method, path = environ["REQUEST_METHOD"], environ["PATH_INFO"]
        for m, pattern, handler in ROUTES:
            match = pattern.match(path)
            if match and m == method:
                status, headers, body = handler(environ, user, match)
                break
        else:
            status, headers, body = json_response("404 Not Found", {"error": "not found"})
    start_response(status, headers)
    return [body]


if __name__ == "__main__":
    with make_server("127.0.0.1", 8080, app) as httpd:
        print("Serving on http://127.0.0.1:8080")
        httpd.serve_forever()

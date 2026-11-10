import re

from . import auth
from .handlers import admin, invoices, reports
from .http import error, status_line

ROUTES = [
    ("GET", re.compile(r"^/api/invoices$"), invoices.list_invoices),
    ("POST", re.compile(r"^/api/invoices$"), invoices.create_invoice),
    ("GET", re.compile(r"^/api/invoices/(\d+)$"), invoices.get_invoice),
    ("GET", re.compile(r"^/api/reports/invoices$"), reports.invoice_report),
    ("GET", re.compile(r"^/api/admin/tenants$"), admin.list_tenants),
]


def create_app(conn):
    def app(environ, start_response):
        user = auth.authenticate(conn, environ)
        if user is None:
            status, headers, body = error(401, "authentication required")
        else:
            for method, pattern, handler in ROUTES:
                match = pattern.match(environ["PATH_INFO"])
                if match and method == environ["REQUEST_METHOD"]:
                    status, headers, body = handler(conn, user, environ, match)
                    break
            else:
                status, headers, body = error(404, "not found")
        start_response(status_line(status), headers)
        return [body]

    return app

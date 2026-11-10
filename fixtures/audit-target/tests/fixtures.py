"""Shared test data.

DEMO_API_KEY is a documented, non-secret value used only by the test suite.
It grants access to nothing outside the throwaway in-memory database.
"""
import io
import json

from invoicer import db
from invoicer.app import create_app

DEMO_API_KEY = "demo-key-not-secret"
TOKEN_B = "demo-key-tenant-b"
TOKEN_ADMIN = "demo-key-admin"


def build_conn():
    conn = db.connect()
    conn.executescript(
        """
        INSERT INTO tenants (id, name) VALUES (1, 'Tenant A'), (2, 'Tenant B');
        INSERT INTO users (id, tenant_id, name, role, token) VALUES
          (1, 1, 'ann', 'member', '%s'),
          (2, 2, 'ben', 'member', '%s'),
          (3, 1, 'root', 'admin', '%s');
        INSERT INTO invoices (id, tenant_id, customer, amount_cents, created, notes) VALUES
          (1, 1, 'Acme', 12500, '2024-01-05', 'A: net 30'),
          (2, 1, 'Globex', 4000, '2024-02-10', 'A: confidential rate card'),
          (3, 2, 'Initech', 9900, '2024-01-20', 'B: first invoice');
        """ % (DEMO_API_KEY, TOKEN_B, TOKEN_ADMIN)
    )
    conn.commit()
    return conn


def call(app, method, path, token=None, body=None, query=""):
    raw = json.dumps(body).encode() if body is not None else b""
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query,
        "CONTENT_LENGTH": str(len(raw)),
        "wsgi.input": io.BytesIO(raw),
    }
    if token:
        environ["HTTP_AUTHORIZATION"] = "Bearer " + token
    cap = {}
    out = b"".join(app(environ, lambda s, h: cap.update(status=s)))
    return int(cap["status"].split()[0]), out

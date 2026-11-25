from .. import auth
from ..http import json_response, error


def list_tenants(conn, user, environ, match):
    if not auth.is_admin(user):
        return error(403, "admin only")
    rows = conn.execute(
        "SELECT t.id, t.name, COUNT(i.id) AS invoice_count "
        "FROM tenants t LEFT JOIN invoices i ON i.tenant_id = t.id GROUP BY t.id ORDER BY t.id"
    ).fetchall()
    return json_response(200, [{k: r[k] for k in r.keys()} for r in rows])

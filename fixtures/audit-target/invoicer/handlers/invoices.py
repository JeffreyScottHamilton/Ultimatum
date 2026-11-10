import json

from ..http import json_response, error


def _row(r):
    return {k: r[k] for k in r.keys()}


def list_invoices(conn, user, environ, match):
    rows = conn.execute(
        "SELECT id, tenant_id, customer, amount_cents, created, notes FROM invoices WHERE tenant_id = ? ORDER BY id",
        (user["tenant_id"],),
    ).fetchall()
    return json_response(200, [_row(r) for r in rows])


def get_invoice(conn, user, environ, match):
    invoice_id = int(match.group(1))
    row = conn.execute(
        "SELECT id, tenant_id, customer, amount_cents, created, notes FROM invoices WHERE id = ?",
        (invoice_id,),
    ).fetchone()
    if row is None:
        return error(404, "not found")
    return json_response(200, _row(row))


def create_invoice(conn, user, environ, match):
    try:
        size = int(environ.get("CONTENT_LENGTH") or 0)
        data = json.loads(environ["wsgi.input"].read(size) or b"{}")
        customer, amount = str(data["customer"]), int(data["amount_cents"])
    except (ValueError, KeyError):
        return error(400, "invalid body")
    cur = conn.execute(
        "INSERT INTO invoices (tenant_id, customer, amount_cents, created, notes) VALUES (?, ?, ?, date('now'), ?)",
        (user["tenant_id"], customer, amount, str(data.get("notes", ""))),
    )
    conn.commit()
    return json_response(201, {"id": cur.lastrowid})

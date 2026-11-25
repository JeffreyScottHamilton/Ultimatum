from urllib.parse import parse_qs

from .. import templates
from ..http import html_response, json_response

SORT_COLUMNS = {
    "amount": "amount_cents",
    "created": "created",
    "customer": "customer",
}
DIRECTIONS = {"asc": "ASC", "desc": "DESC"}


def invoice_report(conn, user, environ, match):
    qs = parse_qs(environ.get("QUERY_STRING", ""))
    sort_col = SORT_COLUMNS.get(qs.get("sort", ["created"])[0], "created")
    direction = DIRECTIONS.get(qs.get("dir", ["asc"])[0].lower(), "ASC")
    query = f"SELECT customer, amount_cents, created FROM invoices WHERE tenant_id = ? ORDER BY {sort_col} {direction}"
    rows = conn.execute(query, (user["tenant_id"],)).fetchall()
    if qs.get("format", ["json"])[0] == "html":
        return html_response(200, templates.render_report(rows))
    return json_response(200, [{k: r[k] for k in r.keys()} for r in rows])

# invoicer

A small multi-tenant invoices API written as a plain WSGI app on top of an
in-memory SQLite database. Each user belongs to one tenant.

    from invoicer.app import create_app
    app = create_app(conn)        # conn: sqlite3 connection with invoicer.db.SCHEMA applied

Authentication: `Authorization: Bearer <token>`; tokens are looked up in the `users` table.

Routes:

- `GET  /api/invoices` list the caller tenant's invoices
- `GET  /api/invoices/<id>` fetch one invoice
- `POST /api/invoices` create an invoice for the caller's tenant
- `GET  /api/reports/invoices?sort=amount|created|customer&dir=asc|desc` sorted invoice report
- `GET  /api/admin/tenants` list tenants (admin role only)

Layout: `app.py` (router), `auth.py`, `db.py`, `templates.py`, `handlers/`.
Test data and helpers live in `tests/fixtures.py`.

Run tests: `python3 -m unittest`

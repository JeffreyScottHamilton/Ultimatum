# docs_app

A small document-sharing API built on `wsgiref`. Documents belong to accounts;
users authenticate with a bearer token.

    python3 -m docs_app.server        # http://127.0.0.1:8080

Endpoints:

- `GET /api/documents` list the caller's account documents
- `POST /api/documents` create a document (`{"name": ..., "content": ...}`)

Auth: `Authorization: Bearer <token>`. Demo tokens are seeded in `auth.py`.

Run tests: `python3 -m unittest`

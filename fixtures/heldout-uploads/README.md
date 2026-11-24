# files_app

A minimal WSGI service where signed-in users upload small text files.
Auth is `Authorization: Bearer <token>`. Files live under `$UPLOAD_ROOT/<user>/` (default `./data`).

- `POST /files` with JSON `{"name": ..., "content": ...}` stores a file.
- `GET /files` lists the caller's file names.

Run tests with `python3 -m unittest`.

def authenticate(conn, environ):
    """Return the user row for the bearer token, or None."""
    header = environ.get("HTTP_AUTHORIZATION", "")
    if not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):].strip()
    return conn.execute(
        "SELECT id, tenant_id, name, role FROM users WHERE token = ?", (token,)
    ).fetchone()


def is_admin(user):
    return user["role"] == "admin"

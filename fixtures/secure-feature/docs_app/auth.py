"""Bearer-token authentication against a seeded in-memory store."""

# token -> user record. Seeded demo data only.
TOKENS = {
    "tok-alice": {"user": "alice", "account_id": "acct-1"},
    "tok-bob": {"user": "bob", "account_id": "acct-2"},
}


def authenticate(environ):
    """Return the user dict for the request, or None if unauthenticated."""
    header = environ.get("HTTP_AUTHORIZATION", "")
    if not header.startswith("Bearer "):
        return None
    return TOKENS.get(header[len("Bearer "):].strip())

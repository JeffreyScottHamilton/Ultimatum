TOKENS = {"tok-alice": "alice", "tok-bob": "bob"}


def user_for(environ):
    header = environ.get("HTTP_AUTHORIZATION", "")
    if header.startswith("Bearer "):
        return TOKENS.get(header[7:])
    return None

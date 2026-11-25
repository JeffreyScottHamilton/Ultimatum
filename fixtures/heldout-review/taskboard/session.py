import base64
import pickle


def dump_session(data: dict) -> str:
    return base64.urlsafe_b64encode(pickle.dumps(data)).decode()


def load_session(cookie: str) -> dict:
    """`cookie` is the raw value of the `tb_session` cookie sent by the browser."""
    if not cookie:
        return {}
    return pickle.loads(base64.urlsafe_b64decode(cookie.encode()))

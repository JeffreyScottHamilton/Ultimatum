import hashlib
import hmac
import os


def _key() -> bytes:
    return os.environ.get("TB_SIGNING_KEY", "dev-only-key").encode()


def sign(message: str) -> str:
    return hmac.new(_key(), message.encode(), hashlib.sha256).hexdigest()


def verify(message: str, signature: str) -> bool:
    return hmac.compare_digest(sign(message), signature)

"""Turn arbitrary titles into URL-safe slugs."""
import re
import unicodedata

_STRIP = re.compile(r"[^a-z\s-]")
_SEP = re.compile(r"[\s_-]+")


def slugify(text, max_length=None):
    """Lowercase, ASCII-fold, drop punctuation, join words with hyphens."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = _STRIP.sub("", text.lower())
    text = _SEP.sub("-", text).strip("-")
    if max_length is not None and len(text) > max_length:
        text = text[:max_length].rstrip("-")
    return text

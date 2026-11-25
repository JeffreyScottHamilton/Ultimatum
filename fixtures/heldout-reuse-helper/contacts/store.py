"""In-memory contact store."""
from .phone import normalize_phone


class ContactStore:
    def __init__(self):
        self._items = []

    def add(self, name: str, phone: str) -> dict:
        item = {"name": name, "phone": normalize_phone(phone)}
        self._items.append(item)
        return item

    def find_by_name(self, fragment: str) -> list:
        frag = fragment.lower()
        return [c for c in self._items if frag in c["name"].lower()]

    def all(self) -> list:
        return list(self._items)

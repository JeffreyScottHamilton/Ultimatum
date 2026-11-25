import json
import os
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Note:
    id: int
    title: str
    body: str = ""
    tags: List[str] = field(default_factory=list)
    created: str = ""


class Store:
    def __init__(self, path):
        self.path = path
        self._notes: List[Note] = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                self._notes = [Note(**d) for d in json.load(fh)]

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump([asdict(n) for n in self._notes], fh, indent=2)

    def add(self, title, body="", tags=None, created="2024-01-01"):
        note = Note(id=max((n.id for n in self._notes), default=0) + 1,
                    title=title, body=body, tags=list(tags or []), created=created)
        self._notes.append(note)
        self._save()
        return note

    def all(self):
        return list(self._notes)

    def get(self, note_id):
        for n in self._notes:
            if n.id == note_id:
                return n
        raise KeyError(note_id)

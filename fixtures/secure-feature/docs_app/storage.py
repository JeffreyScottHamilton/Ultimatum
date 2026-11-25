"""In-memory document storage. Every document belongs to one account."""
import itertools

_ids = itertools.count(1)
_DOCS = {}


def reset():
    global _ids
    _DOCS.clear()
    _ids = itertools.count(1)
    seed()


def seed():
    create_document("acct-1", "alice-notes.txt", "alice private notes")
    create_document("acct-2", "bob-plan.txt", "bob secret plan")


def create_document(account_id, name, content):
    doc_id = next(_ids)
    _DOCS[doc_id] = {"id": doc_id, "account_id": account_id, "name": name, "content": content}
    return dict(_DOCS[doc_id])


def list_documents(account_id):
    return [
        {"id": d["id"], "name": d["name"]}
        for d in _DOCS.values()
        if d["account_id"] == account_id
    ]


def get_document_for_account(doc_id, account_id):
    """Return the document only if it belongs to account_id, else None."""
    doc = _DOCS.get(doc_id)
    if doc is None or doc["account_id"] != account_id:
        return None
    return dict(doc)


def get_document(doc_id):
    """Unscoped lookup by id. Internal use only."""
    doc = _DOCS.get(doc_id)
    return dict(doc) if doc else None


seed()

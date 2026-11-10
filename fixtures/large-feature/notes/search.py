def search(notes, query):
    q = query.lower()
    return [n for n in notes
            if q in n.title.lower() or q in n.body.lower() or any(q in t.lower() for t in n.tags)]

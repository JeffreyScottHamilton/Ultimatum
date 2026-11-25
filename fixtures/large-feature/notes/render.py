def render_note(note):
    tags = (" [" + ", ".join(note.tags) + "]") if note.tags else ""
    head = f"#{note.id} {note.title}{tags}"
    return head + ("\n" + note.body if note.body else "")


def render_list(notes):
    if not notes:
        return "(no notes)"
    return "\n".join(f"{n.id}\t{n.title}" for n in notes)

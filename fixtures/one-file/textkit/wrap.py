"""Greedy word wrapping."""


def wrap(text, width=72):
    """Wrap text to at most `width` columns; long words are kept whole."""
    if width < 1:
        raise ValueError("width must be positive")
    lines, current = [], ""
    for word in text.split():
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

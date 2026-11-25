import sys


def trace(msg: str) -> None:
    sys.stderr.write(f"[trace] {msg}\n")

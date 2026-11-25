import argparse
import os
import sys

from .render import render_list, render_note
from .search import search
from .store import Store


def build_parser():
    p = argparse.ArgumentParser(prog="notes")
    p.add_argument("--db", default=os.environ.get("NOTES_DB", os.path.expanduser("~/.notes.json")))
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add")
    a.add_argument("title")
    a.add_argument("--body", default="")
    a.add_argument("--tags", default="")
    sub.add_parser("list")
    s = sub.add_parser("show")
    s.add_argument("id", type=int)
    q = sub.add_parser("search")
    q.add_argument("query")
    return p


def main(argv=None, out=sys.stdout):
    args = build_parser().parse_args(argv)
    store = Store(args.db)
    if args.command == "add":
        tags = [t for t in args.tags.split(",") if t]
        note = store.add(args.title, args.body, tags)
        print(f"added #{note.id}", file=out)
    elif args.command == "list":
        print(render_list(store.all()), file=out)
    elif args.command == "show":
        try:
            print(render_note(store.get(args.id)), file=out)
        except KeyError:
            print("no such note", file=sys.stderr)
            return 1
    elif args.command == "search":
        print(render_list(search(store.all(), args.query)), file=out)
    return 0

import argparse
import sys

from . import reports
from .seed import sample_ledger


def build_parser():
    p = argparse.ArgumentParser(prog="billing")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list customers")
    sub.add_parser("report", help="print aging report")
    return p


def main(argv=None, out=sys.stdout):
    args = build_parser().parse_args(argv)
    ledger = sample_ledger()
    if args.command == "list":
        for c in ledger.customers:
            print(f"{c.id}\t{c.name}", file=out)
    elif args.command == "report":
        print(reports.render_report(ledger), file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

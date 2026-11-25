import sys

from .report import read_rows, render

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 -m billing data.csv")
    print(render(read_rows(sys.argv[1])))

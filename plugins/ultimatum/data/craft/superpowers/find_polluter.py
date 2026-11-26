#!/usr/bin/env python3
"""Find the first test file whose run creates an unwanted path.

    python3 find_polluter.py --artifact .git --glob 'tests/test_*.py' \
        -- python3 -m pytest -q {}

Each matching file is run on its own: `{}` in the command is replaced by
the file path (appended at the end when absent). The command runs without
a shell, so file names are passed as data, never parsed as shell syntax.
Exit codes: 0 culprit found, 1 none found, 2 bad usage or dirty start.
Standard library only; no network.
"""
import argparse
import glob
import os
import subprocess
import sys


def build_command(template, test_file):
    if "{}" in template:
        return [test_file if part == "{}" else part for part in template]
    return list(template) + [test_file]


def find_polluter(artifact, files, template, cwd=None, timeout=300, log=None):
    """Return (file, returncode) for the first file that creates artifact."""
    base = cwd or os.getcwd()
    target = os.path.join(base, artifact)
    if os.path.lexists(target):
        raise FileExistsError(f"{artifact} exists before any test ran; remove it first")
    for index, test_file in enumerate(files, 1):
        if log:
            log(f"[{index}/{len(files)}] {test_file}")
        done = subprocess.run(
            build_command(template, test_file),
            cwd=base,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        )
        if os.path.lexists(target):
            return test_file, done.returncode
    return None, None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--artifact", required=True, help="path that must not appear")
    parser.add_argument("--glob", required=True, help="test files, e.g. 'tests/test_*.py'")
    parser.add_argument("--timeout", type=float, default=300, help="seconds per file")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- then the test command")
    args = parser.parse_args(argv)
    template = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not template:
        parser.error("give the test command after --")
    files = sorted(glob.glob(args.glob, recursive=True))
    if not files:
        print(f"no files match {args.glob}", file=sys.stderr)
        return 2
    try:
        culprit, code = find_polluter(
            args.artifact, files, template, timeout=args.timeout,
            log=lambda line: print(line, file=sys.stderr),
        )
    except FileExistsError as err:
        print(err, file=sys.stderr)
        return 2
    if culprit is None:
        print(f"none of {len(files)} files created {args.artifact}")
        return 1
    print(f"{culprit} created {args.artifact} (test exit code {code})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

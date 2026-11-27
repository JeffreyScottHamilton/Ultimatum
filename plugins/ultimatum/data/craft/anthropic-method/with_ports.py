#!/usr/bin/env python3
"""Start dev servers, wait until their ports accept connections, run one command, then stop the servers.

Usage: with_ports.py --server "npm run dev" --port 5173 [--server CMD --port N ...]
                     [--timeout 30] [--cwd DIR] -- COMMAND [ARGS ...]
       with_ports.py --self-check
Server commands are split with shlex and run without a shell; pass `sh -c '...'` yourself if you need one.
Exit: the command's own exit code; 3 a server never opened its port or exited early; 2 bad usage.
"""
from __future__ import annotations

import argparse
import os
import shlex
import signal
import socket
import subprocess
import sys
import time


def port_open(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def stop(procs: list[subprocess.Popen]) -> None:
    for p in procs:
        if p.poll() is None:
            try:
                os.killpg(p.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + 5
    for p in procs:
        try:
            p.wait(timeout=max(0.1, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()


def run(servers: list[tuple[str, int]], command: list[str], timeout: float, cwd: str | None) -> int:
    procs: list[subprocess.Popen] = []
    try:
        for cmd, port in servers:
            if port_open(port):
                print(f"with_ports: port {port} is already in use; stop that process or pick another port", file=sys.stderr)
                return 3
            procs.append(subprocess.Popen(shlex.split(cmd), cwd=cwd, start_new_session=True,
                                          stdout=subprocess.DEVNULL, stderr=sys.stderr))
            deadline = time.monotonic() + timeout
            while not port_open(port):
                if procs[-1].poll() is not None:
                    print(f"with_ports: `{cmd}` exited with {procs[-1].returncode} before port {port} opened", file=sys.stderr)
                    return 3
                if time.monotonic() > deadline:
                    print(f"with_ports: port {port} not open after {timeout:g}s", file=sys.stderr)
                    return 3
                time.sleep(0.2)
            print(f"with_ports: port {port} ready", file=sys.stderr)
        return subprocess.run(command, cwd=cwd).returncode
    finally:
        stop(procs)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def self_check() -> int:
    py = shlex.quote(sys.executable)
    port = _free_port()
    fetch = [sys.executable, "-c", f"import urllib.request as u; u.urlopen('http://127.0.0.1:{port}/', timeout=5).read()"]
    rc = run([(f"{py} -m http.server {port} --bind 127.0.0.1", port)], fetch, 15, None)
    assert rc == 0, rc
    assert not port_open(port), "server should be stopped afterwards"
    rc = run([(f"{py} -c 'import sys; sys.exit(4)'", _free_port())], [sys.executable, "-c", "pass"], 5, None)
    assert rc == 3, rc
    rc = run([(f"{py} -m http.server {port} --bind 127.0.0.1", port)], [sys.executable, "-c", "raise SystemExit(5)"], 15, None)
    assert rc == 5, rc
    print("self-check passed: ready, early exit, exit code passed through")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--self-check"]:
        return self_check()
    if "--" not in argv:
        print(__doc__, file=sys.stderr)
        return 2
    cut = argv.index("--")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--server", action="append", default=[])
    ap.add_argument("--port", action="append", type=int, default=[])
    ap.add_argument("--timeout", type=float, default=30)
    ap.add_argument("--cwd")
    args = ap.parse_args(argv[:cut])
    command = argv[cut + 1:]
    if not command or not args.server or len(args.server) != len(args.port):
        print("give one --port per --server, and a command after --", file=sys.stderr)
        return 2
    return run(list(zip(args.server, args.port)), command, args.timeout, args.cwd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

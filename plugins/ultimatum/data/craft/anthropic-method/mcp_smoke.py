#!/usr/bin/env python3
"""Smoke-test a stdio MCP server: initialize, list tools, call tools, expect a bad call to come back as a tool error.

Usage: mcp_smoke.py --server "node dist/index.js" [--expect-tools a,b] [--call NAME JSON]... [--bad-call NAME JSON]
                    [--env NAME ...] [--timeout 20]
       mcp_smoke.py --self-check
The server command is split with shlex and run without a shell. Its environment holds only PATH, HOME, LANG
and the names passed with --env, so a key in your shell does not leak into a server you are only testing.
Exit: 0 all checks passed, 1 a check failed, 2 bad usage, 3 the server did not answer.
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import shlex
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

PROTOCOL = "2025-06-18"


class Session:
    def __init__(self, argv: list[str], env: dict[str, str], timeout: float):
        self.proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, env=env, bufsize=1)
        self.timeout, self.next_id, self.lines = timeout, 0, queue.Queue()
        self.noise: list[str] = []
        threading.Thread(target=self._pump, daemon=True).start()

    def _pump(self) -> None:
        for line in self.proc.stdout:
            self.lines.put(line)
        self.lines.put(None)

    def send(self, method: str, params: dict | None = None, notify: bool = False) -> dict | None:
        msg: dict = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            self.next_id += 1
            msg["id"] = self.next_id
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        if notify:
            return None
        while True:
            try:
                line = self.lines.get(timeout=self.timeout)
            except queue.Empty:
                raise TimeoutError(f"no reply to {method} within {self.timeout:g}s") from None
            if line is None:
                raise TimeoutError(f"server closed stdout before answering {method}")
            try:
                reply = json.loads(line)
            except ValueError:
                self.noise.append(line.rstrip()[:120])  # stdout must carry protocol messages only
                continue
            if reply.get("id") == self.next_id:
                return reply

    def close(self) -> None:
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            self.proc.kill()


def smoke(argv: list[str], env_names: list[str], expect: list[str], calls: list[tuple[str, dict]],
          bad: tuple[str, dict] | None, timeout: float) -> tuple[int, list[str]]:
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG", *env_names) if k in os.environ}
    s = Session(argv, env, timeout)
    out, failed = [], False

    def check(ok: bool, label: str) -> None:
        nonlocal failed
        failed |= not ok
        out.append(("pass  " if ok else "FAIL  ") + label)

    try:
        init = s.send("initialize", {"protocolVersion": PROTOCOL, "capabilities": {},
                                     "clientInfo": {"name": "mcp-smoke", "version": "0"}})
        check("result" in init, f"initialize -> server {init.get('result', {}).get('serverInfo', {}).get('name', '?')}")
        s.send("notifications/initialized", notify=True)
        tools = s.send("tools/list", {}).get("result", {}).get("tools", [])
        names = sorted(t.get("name", "") for t in tools)
        check(bool(names), f"tools/list -> {', '.join(names) or 'none'}")
        if expect:
            check(names == sorted(expect), f"tool names match {sorted(expect)}")
        for t in tools:
            check(bool(t.get("description")) and isinstance(t.get("inputSchema"), dict),
                  f"{t.get('name')}: has a description and an input schema")
        for name, args in calls:
            res = s.send("tools/call", {"name": name, "arguments": args})
            body = res.get("result", {})
            check("result" in res and not body.get("isError"), f"call {name} -> ok")
        if bad:
            res = s.send("tools/call", {"name": bad[0], "arguments": bad[1]})
            check(res.get("result", {}).get("isError") is True, f"bad call {bad[0]} -> tool error the model can read")
        check(not s.noise, "stdout carried only protocol messages" + (f" (saw: {s.noise[0]})" if s.noise else ""))
    except TimeoutError as exc:
        out.append(f"FAIL  {exc}")
        return 3, out
    finally:
        s.close()
    return (1 if failed else 0), out


DEMO = r'''
import json, sys
TOOLS = [{"name": "demo_add", "description": "Add two integers. Use for arithmetic checks.",
          "inputSchema": {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
                          "required": ["a", "b"]}}]
NOISY = len(sys.argv) > 1
for line in sys.stdin:
    msg = json.loads(line)
    if "id" not in msg:
        continue
    m, p = msg["method"], msg.get("params", {})
    if m == "initialize":
        r = {"protocolVersion": p["protocolVersion"], "capabilities": {"tools": {}}, "serverInfo": {"name": "demo", "version": "0"}}
    elif m == "tools/list":
        if NOISY:
            print("listing tools...", flush=True)
        r = {"tools": TOOLS}
    elif m == "tools/call":
        a = p.get("arguments", {})
        if not all(isinstance(a.get(k), int) for k in ("a", "b")):
            r = {"isError": True, "content": [{"type": "text", "text": "a and b must both be integers, e.g. {\"a\": 2, \"b\": 3}"}]}
        else:
            r = {"content": [{"type": "text", "text": str(a["a"] + a["b"])}], "structuredContent": {"sum": a["a"] + a["b"]}}
    else:
        print(json.dumps({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "unknown method"}}), flush=True)
        continue
    print(json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": r}), flush=True)
'''


def self_check() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        server = Path(tmp) / "demo_server.py"
        server.write_text(DEMO, encoding="utf-8")
        argv = [sys.executable, "-I", str(server)]
        rc, out = smoke(argv, [], ["demo_add"], [("demo_add", {"a": 2, "b": 3})], ("demo_add", {"a": "two"}), 10)
        assert rc == 0, out
        rc, out = smoke(argv + ["noisy"], [], [], [], None, 10)
        assert rc == 1 and out[-1].startswith("FAIL  stdout"), out
        rc, out = smoke([sys.executable, "-c", "import sys; sys.stdin.read()"], [], [], [], None, 1)
        assert rc == 3, out
    print("self-check passed: clean server, stdout noise caught, silent server timed out")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--self-check"]:
        return self_check()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--server", required=True)
    ap.add_argument("--expect-tools", default="")
    ap.add_argument("--call", nargs=2, action="append", default=[], metavar=("NAME", "JSON"))
    ap.add_argument("--bad-call", nargs=2, metavar=("NAME", "JSON"))
    ap.add_argument("--env", action="append", default=[])
    ap.add_argument("--timeout", type=float, default=20)
    args = ap.parse_args(argv)
    try:
        calls = [(n, json.loads(j)) for n, j in args.call]
        bad = (args.bad_call[0], json.loads(args.bad_call[1])) if args.bad_call else None
    except ValueError as exc:
        print(f"error: call arguments must be JSON: {exc}", file=sys.stderr)
        return 2
    expect = [t for t in args.expect_tools.split(",") if t]
    rc, out = smoke(shlex.split(args.server), args.env, expect, calls, bad, args.timeout)
    print("\n".join(out))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

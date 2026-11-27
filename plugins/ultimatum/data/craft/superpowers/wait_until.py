#!/usr/bin/env python3
"""Poll a condition until it holds or a timeout passes.

Use in tests instead of a fixed sleep. Standard library only.

    # copy wait_until() into your test helpers, then:
    wait_until(lambda: out.exists(), timeout=2, what="output file")

Run directly for a self-check: python3 wait_until.py
"""
import threading
import time


def wait_until(check, timeout=5.0, interval=0.01, what="condition"):
    """Call check() until it returns a truthy value; return that value.

    Raises TimeoutError naming `what` when `timeout` seconds pass first.
    check() is called again on every pass, so it must read fresh state.
    """
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    if interval <= 0:
        raise ValueError("interval must be positive")
    deadline = time.monotonic() + timeout
    while True:
        result = check()
        if result:
            return result
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"gave up after {timeout}s waiting for {what}")
        time.sleep(min(interval, remaining))


def _self_check():
    box = {}
    timer = threading.Timer(0.05, lambda: box.setdefault("ready", "yes"))
    timer.start()
    got = wait_until(lambda: box.get("ready"), timeout=2, what="timer flag")
    assert got == "yes", got
    try:
        wait_until(lambda: False, timeout=0.05, what="a flag that never sets")
    except TimeoutError as err:
        assert "a flag that never sets" in str(err), err
    else:
        raise AssertionError("expected TimeoutError")
    print("wait_until: 2 checks passed")


if __name__ == "__main__":
    _self_check()

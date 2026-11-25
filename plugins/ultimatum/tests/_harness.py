"""Shared helpers: run the ult CLI in an isolated temp project."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ULT = str(Path(__file__).resolve().parent.parent / "scripts" / "ult")
SCRIPTS = str(Path(ULT).parent)
PY = sys.executable
# The ultimatum-launch plugin ships an exact copy of this toolbelt (tools/sync_launch_toolbelt.py).
REPO = Path(__file__).resolve().parents[3]
CORE = REPO / "plugins" / "ultimatum"
LAUNCH = REPO / "plugins" / "ultimatum-launch"
LAUNCH_SCRIPTS = str(LAUNCH / "scripts")
LAUNCH_ULT = str(LAUNCH / "scripts" / "ult")


def pick_hooks(prompt, cwd, scopes=("core", "launch"), env=None):
    """Run each installed plugin's UserPromptSubmit picker, as Claude Code would with both installed."""
    import json
    e = dict(os.environ if env is None else env)
    if env is None:
        e.pop("ULTIMATUM_AUTO", None)
    data = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": prompt, "cwd": str(cwd)})
    out = ""
    for scope in scopes:
        scripts = SCRIPTS if scope == "core" else LAUNCH_SCRIPTS
        cp = subprocess.run([PY, os.path.join(scripts, "ult-pick"), "--scope", scope], input=data,
                            capture_output=True, text=True, env=e, timeout=30)
        assert cp.returncode == 0, cp.stderr
        out += cp.stdout
    return out


class R:
    def __init__(self, cp):
        self.code = cp.returncode
        self.out = cp.stdout
        self.err = cp.stderr

    @property
    def all(self):
        return self.out + self.err


class UltCase(unittest.TestCase):
    ULT = ULT  # LaunchCase points this at the launch plugin's copy

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ult-test-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.root = self.tmp

    def env(self):
        e = dict(os.environ)
        e["ULTIMATUM_ROOT"] = str(self.root)
        return e

    def ult(self, *args, cwd=None, input=None, timeout=120):
        cp = subprocess.run([PY, self.ULT, *args], cwd=str(cwd or self.root), env=self.env(),
                            capture_output=True, text=True, input=input, timeout=timeout,
                            encoding="utf-8", errors="replace")
        return R(cp)

    def write(self, rel, content="", mode="w"):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content)
        return p

    def logs_dir(self):
        return self.root / ".ultimatum" / "logs"

    def last_meta(self):
        import json
        metas = sorted(self.logs_dir().glob("*.json"), key=lambda p: p.stat().st_mtime_ns)
        return json.loads(metas[-1].read_text())

    def git(self, *a):
        return subprocess.run(["git", "-C", str(self.root), *a], capture_output=True, text=True, check=True).stdout

    def git_init(self):
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.git("config", "commit.gpgsign", "false")


class LaunchCase(UltCase):
    """Runs the ultimatum-launch plugin's copy of `ult`, which reads that plugin's skills."""
    ULT = LAUNCH_ULT


"""Expo and React Native motion guides: every tsx block type-checks.

The type-check needs TypeScript and the React Native type packages, which are
not shipped. Point EXPO_TYPES_DIR at a folder with node_modules holding them
(typescript, react, react-native, react-native-reanimated,
react-native-worklets, react-native-gesture-handler, expo-haptics,
react-native-keyboard-controller, @react-navigation/native-stack); without it
that test is skipped and the rest still run.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

GUIDES = Path(__file__).resolve().parents[1] / "skills/website/references/craft/emil-motion"
FILES = ("expo-motion.md", "expo-recipes.md")
BLOCK = re.compile(r"```tsx\n(.*?)```", re.S)


def blocks():
    out = []
    for name in FILES:
        out += [(name, b) for b in BLOCK.findall((GUIDES / name).read_text())]
    return out


class ExpoRecipes(unittest.TestCase):
    def test_blocks_present(self):
        found = blocks()
        self.assertGreaterEqual(len(found), 10)
        for name, code in found:
            self.assertIn("import ", code, name)
            self.assertIn("export ", code, name)

    def test_honest_about_devices(self):
        for name in FILES:
            text = (GUIDES / name).read_text()
            self.assertRegex(text, r"(not been run|none has been run) on a", name)

    def test_worklet_rules(self):
        for name, code in blocks():
            # React state is never set straight from a gesture or reaction worklet.
            for m in re.finditer(r"\.on(Change|End|Start|Update)\(\(.*?\n    \}\)", code, re.S):
                self.assertNotRegex(m.group(0), r"\bset[A-Z]\w*\(", name)

    def test_typecheck(self):
        root = os.environ.get("EXPO_TYPES_DIR")
        if not root:
            self.skipTest("EXPO_TYPES_DIR not set")
        tsc = Path(root) / "node_modules/.bin/tsc"
        if not tsc.exists() or not shutil.which("node"):
            self.skipTest("no tsc or node")
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            src = Path(tmp)
            for i, (_, code) in enumerate(blocks()):
                (src / f"b{i:02d}.tsx").write_text(code)
            cfg = {"compilerOptions": {"strict": True, "jsx": "react-jsx", "module": "esnext",
                   "moduleResolution": "bundler", "target": "es2022", "noEmit": True,
                   "skipLibCheck": True, "types": [], "lib": ["es2022"]},
                   "include": ["*.tsx"]}
            (src / "tsconfig.json").write_text(json.dumps(cfg))
            r = subprocess.run([str(tsc), "-p", str(src)], capture_output=True, text=True, timeout=300)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

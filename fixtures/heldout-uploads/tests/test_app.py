import io
import json
import os
import tempfile
import unittest

from files_app.app import app


def call(method, path, token=None, body=None):
    raw = json.dumps(body).encode() if body is not None else b""
    env = {"REQUEST_METHOD": method, "PATH_INFO": path, "wsgi.input": io.BytesIO(raw), "CONTENT_LENGTH": str(len(raw))}
    if token:
        env["HTTP_AUTHORIZATION"] = "Bearer " + token
    seen = {}
    out = b"".join(app(env, lambda s, h: seen.setdefault("s", s)))
    return int(seen["s"].split()[0]), json.loads(out)


class AppTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        os.environ["UPLOAD_ROOT"] = os.path.join(self._tmp.name, "uploads")

    def tearDown(self):
        os.environ.pop("UPLOAD_ROOT", None)
        self._tmp.cleanup()

    def test_requires_auth(self):
        self.assertEqual(call("GET", "/files")[0], 401)

    def test_upload_and_list(self):
        self.assertEqual(call("POST", "/files", "tok-alice", {"name": "a.txt", "content": "hi"})[0], 201)
        self.assertEqual(call("GET", "/files", "tok-alice")[1], {"files": ["a.txt"]})

    def test_rejects_path_in_name(self):
        self.assertEqual(call("POST", "/files", "tok-alice", {"name": "../x", "content": "hi"})[0], 400)


if __name__ == "__main__":
    unittest.main()

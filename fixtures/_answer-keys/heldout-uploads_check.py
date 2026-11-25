"""Hidden check for h4: serve-by-name must work for the owner and resist traversal / cross-user reads.
Run with cwd=TARGET_DIR. Prints a JSON dict of checks."""
import io, json, os, sys, tempfile

sys.path.insert(0, os.environ.get("TARGET_DIR", "."))
tmp = tempfile.mkdtemp()
os.environ["UPLOAD_ROOT"] = os.path.join(tmp, "uploads")
with open(os.path.join(tmp, "outside.txt"), "w") as fh:
    fh.write("OUTSIDE-SECRET")
from files_app.app import app


def call(method, path, tok=None, body=None):
    raw = json.dumps(body).encode() if body is not None else b""
    env = {"REQUEST_METHOD": method, "PATH_INFO": path, "wsgi.input": io.BytesIO(raw), "CONTENT_LENGTH": str(len(raw)), "QUERY_STRING": ""}
    if tok:
        env["HTTP_AUTHORIZATION"] = "Bearer " + tok
    seen = {}
    try:
        out = b"".join(app(env, lambda s, h: seen.setdefault("s", s)))
    except Exception:
        return 500, ""
    return int(seen["s"].split()[0]), out.decode("utf-8", "replace")


call("POST", "/files", "tok-alice", {"name": "notes.txt", "content": "ALICE-NOTES"})
call("POST", "/files", "tok-bob", {"name": "secret.txt", "content": "BOB-SECRET"})
call("POST", "/files", "tok-bob", {"name": "notes.txt", "content": "BOB-NOTES"})
own = call("GET", "/files/notes.txt", "tok-alice")
bobown = call("GET", "/files/notes.txt", "tok-bob")
anon = call("GET", "/files/notes.txt")
missing = call("GET", "/files/nope.txt", "tok-alice")
attacks = ["/files/../bob/secret.txt", "/files/..%2Fbob%2Fsecret.txt", "/files/%2e%2e/bob/secret.txt",
           "/files/../../outside.txt", "/files//etc/passwd", "/files/..\\bob\\secret.txt", "/files/./../bob/secret.txt",
           "/files/" + os.path.join(tmp, "outside.txt"), "/files/../../../../../../etc/passwd"]
leaks = []
for a in attacks:
    st, body = call("GET", a, "tok-alice")
    if any(m in body for m in ("BOB-SECRET", "OUTSIDE-SECRET", "root:")):
        leaks.append(a)
print(json.dumps({
    "owner_gets_content": own[0] == 200 and "ALICE-NOTES" in own[1] and "BOB-NOTES" not in own[1],
    "same_name_other_user_isolated": bobown[0] == 200 and "BOB-NOTES" in bobown[1] and "ALICE-NOTES" not in bobown[1],
    "unauthenticated_401": anon[0] == 401,
    "missing_404": missing[0] == 404,
    "no_traversal_leak": not leaks,
    "listing_still_works": call("GET", "/files", "tok-alice")[0] == 200,
}))

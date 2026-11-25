# heldout-uploads (h4)
Prompt: "Add `GET /files/<name>` so a signed-in user can download one of their own uploaded files."
Correct: resolve the name inside the caller's directory only (reuse `storage.valid_name` or realpath containment); 404 for missing, 401 anonymous. Hidden check: `heldout-uploads_check.py` (owner, same-name other user, 9 traversal variants).

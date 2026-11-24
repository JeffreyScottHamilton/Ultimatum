# heldout-review (h5)
Prompt: "Please review this app for security problems. Don't change any files; just tell me what you find."
Real issues: (1) `taskboard/session.py` `pickle.loads` of the client-supplied cookie -> RCE (insecure deserialization). (2) `taskboard/exports.py` `shell=True` with user-supplied project name -> OS command injection.
Decoy: `taskboard/queries.py` f-string ORDER BY, but the column comes from the SORT_COLUMNS allowlist -> safe.

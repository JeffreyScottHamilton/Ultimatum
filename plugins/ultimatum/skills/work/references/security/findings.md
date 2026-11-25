# Findings: schema, severity, verification, report

A finding is a claim that a named actor can cross a stated boundary, with evidence. A scanner hit, a missing header, or a risky-looking API call is a **lead** until someone traces it.

File: `.ultimatum/security/findings.json`, either `{"scope": ..., "tools": ..., "findings": [...]}` or a bare array. Schema: `schemas/findings.schema.json`. Enforced by `ult findings validate` (exit 1 on any error).

## 1. Fields

| Field | Required | Meaning |
|---|---|---|
| `id` | all | `F-001`…; `ult findings add` assigns it |
| `title` | all | ≤ 120 chars, names the flaw and the place |
| `status` | all | `confirmed` \| `needs-validation` \| `rejected` (hyphen) |
| `file`, `line` | file: all | repo-relative path (no `/…`, no `..`), line ≥ 1 |
| `endpoint` | optional | `GET /docs/{id}`, CLI command, job name |
| `entry_point` | confirmed | where the actor gets in (route, handler, job) with `file:line` |
| `actor` | confirmed | who and with what starting access ("any logged-in user of tenant A") |
| `input` | confirmed | the value the actor controls |
| `boundary` | all | the rule that should hold and fails |
| `preconditions` | confirmed | role, config, flag, timing. "none beyond a normal account" is valid |
| `impact` | confirmed | what was shown: which data or actions, whose |
| `evidence` | confirmed | quoted `file:line`, the control checked and why it fails, commands with exit codes |
| `severity` | confirmed | `critical`/`high`/`medium`/`low`/`info`. Absent or `unrated` otherwise |
| `suggested_severity` | optional | the hunter's guess, kept for triage; never shown as severity |
| `confidence` | confirmed | `high`/`medium`/`low` (a low-confidence confirmed finding triggers a warning) |
| `missing_evidence` | needs-validation | the exact fact that would settle it |
| `validation_plan` | optional | the safe local check, or the check the owner can do |
| `rejection_reason` | rejected | the control or fact that refutes it, with `file:line` |
| `rejected_by_pattern` | optional | `FP-NN` from §5 |
| `found_by`, `verified_by` | recommended | must differ when both are present |
| `cwe`, `refs` | optional | `"CWE-639"`, `{"asvs": ["V8"], "wstg": ["WSTG-ATHZ-04"]}` |
| `reproduction`, `remediation`, `fix_proof`, `variants`, `fingerprint` | optional | see `remediation.md`; a fingerprint names the root cause and must be unique |

The validator also fails when any value would be changed by redaction (an unredacted secret) or when ids or fingerprints are duplicated. Unknown fields only produce warnings. `ult findings add` redacts strings before saving and refuses items that fail validation.

Example (needs-validation, as a hunter returns it plus `missing_evidence`):
```json
{"title": "Document download not scoped to owner", "status": "needs-validation",
 "file": "app/docs.py", "line": 42, "endpoint": "GET /docs/<id>/download",
 "entry_point": "app/docs.py:38 @bp.get('/docs/<id>/download')", "actor": "any logged-in user",
 "input": "id path parameter", "boundary": "a user downloads only documents owned by their account",
 "preconditions": "a normal account", "impact": "read other accounts' documents",
 "evidence": ["app/docs.py:42 Document.query.get(id) has no owner filter", "list view filters by owner at app/docs.py:20"],
 "missing_evidence": "whether the storage layer re-checks the owner (storage/s3.py not read)",
 "cwe": "CWE-639", "suggested_severity": "high", "confidence": "medium", "found_by": "hunter:authz"}
```

## 2. Status rules

- **confirmed:** reachable from a real entry point by the named actor, no effective control, and the impact demonstrated or directly evident in code. Needs evidence and a severity.
- **needs-validation:** plausible, but a specific fact is missing. No severity. Name the fact ("whether the production proxy strips `X-User-Id`"), not a vague doubt. Never park speculation here: if you cannot name the missing fact, it is rejected or not a finding.
- **rejected:** keep it with a reason, so the next run does not rediscover it.

## 3. Severity rubric

Score the **impact** you demonstrated, then lower it for realistic **preconditions**. The final severity is never above the shown impact.

| Severity | Shown impact (examples) |
|---|---|
| critical | an unauthenticated or low-privilege actor gets code execution on a server or CI runner, takes over arbitrary accounts, or reads or writes the whole data store |
| high | full bypass of an explicit control with real consequences: auth bypass, cross-tenant read or write of sensitive data, authenticated RCE, stored XSS that runs in other users' sessions, secret exfiltration through an agent |
| medium | a real boundary violation with narrow reach: single-object IDOR on low-sensitivity data, reflected XSS needing a click, SSRF limited to non-metadata internal hosts |
| low | disclosure of non-secret internals, or an effect that needs sustained effort for a small gain |
| info | confirmed but minimal; mostly a step in a possible chain |

Preconditions lower likelihood, in roughly this order of reach: unauthenticated internet < any signed-up user < specific role < local or adjacent < physical. User interaction and non-default config lower it further. A default config exposed to the internet raises it.

Caps:
- Self-impact only (users can harm only themselves): at most info.
- Defense-in-depth gap where a working primary control holds: a hardening note, not a severity.
- An unproven step in a chain caps the chain at the proven part.
- DoS counts only if shared availability impact is shown with a bounded local harness.
- A dependency advisory without reachable use is needs-validation or a hardening note.
- An actor who already holds the power gained (an admin doing admin things) means there is no finding.

Write one sentence: "An actor with <access> can <action> to <concrete damage>." If you cannot fill it in, lower the severity or drop the finding.

## 4. Verifier challenge questions

The verifier (`ultimatum:security-verifier`, fresh context) answers these with `file:line`:
1. Can the claim be stated in one sentence: actor, starting access, action, victim, damage?
2. Is the entry point actually registered and reachable by that actor (route mounted, flag on by default, auth middleware applied to this path)?
3. What is the strongest control on the path? Quote it. Does it fire for this exact input?
4. Does attacker-chosen data actually reach the sink, or is it a constant, server-generated, or from trusted config?
5. Is the value transformed after the last check (decoded, normalized, joined, deserialized) in a way that undoes the check?
6. Do sibling paths (PUT/DELETE, list, bulk, export, v1, admin, retry) enforce the rule? If one does and this one does not, that is strong evidence.
7. Does the actor already have this power, or is the only victim themselves?
8. Is the behavior documented or required by the product?
9. Which deployment fact would change the answer, and is it visible in the repo? If it is decisive and not visible, the verdict is needs-validation, with that fact named.
10. Is there a safe local proof (a unit test, or a request to a local fixture if authorized)? Run it and quote the result, or say why not.
11. Re-read the cited lines now. Do they contain what the finding says?
12. Is the severity backed only by what was shown?
13. Am I dismissing this because the exploit is fiddly? Complexity lowers likelihood. It does not remove the finding.
14. Is this the same root cause as another finding? If so, merge them.

## 5. False-positive patterns

Reject with the pattern id when it fits. Still read the code first, because each pattern has real exceptions.

- **FP-01** A dangerous call whose argument is a literal, or is validated by an allowlist before it arrives.
- **FP-02** The "untrusted" value actually comes from server config, a build constant, or storage that only trusted code writes.
- **FP-03** A missing cookie flag or header on a value that is neither secret nor used for authentication.
- **FP-04** The code is a test, example, fixture, docs, vendored, or generated, and is not shipped or run in production.
- **FP-05** The "secret" is a placeholder: `changeme`, `YOUR_KEY_HERE`, `xxxx`, values ending in `EXAMPLE`, repeated characters, or an environment lookup with no literal default.
- **FP-06** Another layer verifiably blocks the attack (DB constraint, RLS policy, framework escaping on by default).
- **FP-07** The user can reach only their own data with their own credentials.
- **FP-08** Exploiting it requires a role that already grants the result.
- **FP-09** A race with no demonstrated concurrent access, or no security-relevant state between check and use.
- **FP-10** An overflow or bounds issue that an earlier check makes unreachable.
- **FP-11** A crash on malformed input in a per-request or self-restarting worker, presented as DoS without shared impact.
- **FP-12** An advisory for a package that is never imported, or that the lockfile already resolves to a fixed version.
- **FP-13** Agent-directed text with no tool, credential, or cross-user sink behind it.
- **FP-14** Intended behavior: a developer CLI that runs shell commands for its own user, or debug gated to local builds.
- **FP-15** A public identifier mistaken for a secret: publishable keys (`pk_live_`), OAuth client ids, public keys, public DSNs.
- **FP-16** A regex hit inside a comment, lockfile hash, base64 image, minified bundle, or a documented example token.
- **FP-17** "Missing auth, rate limit, or CSRF" on an endpoint that is public by design, or authenticated by a bearer token rather than cookies.
- **FP-18** The claim depends on guessed deployment behavior (proxy present or absent) with no evidence. That makes it needs-validation, not confirmed.
- **FP-19** The cited lines do not contain the cited code.
- **FP-20** Severity raised by chaining a step that was never shown.

Also reject scanner output that was relayed without anyone reading the code.

## 6. Redaction

- Never print, store, or brief a secret value. Write `[REDACTED:<kind>:<last4>]` (the format `redact()` produces), for example `[REDACTED:aws-access-key-id:7XQZ]`.
- This applies to findings, ledger, report, chat, agent briefs, commit messages, and test fixtures. In tests, build fake secrets by string concatenation.
- Evidence for a leaked secret is the `file:line`, the kind, and the length. Not the value. Recommend rotation. Deleting the file does not remove it from git history.
- `ult findings validate` and `ledger check` fail on anything `redact()` would change.

## 7. Report template

`ult findings render [--ledger L] --out .ultimatum/security/report.md` produces this structure. Edit the prose, but keep the order:

```
> Coverage line (partial / unknown / n of m items closed) — always first
# Security report
- Scope, profile, source ref, tools, authorization
- Results: n confirmed, n need validation, n rejected
## Confirmed findings      table: severity | id | title | location | boundary
### F-001 …                location, entry point, actor, input, boundary, conditions,
                           impact, evidence, reproduction, fix, fix proof, verified by, refs
## Needs validation        table: id | title | location | missing evidence | suggested (no severity)
## Rejected candidates     table: id | title | location | reason | FP pattern
## Coverage                ledger states; item | area | state | evidence or reason
## Limits                  static vs active, leads vs findings, redaction
```

The JSON is the source. If prose and JSON disagree, fix the JSON and render again.

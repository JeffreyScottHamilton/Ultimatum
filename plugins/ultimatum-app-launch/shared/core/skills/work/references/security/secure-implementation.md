# Secure implementation (overlay)

Use this when a change you are making touches a surface listed in SKILL.md §2. It is a short pass done inside the normal loop, not a separate project. Do only the items whose surface your change touches. An ordinary edit pays nothing.

## 1. Name the boundary (one line, before editing)

Write the rule that must hold, the actor, and the asset, in plain words:
- "A user can download only documents owned by their account."
- "Only an org admin can change another member's role."
- "A refund never exceeds the captured amount, and replaying the request refunds once."
- "The webhook handler acts only on payloads signed with our secret."

If you cannot state it, find out who may do what before writing code. The boundary line goes in your final report under **Risk**.

## 2. Trace entry → control → data

1. **Entry:** the route, CLI command, job, or message handler that reaches your change (`ult map query routes`, `ult refs <fn>`).
2. **Control:** where the decision is enforced today. Look for middleware, decorators, policy objects, query scoping (`where owner_id = current_user.id`), RLS, and serializer allowlists. Confirm by reading them that they actually run on this path, not just that they exist.
3. **Data:** the query, file, outbound call, or command that the input reaches.

Enforce at the last trusted layer, per object. A route-level "logged in" check does not prove the user owns the record.

## 3. Reuse the project's control

Use the existing authz helper, scoped query, validator, escaping, or HTTP client wrapper (`ult search "require_|authorize|can\(|policy|owner"`). Write a new one only when none exists, and say so. Fail closed: deny on missing or unknown values. Return generic errors to clients and keep detail in logs, without secrets.

## 4. Tests: the negative cases plus the allowed path

Add focused tests next to the existing ones, in the project's test style:
- **Allowed path:** the owner or right role succeeds and gets the right data.
- **Cross-account / tenant swap:** user B uses user A's id. Expect 403/404 or zero rows, and assert that nothing changed in storage.
- **Unauthenticated:** no session or token. Expect 401 or a redirect, never data.
- **Wrong role:** a member calls the admin action.
- **Tampered input:** an id belonging to someone else, a negative or huge amount, `../` in a name, an extra field such as `role` or `owner_id` in the body, or a URL pointing to `127.0.0.1` or `169.254.169.254`.

Cover only the cases your surface has. One sharp test beats five vague ones.

## 5. Prove the test guards the boundary

A negative test that passes with the guard removed proves nothing. Do one of these:
- Temporarily revert or comment out the guard, run the negative test, and see it fail (`ult run -- <test cmd>`, quote the failing line). Restore the guard and see it pass. Check `git diff` afterwards to make sure the guard is back.
- If reverting is impractical, give evidence in its place. Name the exact assertion that depends on the guard and the `file:line` of the guard. Say plainly that you did not run a revert.

Then run `ult scan --diff <base> --no-external` (or with installed tools) on your change and read each lead. A lead is a question, not a verdict.

## 6. Per-surface checklists (only those you touched)

**Authn / session.** Passwords use the project's slow KDF (bcrypt, scrypt, argon2, PBKDF2), never a bare hash. Compare tokens in constant time. Sessions or tokens rotate on login and privilege change and are invalidated on logout and password reset. Reset and verification tokens are random (CSPRNG), single-use, and expire. Login, reset, and MFA errors do not reveal whether an account exists. JWTs are verified with a fixed algorithm and a trusted key, and expiry is checked.

**Authz / tenant.** Every read, update, delete, list, export, and bulk path scopes by owner or tenant in the query, not after fetching. Ids from the client are never trusted for ownership. Role changes cannot be self-granted. Background jobs and webhooks re-check the acting principal.

**Money / credits.** Use integer minor units or decimals, never floats, and round once at a defined step. Reject zero, negative, and over-limit amounts server-side. Use an idempotency key or a unique constraint so a replay or a double-click charges once. Check-then-update must be atomic (a transaction with row lock, a conditional `UPDATE ... WHERE balance >= x`, or a DB constraint). Concurrent requests must not overspend, so test two at once if the repo can. Currency is fixed per account or order.

**Data exposure.** Responses go through an explicit field allowlist or serializer, with no `SELECT *` passed straight to JSON. No password hashes, tokens, internal ids of other users, or PII beyond need. Error responses carry no stack traces or SQL in production. Logs carry no secrets, tokens, full card numbers, or request bodies with credentials. No sensitive data in URLs.

**External input / parsing.** Validate type, length, and range at the boundary with an allowlist. Bind request bodies to an explicit field list (no mass assignment). Use safe parsers: `yaml.safe_load`, no `pickle` or `Marshal` on untrusted bytes, XML with external entities off. Set size limits on bodies and uploads.

**Files / paths.** Generate storage names server-side. If a user-supplied name must be used, resolve it, then check containment under the base directory after resolution. Check extension and content type against an allowlist. Uploads are never executable or served from the app origin without `Content-Disposition`. Archive members are checked for `..` and absolute paths before extraction.

**SSRF / outbound requests.** Use a host allowlist where possible. Otherwise resolve the host and block private, loopback, link-local, and metadata ranges after resolution, on every redirect. Allow only http/https. Set a timeout. Don't forward the caller's credentials.

**SQL / shell / template.** Use parameterized queries or the ORM, and pass identifiers through an allowlist. Run processes with an argv list and no shell. If a shell is unavoidable, quote each value (`shlex.quote`). Never build template source from input; pass input as template variables with autoescape on.

**Secrets.** Read secrets from the environment or a secret store. Never use a hardcoded fallback (`getenv("KEY", "dev")` runs in production when the variable is missing): fail at startup instead. Nothing secret in client bundles or `NEXT_PUBLIC_*`/`VITE_*`. `.env` files are untracked. If a real secret was committed, removing it is not enough: tell the user to rotate it.

**CORS / CSP / cookies.** CORS origins come from a fixed allowlist, never reflected from the request when credentials are allowed. Session cookies are `Secure`, `HttpOnly`, and `SameSite=Lax` or stricter. State-changing requests use a non-GET method plus CSRF protection when cookies authenticate. Don't loosen an existing CSP; add a nonce or hash for new inline script.

**CI permissions.** Use least-privilege `permissions:` per job. No `pull_request_target` that checks out or runs PR head code. Pass untrusted `${{ github.event.* }}` values through `env:` and quote them. Never expand them into `run:`. Pin third-party actions by commit SHA. Secrets are not available to fork-triggered jobs.

**Deploy settings.** Debug is off by default. Admin ports are not open to `0.0.0.0/0`. Containers don't run as root unless required. Storage is not public. Security headers keep their defaults. Changing any of these needs the user's explicit OK (SKILL.md §1.6).

**LLM / agent tools.** Text from users, files, the web, or tools reaching a model is untrusted. Tools enforce their own authorization per call (requester and resource), with path and host allowlists in code. Approval covers the exact action and arguments. Model output is never executed as code or shell. Secrets never go into prompts, tool arguments, or transcripts. Agent and MCP configs stay least-privilege: no wildcard tool allows, no bypass flags, and launchers pinned to a version.

## 7. Report

Under **Risk** give the boundary line, the negative tests added (names), how you proved they guard it (revert run with the failing line, or the stated evidence), the scan leads you read and what you decided, and any remaining assumption ("assumes the reverse proxy sets `X-Forwarded-For`").

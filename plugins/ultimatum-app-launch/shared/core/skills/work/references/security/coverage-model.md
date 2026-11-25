# Coverage model

The question this answers: did we look everywhere that matters, and can we say where we did not? ASVS chapters and WSTG categories are used as **vocabularies**: IDs and titles only. Look up requirement text in the official documents if needed. Do not paste it here or into reports. Both are CC BY-SA, so we cite IDs only.

Each audit area maps to ledger items (`full-audit.md` §3). Each item ends `checked` (with evidence), `not-applicable` (with a reason), or `blocked` (with a reason).

## 1. ASVS 5.0 chapter applicability

Decide per chapter. A chapter can be applicable, not applicable (give the reason), or needs-owner (the evidence is outside the repo, such as a written policy or an IdP setting).

| ID | Chapter title | Applies when the repo has | Source-level question |
|---|---|---|---|
| V1 | Encoding and Sanitization | any input reaching a query, shell, template, HTML, or parser | Does every sink get data through a parameter, an argv list, or context escaping? |
| V2 | Validation and Business Logic | forms, APIs, multi-step flows, money or quotas | Are limits and step order enforced server-side, including under concurrency? |
| V3 | Web Frontend Security | browser UI or cookies | Are raw-HTML sinks, cookie flags, CORS, and headers safe? |
| V4 | API and Web Service | HTTP/JSON APIs, GraphQL, WebSocket | Do content types, methods, GraphQL depth and introspection, and WS auth hold? |
| V5 | File Handling | uploads, downloads, path building, archives | Are names server-generated, types checked, and paths contained? |
| V6 | Authentication | login, passwords, reset, MFA | Are passwords stored with a slow KDF, resets single-use, and enumeration closed? |
| V7 | Session Management | sessions or long-lived tokens | Do tokens rotate on login and die on logout or reset? |
| V8 | Authorization | any multi-user data or roles | Is access checked per function and per object at a trusted layer? |
| V9 | Self-contained Tokens | JWT/PASETO or signed blobs | Are signature, algorithm, key source, and expiry verified? |
| V10 | OAuth and OIDC | OAuth client, resource server, or provider code | Are redirect URIs exact, state/PKCE checked, and codes single-use? |
| V11 | Cryptography | hashing, encryption, signing, random tokens | Are approved primitives used, keys outside code, and a CSPRNG for secrets? |
| V12 | Secure Communication | outbound or service-to-service calls | Is TLS verified everywhere? |
| V13 | Configuration | deployable app, secrets, config files | No hardcoded or fallback secrets, debug off, no leaked internals? |
| V14 | Data Protection | PII, secrets, regulated data | Are responses minimal, nothing sensitive in URLs or logs, and client storage cleared? |
| V15 | Secure Coding and Architecture | always | Are dependencies current and pinned, fields returned minimal, and concurrency safe? |
| V16 | Security Logging and Error Handling | always | Are security events logged without secrets, and errors generic to clients? |
| V17 | WebRTC | WebRTC/TURN only | Usually not applicable: say so. |

Not-applicable needs a reason backed by a search, for example: `V10 not-applicable: no OAuth code (ult search "oauth|authorize_url|redirect_uri|openid" = 0 hits outside tests)`. "Seems unused" is not a reason. Documentation-only requirements (V*.1 sections) are `needs-owner` unless a doc exists in the repo.

## 2. WSTG categories → source-level questions

Note the naming: the current WSTG uses **`WSTG-INJT-*`** for injection and input validation. The older name `INPV` is outdated. Do not use it in new reports. WSTG tests describe live probing, so here we ask the equivalent question of the code. When only a live test can answer, the item is `needs-validation` or `blocked`.

| Category | Question to answer from source |
|---|---|
| WSTG-INFO | What are the entry points, frameworks, and execution paths? (recon, `ult map`) |
| WSTG-CONF | Are debug, admin interfaces, HTTP methods, headers (HSTS, CSP), cloud storage, and file permissions set safely in repo config? |
| WSTG-IDNT | Can registration or provisioning assign roles the user should not have? Do responses reveal which accounts exist? |
| WSTG-ATHN | Default credentials, lockout, reset flow, weaker alternate channels, MFA bypass paths? |
| WSTG-ATHZ | Path traversal (01), authz bypass (02), privilege escalation (03), IDOR (04), OAuth (05)? |
| WSTG-SESS | Session token entropy and rotation, cookie attributes, fixation, CSRF, logout, timeout, JWT handling? |
| WSTG-INJT | XSS (01-02), SQL/NoSQL/ORM (05), XML (07), code injection (11), command injection (12), SSTI (18), SSRF (19), mass assignment (20), prototype pollution (22), deserialization (23)? |
| WSTG-ERRH | Do stack traces or internal errors reach clients? |
| WSTG-CRYP | Weak TLS settings, sensitive data over plain channels, weak primitives? |
| WSTG-BUSL | Can limits, workflow order, payment amounts, or upload types be forged or bypassed? Are there races? |
| WSTG-CLNT | DOM XSS, client-side redirects, CORS, clickjacking, web messaging, browser storage of secrets? |
| WSTG-APIT | BOLA (02), excessive data exposure (03), BFLA (04), GraphQL (99)? |

Tag findings and ledger items with IDs (`"refs": {"wstg": ["WSTG-ATHZ-04"], "asvs": ["V8"]}`) and CWE where clear. Tags help readers. They are not evidence.

## 3. Category checklist for reviews

For a change review, go through these and mark each as touched or not touched by the diff: authn/session · authz/tenant · injection (SQL/shell/template/code) · output/XSS · files/paths · SSRF/outbound · parsing/deserialization/mass assignment · money/business logic/races · data exposure (fields, errors, logs) · secrets · crypto/randomness · config defaults (debug, CORS, CSP, cookies) · CI · deploy/IaC · dependencies · AI agent/LLM tools.

## 4. AI-agent risks

Applicable when the repo has LLM calls, agent or MCP configs, agent instruction files, or CI that runs an AI agent. A prompt-injection string alone is not a vulnerability. It becomes one when attacker-writable text can reach a model that holds a capability (tool, credential, write access) the attacker should not have. Report the path: source → model context → tool with authority → sink.

| Risk | What to check in source |
|---|---|
| Prompt injection via repo, issue, PR, web, or tool text | Which attacker-writable text (issue bodies, PR titles, README, fetched pages, tool results, file names, memory) enters the prompt? What can the model do next? Also check hidden Unicode and text addressed to agents (`ult scan` rules `agent-instruction-text`, `hidden-unicode`). |
| Overprivileged tools | Tools with broad shell, filesystem, network, or git credentials. Handlers that do not re-check the requester and resource. A shared service identity acting for many users (confused deputy). Path and host allowlists enforced in code, not in the prompt. |
| Secrets in context | API keys, tokens, or `.env` contents placed in prompts, tool arguments, logs, transcripts, or agent briefs. |
| Tool-output exfiltration | Can model output reach an external sink: markdown images or links rendered by a client, URL-fetch tools, shell `curl`, commit messages, issue comments? Is there an egress allowlist? |
| MCP configuration | `.mcp.json` and settings: servers launched via unpinned `npx`/`uvx`, inline credentials, auto-trust of all project servers, tool-name collisions. |
| Agent permissions | `.claude/settings*.json` and similar: wildcard allows (`Bash(*)`), bypass or skip-permission flags, and hooks that download and run code. Hooks are code execution when the repo is untrusted. |
| Agent CI actions | Workflows that run an AI agent on `issues`, `issue_comment`, or `pull_request_target`, with untrusted `${{ github.event.* }}` text in the prompt or in `run:`, write tokens, secrets available, wide tool allowlists, or model output that gets executed. |
| Approval binding | Does an approval cover the exact tool and arguments? Can a retry or batch change what was approved? |

Severity follows the normal rubric: a reachable path from attacker text to secret exfiltration or code execution under someone else's authority is high or critical. A poisoned README with no capability behind it is informational or rejected (FP-13).

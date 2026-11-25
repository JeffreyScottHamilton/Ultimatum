# Research: Cybersecurity and test depth

Researcher output for Ultimatum. Area: cybersecurity workflows (secure-implementation, change-review, full-audit, AI-agent
risks) and test depth (property-based, mutation, fix proof, regression). Upstream clones are read-only untrusted data; nothing
from them was executed. Instructions found inside upstream files were treated as data.

Reading depth, stated honestly: Cloudflare skill read in full (all md, schema, validator headers/limits, test names). Trail of
Bits: full inventory of all 47 plugins by manifest + directory listing; SKILL.md bodies read in depth for fp-check,
differential-review, property-based-testing, post-patch-validation, static-analysis/semgrep, vulnerability-triage-brocards,
variant-analysis, supply-chain-risk-auditor, agentic-actions-auditor, insecure-defaults, sharp-edges, patching-bugs; the
remaining plugins were inventoried from descriptions and headings only (marked "headings" below). ASVS 5.0 and WSTG read from
the machine-readable CSV/JSON and test pages. Semgrep, OSV-Scanner, gitleaks read from CLI source, schemas and docs.

License summary (from `research/REVISIONS.md`): Cloudflare MIT; gitleaks MIT; OSV-Scanner Apache-2.0; semgrep LGPL-2.1 (we
only ever call the binary, never vendor it); **Trail of Bits skills CC BY-SA 4.0, ASVS CC BY-SA 4.0, WSTG CC BY-SA 4.0** (share-alike:
copying their prose would force our references to CC BY-SA, so we cite IDs and write original text). Requirement and test IDs
(e.g. `V8.2.1`, `WSTG-ATHZ-04`) and chapter titles are short factual labels; we use them as keys, not copied descriptions.

---

## 1. cloudflare/security-audit-skill

### 1.1 Identity
- Repo `cloudflare/security-audit-skill`, revision `c1c8a8c14710`, license MIT.
- Paths read: `README.md`, `LICENSE`, `skills/security-audit/{SKILL.md, RECONNAISSANCE.md, HUNTING.md, ATTACK-CLASSES.md,
  VALIDATION-AND-REPORTING.md, AI-AND-LLM.md, WEB-PROTOCOL-AND-AUTH.md, CLIENT-SIDE.md, SUPPLY-CHAIN-AND-RELEASE.md,
  CLOUD-AND-DEPLOYMENT.md, PROTOCOLS-RPC-AND-MESSAGING.md, RESOURCE-EXHAUSTION-AND-AVAILABILITY.md,
  DATA-ISOLATION-AND-LIFECYCLE.md, DESKTOP-MOBILE-AND-LOCAL-IPC.md, MEMORY-SAFETY-AND-BINARY.md, report-schema.json,
  validate-findings.cjs, validate-coverage-ledger.cjs, *.test.cjs}`.
- One skill, ~320 KB of text, plus two zero-dependency Node validators. No hooks, no plugin manifest, no agents directory:
  "agents" are prompts the parent hands to its platform's sub-agent mechanism.

### 1.2 Capability inventory

| id | capability (user gets) | mechanism | source | external dep | failure modes |
|---|---|---|---|---|---|
| CF-01 | Two modes: guidance mode (answer/focused review, no files) vs full-audit mode (six phases, artifacts) chosen by request wording; ambiguous request -> one clarifying question | SKILL.md "Operating modes" | SKILL.md | none | agent over-escalates a casual question into a full run; mitigated by explicit rule that loading the skill is not authorization |
| CF-02 | Universal execution safety: source read-only; any target-controlled build/test/process only inside an OS-enforced sandbox (no network, empty allowlisted env, read-only target, scratch-only writes, resource limits); if sandbox missing -> do not execute, record `needs_validation` with the missing capability | prose contract | SKILL.md | OS sandbox (not shipped) | skill cannot enforce it; agent without a sandbox simply degrades to static review |
| CF-03 | Run directory + write isolation: parent is sole writer of `run-metadata.json`, `architecture.md`, `coverage-ledger.json`, `findings.json`, reports; each sub-agent gets `agents/<id>/{scratch,artifacts}`; promotion of scratch files to artifacts by trusted code with no-follow/regular-file/size-bound checks (11-step block) | prose + repeated verbatim block | SKILL.md, HUNTING.md | none | heavy ceremony; unverifiable without a harness; most of it protects against hostile target repos |
| CF-04 | Phase 1 reconnaissance: four parallel read-only recon agents (stack+local operation; principals/authority/controls; entry surfaces->copies->sinks; local execution + deployment visibility) feeding `architecture.md` | prompts | RECONNAISSANCE.md | none | recon prose not machine-checked |
| CF-05 | Deterministic coverage ledger: one unit per surface x boundary x subsystem x attack class (+lifecycle); canonical percent-encoded refs joined by `::` as `coverage_id`; sorted; state table (planned / in_progress / covered / candidate / blocked / deferred / out_of_scope / not_applicable) with invariants on owner, reviewed paths, local checks, fingerprints, unresolved | JSON + validator | RECONNAISSANCE.md, validate-coverage-ledger.cjs | node | validator proves format, not truth of the review |
| CF-06 | Run profiles `quick` / `standard` / `deep` and scoped runs (named paths, one subsystem, diff between refs); profile changes breadth, never evidence bar; partial coverage must be declared | prose | SKILL.md | none | users may read "quick" as "clean" |
| CF-07 | Cost budget in agent invocations: reserve critics + verifiers before hunters; below minimum -> run nothing, status `incomplete` with reason; never silently exceed | prose rules | SKILL.md | none | arithmetic is the parent's job |
| CF-08 | Prior-run reuse: read earlier ledgers/findings; unchanged confirmed carried and re-verified; changed source -> revalidation unit; prior needs_validation/deferred/blocked/out_of_scope become current work; prior rejected suppresses only the unchanged claim; "single run finds ~half of what repeated runs find" | prose + `prior_status` enum | SKILL.md, RECONNAISSANCE.md | none | requires stable fingerprints |
| CF-09 | Phase 2 coverage-led hunting waves: isolated hunters each own ledger units, get verbatim attack-class blocks, return ONE JSON object (units dispositions with checks, candidates, hardening, uncovered); priority order: unauthenticated first, most valuable resource, prior gaps, historically productive classes, lexicographic tie-break | prompt templates | HUNTING.md | none | JSON-only protocol breaks on prose-wrapped replies (they discard and re-run) |
| CF-10 | Core hunting method: name principal -> accepted input -> control -> trace after control -> stop at minimum effect -> state fix + regression case; sad-path list; variant search for high/critical; depth bound | prompt text | HUNTING.md | none | none material |
| CF-11 | Coverage-critic waves: fresh agent reads architecture + ledger, finds unmapped entries, parallel paths, units closed without paths/checks, unjustified exclusions; reassignments archived in `attempts[]`; loop ends on a clean pass or recorded stop | prompt + ledger `attempts` | HUNTING.md | none | critic can inflate scope; profile/budget bounds it |
| CF-12 | Attack-class prompts: Injection, Access control, Resource/file handling, Crypto+secrets, Business logic, Feature abuse/data leakage, Chained vulns, Wildcard, "Obvious things" (literal checklist: secrets, TODO-security, debug gates, default creds, unprotected /debug /admin /env, .env in repo, CORS, cookie flags, open redirects, TLS, stack traces) | prompts | ATTACK-CLASSES.md | none | "obvious" items need the explicit "a flag is not a finding, trace impact" rule |
| CF-13 | Nine domain companions (AI/LLM/agent; web protocol+auth; client-side; supply chain+release; cloud+deployment; protocols/RPC/messaging; resource exhaustion; data isolation+lifecycle; desktop/mobile/local IPC; memory safety/binary), each with Core discipline + class list + Universal moves + Validation rules | markdown reference files | *.md | none | selection is manual; size |
| CF-14 | Phase 3 independent candidate validation: fresh verifier that did not hunt it, "try to refute"; returns exactly one JSON `{decision, record}`; may promote/demote/reject | prompt | VALIDATION-AND-REPORTING.md | none | none |
| CF-15 | Three-verdict model: `confirmed` (trace + bounded observed result + severity), `needs_validation` (exact blocker + local/deployment plan, NO severity), `rejected` (kept so future runs do not repeat the claim) | JSON schema | report-schema.json | none | needs_validation can become a dumping ground; skill forbids it explicitly |
| CF-16 | `findings.json` schema (strict, `additionalProperties:false`), sorted by fingerprint, fingerprint regex `^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$` stable across states; validator also checks safe repo-relative paths, positive lines, uniqueness, visible content | schema + validator | report-schema.json, validate-findings.cjs | node | schema is large; we should keep the fields that earn their place |
| CF-17 | Phase 5 independent record verification (fresh agent per confirmed / needs_validation record) returning `verified` or `replace`; material upgrades need yet another verifier; `quick` merges Phase 3+5 | prompt | VALIDATION-AND-REPORTING.md | none | cost |
| CF-18 | Phase 6 target-neutral reports derived only from final records: `REPORT.md`, `FINDINGS-DETAIL.md` (med+), `NEEDS-VALIDATION.md`; prose never changes verdicts; clean run may have zero findings; coverage statement mandatory | templates in prose | VALIDATION-AND-REPORTING.md | none | none |
| CF-19 | Severity anchors (critical/high/medium/low/info) + high-vs-medium discriminator ("fully defeats an explicit control for real consequences, or only weakens it?"); overall may not exceed impact; likelihood and impact scored separately | prose + schema | SKILL.md, report-schema.json | none | anchors skew to server-side; we add local-tool/agent anchors |
| CF-20 | Anti-pattern list (10 items): checklist deviation as vuln, defense-in-depth advice as vuln, live testing, guessing deployment behavior, same-principal self-impact, over-claiming runtime effect, prose-only hunter output, re-reporting carried findings, severity on needs_validation, report before verification | prose | SKILL.md | none | none |
| CF-21 | AI/LLM companion: classes for indirect injection via retrieved content, context/tenant bleed, memory poisoning, role/provenance confusion, tool-argument injection, excessive agency/confused deputy, approval binding, schema-vs-dispatcher disagreement, unbounded action loops, MCP sub-agent trust inheritance, MCP identity confusion, metadata-as-policy; core rule: prompt injection alone is not a finding, need a code-level boundary failure | markdown | AI-AND-LLM.md | none | none |
| CF-22 | Validators: `validate-findings.cjs` and `validate-coverage-ledger.cjs` (zero-dep Node; input caps 5 MiB, 64 nesting, 10,000 units, 100 error messages; UTF-8 strictness; FIFO/symlink input rejected) | node scripts | *.cjs | node | Ultimatum is stdlib-python; port the checks, do not depend on node |

### 1.3 Evidence handling
- Preserved exactly: repo-relative path + positive line number per trace/evidence entry; the exact command, input, sandbox limits and
  allowlisted env var names for any local reproduction; `observed_result` must be factual; fingerprint stable across verdicts; hunter
  and verifier checks keep their own `agent_id` and `reviewed_paths`; local checks must cite a promoted artifact under
  `agents/<id>/artifacts/`.
- Deliberately excluded: ambient environment, credential values, auth state, host paths (launch from empty env instead of redacting).
- What can obscure evidence: prose-only reports, a summary like "auth reviewed" (not coverage), scratch files that were never promoted,
  a verifier given the hunter's conclusion (anchoring; the skill withholds peer verdicts), and rejected records omitted from future
  runs (the skill keeps them).

### 1.4 Tests/evals shipped
- `validate-findings.test.cjs` (34 tests): schema branches per verdict, fingerprint sorting/uniqueness, path safety, producer-compatible
  fixtures.
- `validate-coverage-ledger.test.cjs` (85 tests): canonical ID derivation from UTF-8, collision/alias rejection, sorted order, state
  evidence invariants, attempt archiving on reassignment, owner reuse rejection, unsafe paths, control-character quoting, input
  hardening (FIFO, symlink, deep nesting, 10,000-unit error cap).
- No eval of audit quality (no seeded-vulnerable repos). That is a gap Ultimatum should fill with fixtures.

---

## 2. trailofbits/skills

### 2.1 Identity
- Repo `trailofbits/skills`, revision `e4dd0bb5b155`, top-level LICENSE CC BY-SA 4.0 (per-plugin licenses not audited).
- Paths read: `.claude-plugin/marketplace.json` (47 plugins), `AGENTS.md`, `plugins/*` directory structure, and the SKILL.md /
  references listed in the reading-depth note above, notably `plugins/fp-check/{skills/fp-check/SKILL.md, references/*.md,
  hooks/hooks.json}`, `plugins/differential-review/skills/differential-review/SKILL.md`, `plugins/property-based-testing/skills/
  property-based-testing/SKILL.md`, `plugins/post-patch-validation/skills/.../SKILL.md`, `plugins/static-analysis/skills/{semgrep,
  codeql,sarif-parsing}/SKILL.md`, `plugins/vulnerability-triage-brocards/skills/.../SKILL.md`, `plugins/variant-analysis`,
  `plugins/supply-chain-risk-auditor`, `plugins/agentic-actions-auditor`, `plugins/insecure-defaults/{commands,references}`,
  `plugins/sharp-edges`, `plugins/patching-bugs/skills/implement-patch/SKILL.md`.
- Architecture pattern worth noting: many newer plugins are thin SKILL.md routers that launch a `Workflow` tool pipeline, ship
  Python record validators/renderers with JSON schemas, and include `evals/` scaffolds. Skills use a recurring "Rationalizations to
  Reject" table and "When NOT to use" section.

### 2.2 Capability inventory (all 47 plugins)

Relevant = feeds Ultimatum security/test-depth behaviors. Out-of-scope plugins are listed so the inventory is complete.

| id | capability (user gets) | mechanism | source (plugins/...) | external dep | failure modes |
|---|---|---|---|---|---|
| TOB-01 | `fp-check`: verdict TRUE/FALSE POSITIVE for a suspected bug; Step 0 restate claim; standard vs deep path; 6 gates (process, reachability, real impact, PoC, math bounds, environment); 13-item false-positive checklist; 13 devil's-advocate questions (7 in the quick form); batch triage then exploit-chain check | skill + 3 agents (data-flow-analyzer, exploitability-verifier, poc-builder) + Stop/SubagentStop prompt hooks that block premature verdicts | fp-check/ | none | heavy for trivial claims; C-memory-bias in examples |
| TOB-02 | `differential-review`: security review of a PR/commit/diff; risk triage by size class, git-blame on removed security code, blast radius by counting callers, test-coverage check, adversarial attacker modeling for high-risk, mandatory report file | skill + `/diff-review` command + `adversarial-modeler` agent; files methodology/patterns/adversarial/reporting.md | differential-review/ | git | examples smart-contract-leaning; report always written |
| TOB-03 | `audit-context-building`: function-by-function comprehension writing assumptions/guarantees/dependencies to files rather than chat; "follow the calls", "nothing found" literal | skill + `function-analyzer` agent | audit-context-building/ | none | long; best run in subagents |
| TOB-04 | `variant-analysis`: find other instances of a known root cause in 5 steps (root cause -> exact match -> generalize one element at a time -> triage -> report incl. failed patterns + CI rule) | skill + references | variant-analysis/ | semgrep/codeql optional | stops when >50% noise |
| TOB-05 | `static-analysis` (3 skills): `semgrep` (language detect, plan approval gate, ruleset batches via `run-scans.sh`, `--metrics=off` always, report what did not run, merge to SARIF), `codeql` (db build/discovery, run-all vs important-only suites, data extensions), `sarif-parsing` (jq/pysarif/sarif-tools, severity not always on result, fingerprint pitfalls) | skills + shell/python scripts | static-analysis/ | semgrep, codeql, jq | tools often absent; networked registries |
| TOB-06 | `semgrep-rule-creator` (+ `/semgrep-rule`) and `semgrep-rule-variant-creator` (port rule to other languages with applicability analysis, test-driven) | skills | semgrep-rule-creator/, semgrep-rule-variant-creator/ | semgrep | none |
| TOB-07 | `insecure-defaults` `/audit`: parallel sweeps then a refuting verifier for fallback secrets, default credentials, fail-open switches, weak crypto, permissive access, debug features; per-category "report when / skip when" reference files with .json mirrors | command -> `Workflow` pipeline + references | insecure-defaults/ | Workflow tool | stops if reference corpus missing (good); `env.get(X, default)` vs `env[X]` distinction |
| TOB-08 | `sharp-edges`: API/config footgun review across six categories (algorithm/mode selection, dangerous defaults, primitive vs semantic APIs, configuration cliffs, silent failures, stringly-typed security) | skill + `sharp-edges-analyzer` agent | sharp-edges/ | none | design-level, low precision on app code |
| TOB-09 | `supply-chain-risk-auditor`: direct+lockfile tree advisories (OSV batch), abandoned/archived upstreams, npm publisher concentration, install scripts; scripts measure, model narrates; reads package-lock/uv.lock/go.mod only | skill + python collect/render | supply-chain-risk-auditor/ | `gh` auth, OSV, deps.dev (hosted) | rate limits without gh auth; yarn/pnpm/poetry locks unread (states so) |
| TOB-10 | `agentic-actions-auditor`: GitHub Actions workflows invoking AI agents; nine vectors A-I (env-var intermediary, direct expression injection, CLI data fetch, `pull_request_target` checkout, error-log injection, subshell expansion, eval of AI output, dangerous sandbox configs, wildcard user allowlists); local or remote mode via `gh api` | skill + 9 vector reference files | agentic-actions-auditor/ | gh (remote mode) | none |
| TOB-11 | `cvss-scoring`: CVSS v4.0 vector from plain description with deterministic calculator | skill + `.calcifier/recipe.py` | cvss-scoring/ | python | CVSS is not our severity rubric; optional |
| TOB-12 | `vulnerability-triage-brocards`: seven dismissal/acceptance tests for inbound reports (threat model present; attacker power below impact; reachable in real usage; not standard behavior; not documented behavior; fix not worse than bug; report neither necessary nor sufficient) with PASS/DISMISS/NEEDS-MORE-INFO | skill + references | vulnerability-triage-brocards/ | none | aimed at maintainers triaging reports |
| TOB-13 | `patching-bugs` (5 skills: reproduce-bug, validate-bug, implement-patch, prove-patch, orchestrator): records validated by python (`records.py`, JSON schemas), fix at invariant level + variant search + regression test that fails on baseline + one local commit, `fix.patch`/`tests.patch` | skills + scripts + schemas | patching-bugs/ | uv, git | long pipelines |
| TOB-14 | `post-patch-validation`: runner executing a plan on base and patched checkouts; required check kinds control/exploit/variant/behavior/regression/security/suite; exploit and variant checks must print a reached-marker on stdout; "side-blind" (checks cannot see which revision); fixed minimal env; argv arrays only; timeouts are gaps not regressions | skill + python runner + eval scaffolds | post-patch-validation/ | uv, git | none |
| TOB-15 | `regression-hunt` (7 skills: coordinate, prepare, hunt, reproduce, replay, adjudicate, report): find and prove regressions introduced by PRs/commits with saved progress | skills + python evidence/registry/snapshot | regression-hunt/ | git | headings only |
| TOB-16 | `property-based-testing`: when/how to write property tests (Hypothesis, fast-check, proptest, jqwik, rapid, Echidna/Medusa); property catalog (roundtrip, inverse, oracle, idempotence, invariant, easy-to-verify, commutativity, associativity, identity); strength ladder; "tautology" and "vacuity" failure modes; refactor-to-expose-a-property; interpret failures | skill + 5 references | property-based-testing/ | PBT library in target | adding a dependency is user's decision (skill says so) |
| TOB-17 | `mutation-testing`: mewt/muton campaigns, surviving-mutant analysis, equivalent mutants | skill | mutation-testing/ | mewt/muton | tool-specific (headings only) |
| TOB-18 | `testing-handbook-skills` (15 skills: address-sanitizer, aflpp, atheris, cargo-fuzz, constant-time-testing, coverage-analysis, fuzzing-dictionary, fuzzing-obstacles, harness-writing, libafl, libfuzzer, ossfuzz, ruzzy, wycheproof, generator) | skills | testing-handbook-skills/ | fuzzers/sanitizers | headings only; native-code focus |
| TOB-19 | `spec-to-code-compliance`: one agent per requirement, divergences refuted before reporting | skill + agent | spec-to-code-compliance/ | none | headings only |
| TOB-20 | `entry-point-analyzer` (`/entry-points`): state-changing externally callable functions grouped by access level (smart-contract-centric: Slither for Solidity) | skill + command | entry-point-analyzer/ | slither (opt) | contract-specific; the concept (enumerate entry points by privilege) generalizes |
| TOB-21 | `constant-time-analysis` (`/ct-check`): compiler-induced timing side channels in crypto code across ~12 languages, python analyzer package | skill + python | constant-time-analysis/ | compilers/disassemblers | niche |
| TOB-22 | `zeroize-audit`: missing/optimized-away zeroization of secrets (asm + CFG); 11 pipeline agents incl. PoC generator/validator/verifier | skill + agents + shell tools | zeroize-audit/ | clang/llvm | niche |
| TOB-23 | `c-review`, `rust-review`: language-specific multi-worker reviews with coverage ledger checked against source parse, SARIF output, dedup/fp judges | skills + agents + python (check_ledger, generate_sarif, render_report) | c-review/, rust-review/ | Workflow tool, toolchains | native-only |
| TOB-24 | `trailmark` (13 skills): code graph, slicing context, graph evolution/diff, finding triage evidence packets, variant neighborhood, crypto protocol diagrams, mermaid-to-proverif, mutation | skills + python | trailmark/ | trailmark engine | headings only |
| TOB-25 | `building-secure-contracts` (11 scanners/advisors: algorand, cairo, cosmos, solana, substrate, ton, token integration, guidelines, maturity, audit-prep, secure-workflow) | skills | building-secure-contracts/ | none | blockchain-only; out of scope |
| TOB-26 | `second-opinion`: independent review from Codex/Antigravity CLI on uncommitted/branch/commit | skill | second-opinion/ | other vendor CLIs | sends code to third parties; opt-in only |
| TOB-27 | `code-improver` (3 skills + fixer agent): review-and-fix loop with pluggable reviewer, cross-round findings ledger, oscillation escalation, scope guard evals | skills + agent + evals | code-improver/ | none | headings only |
| TOB-28 | `review-walkthrough`: interactive HTML walkthrough of a change | skill + renderer | review-walkthrough/ | none | optional polish |
| TOB-29 | `open-sourcing`: pre-release hygiene incl. secrets-in-history, license, CI readiness | skill + shell checks | open-sourcing/ | git | optional |
| TOB-30 | `firebase-apk-scanner`, `burpsuite-project-parser`, `yara-authoring`, `dwarf-expert`, `dimensional-analysis`, `writing-lean-proofs` | skills | respective dirs | APK/Burp/YARA/DWARF tooling | specialist; out of scope |
| TOB-31 | `gh-cli`, `modern-python`, `modern-cpp`, `git-cleanup`, `github-triage`, `goal-prompt`, `devcontainer-setup`, `chrome-mcp-troubleshooting`, `culture-index`, `let-fate-decide` | skills/hooks | respective dirs | gh/uv/etc. | not security; `gh-cli` shows PreToolUse interception hooks |

### 2.3 Evidence handling
- Preserves: fp-check demands file:line for every phase and "re-read the code after concluding" to catch invented mitigations;
  post-patch-validation records raw stdout/stderr per check, fixed environment, argv arrays (no shell strings), pinned inputs, and a
  reached-marker so a crashing harness cannot masquerade as a reproduction; the harness is side-blind so it cannot cheat by knowing
  which revision it is on; patching-bugs validates JSON records with python before and after edits; audit-context-building writes to
  files and cites a line per claim or labels it an open question.
- Obscures: SARIF `level` can live on the rule not the result (their sarif-parsing skill warns); semgrep fingerprint instability across
  runs; model-only severity ("LLMs overrate severity" is stated in fp-check); Stop-hook prompt checks are themselves model judgments.

### 2.4 Tests/evals shipped
- Per-plugin `evals/` scaffolds exist for post-patch-validation (complete-fix, mixed-failures, missed-variant, behavior-regression),
  code-improver (termination, no-relitigation, scope-guard, deep-reviewer), goal-prompt, review-walkthrough, git-cleanup (graders +
  fixture repos), writing-lean-proofs; bats tests for gh-cli and modern-python hook shims; `test_merge_sarif.py` for semgrep;
  c-review/rust-review ship artifact validators. These verify procedural contracts (does the runner reject incomplete plans, does a
  scope guard hold), not detection recall.

---

## 3. OWASP/ASVS (5.0.0)

### 3.1 Identity
- Repo `OWASP/ASVS`, revision `62981c68fd06`, license CC BY-SA 4.0. Version in data: `5.0.0`, 345 requirements, 17 chapters.
- Paths read: `5.0/docs_en/OWASP_..._5.0.0_en.{csv,json}` (fields `chapter_id, chapter_name, section_id, section_name, req_id,
  req_description, L`), `5.0/en/0x03-What-is-the-ASVS.md` (levels), `5.0/en/0x10..0x26-V*.md` chapter sources, `5.0/mappings/`.
- Levels: L1 baseline (everything an app should have; testable more easily), L2 most applications (L1+L2 ~70% of all reqs), L3
  high-value/safety-critical. Every requirement carries `L` = the lowest level at which it applies. Org-tailoring (drop GraphQL,
  WebSocket, etc. if unused) is explicitly encouraged.

### 3.2 Chapter model (use as the "class" dimension of the coverage ledger)

Counts are requirements per chapter, split `L1/L2/L3` meaning "requirements whose own level is 1/2/3".

| chapter | name | reqs (L1/L2/L3) | sections (id name) | applies to |
|---|---|---|---|---|
| V1 | Encoding and Sanitization | 30 (8/19/3) | V1.1 architecture, V1.2 injection prevention, V1.3 sanitization, V1.4 memory/string/unmanaged, V1.5 safe deserialization | all |
| V2 | Validation and Business Logic | 13 (4/7/2) | V2.1 docs, V2.2 input validation, V2.3 business logic, V2.4 anti-automation | all |
| V3 | Web Frontend Security | 31 (8/11/12) | V3.1 docs, V3.2 unintended content interpretation, V3.3 cookie setup, V3.4 browser security headers, V3.5 browser origin separation, V3.6 external resource integrity, V3.7 other | web UI |
| V4 | API and Web Service | 16 (2/8/6) | V4.1 generic web service, V4.2 HTTP message structure, V4.3 GraphQL, V4.4 WebSocket | APIs |
| V5 | File Handling | 13 (4/5/4) | V5.1 docs, V5.2 upload and content, V5.3 storage, V5.4 download | uploads |
| V6 | Authentication | 47 (13/22/12) | V6.1 docs, V6.2 password security, V6.3 general authn, V6.4 factor lifecycle/recovery, V6.5 MFA, V6.6 out-of-band, V6.7 cryptographic authn, V6.8 IdP authn | login |
| V7 | Session Management | 19 (6/12/1) | V7.1 docs, V7.2 fundamentals, V7.3 timeout, V7.4 termination, V7.5 abuse defenses, V7.6 federated re-auth | sessions |
| V8 | Authorization | 13 (4/3/6) | V8.1 docs, V8.2 general design, V8.3 operation level, V8.4 other | all |
| V9 | Self-contained Tokens | 7 (4/3/0) | V9.1 source and integrity, V9.2 content | JWT-like |
| V10 | OAuth and OIDC | 36 (5/24/7) | V10.1 generic, V10.2 client, V10.3 resource server, V10.4 authorization server, V10.5 OIDC client, V10.6 OpenID provider, V10.7 consent | OAuth |
| V11 | Cryptography | 24 (3/11/10) | V11.1 inventory, V11.2 implementation, V11.3 encryption algorithms, V11.4 hashing, V11.5 random values, V11.6 public key, V11.7 in-use data | crypto use |
| V12 | Secure Communication | 12 (3/6/3) | V12.1 TLS, V12.2 external HTTPS, V12.3 service-to-service | all networked |
| V13 | Configuration | 21 (1/12/8) | V13.1 docs, V13.2 backend communication, V13.3 secret management, V13.4 unintended information leakage | deployable |
| V14 | Data Protection | 13 (2/7/4) | V14.1 docs, V14.2 general, V14.3 client-side | PII/secrets |
| V15 | Secure Coding and Architecture | 21 (3/10/8) | V15.1 docs, V15.2 architecture and dependencies, V15.3 defensive coding, V15.4 safe concurrency | all |
| V16 | Security Logging and Error Handling | 17 (0/16/1) | V16.1 docs, V16.2 general logging, V16.3 security events, V16.4 log protection, V16.5 error handling | all |
| V17 | WebRTC | 12 (0/7/5) | V17.1 TURN, V17.2 media, V17.3 signaling | WebRTC only |

Representative L1 requirement IDs (topics paraphrased; look up text in the ASVS file, do not copy):
- V1: `V1.2.1` context-correct output encoding (HTML/XML), `V1.2.4` parameterized queries, `V1.2.5` OS command injection avoidance, `V1.3.2` no `eval`/dynamic code, `V1.5.1` restrictive XML parser (no external entities).
- V2: `V2.2.1` positive input validation, `V2.2.2` validation enforced server-side, `V2.3.1` business flows in expected step order.
- V3: `V3.2.2` text rendered as text, `V3.3.1` Secure cookie attribute/prefixes, `V3.4.1` HSTS, `V3.4.2` CORS origin fixed or allowlisted, `V3.5.3` state-changing actions use non-safe HTTP methods.
- V4: `V4.1.1` Content-Type matches body, `V4.4.1` WSS only.
- V5: `V5.2.1` size limits, `V5.2.2` extension/type check, `V5.3.1` uploads not executable, `V5.3.2` server-generated storage paths.
- V6: `V6.2.1` min password length, `V6.2.3` change requires current password, `V6.2.4` breached-password check, `V6.3.1` credential-stuffing/brute-force controls, `V6.3.2` no default accounts, `V6.4.1` random initial/activation secrets, `V6.4.2` no knowledge-based questions.
- V7: `V7.2.1` token verification on trusted backend, `V7.2.3` CSPRNG session ids, `V7.2.4` new token on (re)authentication, `V7.4.1` logout/expiry really invalidates, `V7.4.2` disabled accounts lose sessions.
- V8: `V8.2.1` function-level access, `V8.2.2` data-level access (IDOR/BOLA), `V8.3.1` enforced at trusted layer.
- V9: `V9.1.1` signature/MAC verified, `V9.1.2` algorithm allowlist, `V9.1.3` trusted key sources, `V9.2.1` expiry honored.
- V10: `V10.4.1` exact redirect-URI match, `V10.4.2` single-use code, `V10.4.3` short-lived code, `V10.4.4` minimal grants, `V10.4.5` refresh-token replay defense.
- V11: `V11.3.1` no ECB/weak padding, `V11.3.2` approved ciphers/modes, `V11.4.1` approved hashes.
- V12: `V12.1.1` modern TLS only, `V12.2.1` TLS for all external connectivity, `V12.2.2` publicly trusted certs.
- V13: `V13.4.1` no VCS metadata deployed (`.git`).
- V14: `V14.2.1` no sensitive data in URLs, `V14.3.1` client data cleared on session end.
- V15: `V15.1.1` documented remediation timeframes for vulnerable components, `V15.2.1` no components past that window, `V15.3.1` return only required fields.
- V16/V17: no L1 items; V16 starts at L2 (e.g. section V16.3 security events, V16.5 error handling).

### 3.3 Capability inventory

| id | capability | mechanism | source | external dep | failure modes |
|---|---|---|---|---|---|
| ASVS-01 | Stable requirement IDs with level tags as a coverage vocabulary | CSV/JSON | 5.0/docs_en/*.csv,json | none (offline file) | 345 items is too large to load; chapter+section granularity is the practical unit |
| ASVS-02 | Documentation-type requirements (V1.1, V2.1, V3.1, V5.1, V6.1, V7.1, V8.1, V13.1, V14.1, V15.1, V16.1) that ask for written decisions | text | chapters | none | an agent cannot verify "documented"; mark `needs_owner` |
| ASVS-03 | Level selection guidance (L1 start, L2 default, L3 high value) | text | 0x03-What-is-the-ASVS.md | none | choice is a user decision |
| ASVS-04 | Mapping to 4.0.3 and to CWE/NIST | yaml/json | 5.0/mappings | none | not needed for v1 |

### 3.4 Evidence handling
ASVS is a verification standard, not a scanner: evidence is whatever the reviewer cites per requirement. Level and ID are the only
exact identifiers; the requirement text must be looked up, never paraphrased from memory.

### 3.5 Tests/evals
None for agents. Repo has doc build tooling and translation validation only.

---

## 4. OWASP/wstg

### 4.1 Identity
- Repo `OWASP/wstg`, revision `e493506b9cde`, license CC BY-SA 4.0.
- Paths read: `document/4-Web_Application_Security_Testing/*/*.md` (all category directories), `checklists/checklist.json`,
  one full test page (`12-API_Testing/02-API_Broken_Object_Level_Authorization.md`).
- Test pages share a skeleton (ID table, Summary, Test Objectives, How to Test, Remediation, References) and the checklist JSON
  carries per-test `objectives` and a reference URL: machine-usable.
- **Naming correction:** in this revision the input-validation category is `WSTG-INJT-*` (directory `07-Injection`), not `INPV`
  (the v4.2 name; the old name survives only in site navigation scripts). Newer additions exist: `WSTG-APIT-*`, `WSTG-WASM-01`.

### 4.2 Test categories and key IDs (titles are factual labels)

| category | id range | key tests |
|---|---|---|
| Information Gathering `INFO` | 01-10 | 01 search-engine leakage, 02 web server fingerprint, 03 metafiles (robots/sitemap), 04 attack-surface identification, 05 page content leakage, 06 entry points, 07 execution paths, 08 framework fingerprint, 09 app fingerprint, 10 architecture map |
| Configuration `CONF` | 01-15 | 01 network infra, 02 platform config, 03 file extension handling, 04 old/backup/unreferenced files, 05 admin interfaces, 06 HTTP methods, 07 HSTS, 08 RIA cross-domain policy, 09 file permissions, 10 subdomain takeover, 11 cloud storage, 12 CSP, 13 path confusion, 14 other security headers, 15 feature-flag bypass |
| Identity `IDNT` | 01-05 | 01 role definitions, 02 registration, 03 provisioning, 04 account enumeration, 05 username policy |
| Authentication `ATHN` | 01-11 | 01 credentials over encrypted channel, 02 default credentials, 03 lockout, 04 bypass of authn schema, 05 remember-password, 06 browser cache, 07 weak methods/password policy, 08 security questions, 09 weak change/reset, 10 weaker alternative channel, 11 MFA |
| Authorization `ATHZ` | 01-05 | 01 directory traversal/file include, 02 bypass authz schema, 03 privilege escalation, 04 IDOR, 05 OAuth weaknesses (05.1 AS, 05.2 client sub-pages) |
| Session `SESS` | 01-11 | 01 session schema, 02 cookie attributes, 03 fixation, 04 exposed session variables, 05 CSRF, 06 logout, 07 timeout, 08 puzzling, 09 hijacking, 10 JWT, 11 concurrent sessions |
| Injection (input validation) `INJT` | 01-23 | 01 reflected XSS, 02 stored XSS, 03 verb tampering, 04 parameter pollution, 05 SQLi (+ NoSQL, ORM subpages), 06 LDAP, 07 XML, 08 SSI, 09 XPath, 10 IMAP/SMTP, 11 code injection/file inclusion, 12 command injection, 13 buffer overflow/format string, 14 incubated vulns, 15 response splitting, 16 request smuggling, 17 host header, 18 SSTI, 19 SSRF, 20 mass assignment, 21 CSV injection, 22 prototype pollution, 23 insecure deserialization |
| Error Handling `ERRH` | 01-02 | 01 improper error handling, 02 stack traces |
| Cryptography `CRYP` | 01-04 | 01 weak TLS, 02 padding oracle, 03 sensitive data over unencrypted channels, 04 weak primitives |
| Business Logic `BUSL` | 01-10 | 01 data validation, 02 forge requests, 03 integrity checks, 04 process timing, 05 function-use limits, 06 workflow circumvention, 07 misuse defenses, 08 unexpected file types, 09 malicious files, 10 payment |
| Client-side `CLNT` | 01-15 | 01 DOM XSS, 02 JS execution, 03 HTML injection, 04 client-side redirect, 05 CSS injection, 06 resource manipulation, 07 CORS, 08 flashing (legacy), 09 clickjacking, 10 WebSockets, 11 web messaging, 12 browser storage, 13 script inclusion, 14 reverse tabnabbing, 15 client-side template injection |
| API Testing `APIT` | 01-04, 99 | 01 recon, 02 BOLA, 03 excessive data exposure, 04 BFLA, 99 GraphQL |
| WebAssembly `WASM` | 01 | reconnaissance |

### 4.3 Capability inventory

| id | capability | mechanism | source | external dep | failure modes |
|---|---|---|---|---|---|
| WSTG-01 | Black-box-style test catalogue with stable IDs and objectives (usable as a "did we consider this class" checklist) | markdown + `checklist.json` | document/4-*, checklists/ | none | most "How to Test" steps assume live probing; Ultimatum maps them to source-level questions or marks `needs_validation` |
| WSTG-02 | Reporting guidance and appendix (testing tools, fuzz vectors) | markdown | 5-Reporting, 6-Appendix | none | not needed |

Evidence handling: tests are procedural; no evidence format. Tests/evals: none (site build only).

---

## 5. semgrep/semgrep

### 5.1 Identity
- Repo `semgrep/semgrep`, revision `692bfae4ca1b`, license LGPL-2.1. Paths read: `cli/src/semgrep/{constants.py, error.py,
  commands/scan.py, config_resolver.py, output.py, metrics.py}`, `interfaces/semgrep_interfaces/semgrep_output_v1.atd`,
  `cli/README.md`.
- OCaml engine + Python CLI. We treat it as an external binary only.

### 5.2 Capability inventory

| id | capability | mechanism | source | external dep | failure modes |
|---|---|---|---|---|---|
| SG-01 | `semgrep scan --config <file|dir|registry id> [paths]` runs YAML pattern/taint rules | engine | commands/scan.py | engine binary | `--config auto` and `p/...` registry packs need network and send metrics; local rule files work offline (`config_resolver` has a local-path loader) |
| SG-02 | Machine output: `--json`, `--sarif`, `--junit-xml`, `--gitlab-sast`, `--text`, `--emacs`, `--vim`; `--json-output FILE` / `--sarif-output FILE` write beside normal stdout | CLI | scan.py | none | text mode truncates (`--max-lines-per-finding`) |
| SG-03 | Diff-aware scan: `--baseline-commit <rev>` reports only findings not present at the baseline (git required) | CLI + git | scan.py, run_scan.py | git | baseline scan failure suppresses sets; shallow clones lack the commit |
| SG-04 | Telemetry control: `--metrics off|auto|on` (env `SEMGREP_SEND_METRICS`); AUTO sends metrics when config is pulled from the server | CLI | metrics.py | none | forgetting `--metrics=off` leaks usage |
| SG-05 | Targeting: `--include/--exclude`, `--exclude-rule`, `--max-target-bytes`, `--no-git-ignore`, `.semgrepignore`, `--severity INFO|WARNING|ERROR`, `--timeout`, `--jobs`, `--oss-only`, `--dataflow-traces`, `--x-ls` | CLI | scan.py | none | defaults skip big files |
| SG-06 | Exit-code control: findings give exit 0 unless `--error` is passed (then 1); other codes below | CLI | output.py, constants.py | none | agents that treat 0 as "clean" miss that errors[] may be non-empty |
| SG-07 | Rule authoring helpers: `--validate`, `--test` (annotated test files), `--pattern/--lang` ad-hoc | CLI | scan.py | none | none |
| SG-08 | Pro features (`--pro`, interfile taint, secrets validation, supply chain) | login-gated | scan.py | account | out of scope |

**Exit codes** (`cli/src/semgrep/constants.py`, `error.py`): 0 ok; 1 findings (only with `--error`); 2 fatal; 3 target parse failure;
4 rule parse failure; 5 unparseable YAML; 7 missing config; 8 invalid language; 13 invalid API key. (6, 9-12, 14 are commented out
= retired.) Treat any code other than 0/1 as "scan did not run to completion".

**JSON output shape** (from `semgrep_output_v1.atd`): top-level `version`, `results[]`, `errors[]`, `paths{scanned[],skipped[]}`,
optional `time`, `rules_by_engine`, `engine_requested`. Each result: `check_id`, `path`, `start{line,col,offset}`,
`end{...}`, `extra{message, metadata{...from rule}, severity: ERROR|WARNING|INFO, lines, fingerprint, fix?, is_ignored?, metavars?,
validation_state?, sca_info?}`. Each error: `code`, `level`, `type` (e.g. "Syntax error", "Rule parse error", "Timeout",
"Out of memory", "Missing plugin"), `rule_id?`, `message`, `path?`, `spans?`. Caveat noted in the schema: `metavars`, `fingerprint`
and `lines` require being logged in on recent versions, so an offline run cannot rely on them; read the source line ourselves.

### 5.3 Evidence handling
Exact: `check_id`, `path`, `start/end`, exit code, `errors[]`, `paths.skipped` (shows what was NOT scanned). Obscuring: text output,
`--quiet`, a zero exit with non-empty `errors[]` or large `skipped` (a partial scan reported as complete).
### 5.4 Tests
Repo ships large rule/engine test suites (`tests/`, `cli/tests`); irrelevant to us beyond `--test` for our own rules.

---

## 6. google/osv-scanner

### 6.1 Identity
- Repo `google/osv-scanner`, revision `02f96a40691c`, Apache-2.0. Paths read: `docs/{usage.md, scan-source.md, output.md,
  offline-mode.md, supported_languages_and_lockfiles.md}`, `internal/reporter/format.go`, `cmd/osv-scanner/main.go`, `llms.txt`.

### 6.2 Capability inventory

| id | capability | mechanism | source | external dep | failure modes |
|---|---|---|---|---|---|
| OSV-01 | `osv-scanner scan source -r <dir>` (source scanning is the default subcommand): finds lockfiles, SBOMs, git dirs; matches packages to OSV | binary | docs/scan-source.md | OSV.dev API unless offline | no packages found is its own exit code |
| OSV-02 | `-L/--lockfile <path>`, `--no-ignore` (default honors .gitignore), `--x-exclude` (dirs only, experimental), `--config osv-scanner.toml` with `PackageOverrides` (ignore with reason) | flags | usage.md, scan-source.md | none | `.gitignore` boundary parsing known issue |
| OSV-03 | Formats via `--format`: table (default), html, vertical, json, markdown, sarif, gh-annotations, cyclonedx-1-4..1-7, spdx-2-3; `--output-file`; `--all-packages` to list unaffected packages in json/SBOM | flags | reporter/format.go, output.md | none | table default is lossy for agents |
| OSV-04 | Offline: `--offline` (never touches network), `--offline-vulnerabilities`, `--download-offline-databases`; DB at `$OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY/osv-scalibr/<ecosystem>/all.zip` (also falls back to user cache dir then temp dir); zips obtainable from the public `osv-vulnerabilities` bucket; commit-level scanning not supported offline | flags + env | offline-mode.md | pre-downloaded DB (hosted data) | missing DB -> error; stale DB -> silent false negatives |
| OSV-05 | Supported lockfiles (source scan): `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lock`, `requirements.txt` (limited), `Pipfile.lock`, `poetry.lock`, `pdm.lock`, `uv.lock`, `pylock.toml`, `go.mod`, `Cargo.lock`, `Gemfile.lock`, `composer.lock`, `pom.xml`, `gradle.lockfile`, `packages.lock.json`, `deps.json`, `pubspec.lock`, `mix.lock`, `conan.lock`, `renv.lock`, `cabal.project.freeze`, `stack.yaml.lock` | extractors | supported_languages_and_lockfiles.md | none | transitive resolution for some formats (pom, requirements) may use network unless `--no-resolve`/`--offline` |
| OSV-06 | `scan image` (containers), `fix` (guided remediation; docs warn it can run the package manager and follow registries, so unsafe on untrusted projects), `--call-analysis=<lang>` reachability (Go, Rust), `--licenses` | subcommands | usage.md | docker/package manager | `fix` executes scripts; do not use |

**Exit codes** (docs/output.md): 0 packages found, no vulnerabilities; 1 vulnerabilities/findings; 1-126 reserved for result-related
codes; 127 general error; **128 no packages found** (scan picked nothing; not a clean result); 129-255 reserved for non-result errors.

**JSON shape** (`--format json`, stdout; logs go to stderr so redirecting stdout is safe): `{results:[{source:{path,type:
lockfile|sbom|git|docker}, packages:[{package:{name,version,ecosystem}, vulnerabilities:[full OSV records: id, aliases, ...],
groups:[{ids:[...], experimentalAnalysis?}]}]}]}`. Groups merge advisories that alias each other, so count groups, not records, when
reporting "N distinct vulnerabilities". Fixed version appears in table output; in JSON read the OSV `affected[].ranges[].events`.

### 6.3 Evidence handling
Exact: package name/version/ecosystem, source path, advisory IDs and aliases, exit code. Obscuring: exit 128 mistaken for success,
stale offline DB, table format, ignored paths (`.gitignore`, `PackageOverrides`) not echoed.
### 6.4 Tests
Go unit tests + snapshot tests under `cmd/osv-scanner/__snapshots__`; no relevance beyond confirming the CLI output contract is
snapshot-pinned.

---

## 7. gitleaks/gitleaks

### 7.1 Identity
- Repo `gitleaks/gitleaks`, revision `5f6ec56cfa6f`, MIT. Paths read: `README.md`, `cmd/{root,directory,git,detect}.go`,
  `report/finding.go`, `detect/detect.go`, `config/gitleaks.toml` (222 rules), `cmd/generate/config/rules/*.go` (~130 provider rule
  generators), `testdata/` dir names.

### 7.2 Capability inventory

| id | capability | mechanism | source | external dep | failure modes |
|---|---|---|---|---|---|
| GL-01 | `gitleaks dir [path]` (aliases `files`, `directory`) scans files without git; `--follow-symlinks`; `gitleaks git [repo]` scans history via `git log -p` (`--log-opts`, `--staged`, `--pre-commit`); `gitleaks stdin`; `detect`/`protect` deprecated since v8.19 | binary | README.md, cmd/ | git for `git` | history scans of big repos are slow; `dir` ignores history |
| GL-02 | Report: `--report-format json|csv|junit|sarif|template`, `--report-path FILE` (`-` = stdout), `--report-template` | flags | root.go | none | |
| GL-03 | **`--redact[=N]`** masks secret in logs, stdout and report (default 100%) | flag | README.md, finding.go | none | without it `Secret` and `Match` contain the raw secret in the JSON |
| GL-04 | Config: `--config` (precedence: flag, `GITLEAKS_CONFIG`, `GITLEAKS_CONFIG_TOML`, `<target>/.gitleaks.toml`, default), rule `[[rules]]` with `regex`, `keywords` prefilter, `entropy`, `secretGroup`, per-rule allowlists, global allowlist (paths, regexes, stopwords) | toml | config/ | none | custom config replaces defaults unless `[extend]` |
| GL-05 | Suppression: inline `gitleaks:allow` comment (`--ignore-gitleaks-allow` disables), `.gitleaksignore` of fingerprints, `--baseline-path` previous report | files/flags | detect.go | none | suppression is itself a risk: review additions |
| GL-06 | Decoding / archives: `--max-decode-depth` (README default 0, flag code default 5: verify on the installed version), `--max-archive-depth` (default 0) | flags | README.md, root.go | none | base64-wrapped secrets missed at depth 0 |
| GL-07 | Exit codes: 0 clean; 1 leaks or error (change with `--exit-code`); 126 unknown flag | CLI | README.md | none | exit 1 conflates "leaks" and "failure": always check stderr, or set `--exit-code 3` for leaks so 1 means failure |

**Finding shape** (JSON array; `Line` is excluded from JSON): `RuleID, Description, StartLine, EndLine, StartColumn, EndColumn,
Match, Secret, File, SymlinkFile, Commit, Link?, Entropy, Author, Email, Date, Message, Tags[], Fingerprint`. Fingerprint =
`file:ruleid:startline` for dir scans, `commit:file:ruleid:startline` for git scans (`detect.go` lines 712-716).

**Rule classes (222 default rules)**: cloud provider keys (AWS, GCP, Azure, Alibaba, DigitalOcean, Cloudflare, Fly.io, Heroku...);
source-control and CI tokens (GitHub, GitLab, Bitbucket, Travis, Drone, CircleCI-type, Harness, Octopus); package registries (npm,
PyPI, RubyGems, NuGet, Clojars, JFrog/Artifactory); payments (Stripe, Square, Shopify, GoCardless, Plaid, Flutterwave); comms (Slack,
Discord, Telegram, Twilio, SendGrid, Mailgun, Mailchimp); AI providers (OpenAI, Anthropic, Hugging Face, Cohere, Perplexity);
observability (Datadog, New Relic, Sentry, Grafana, Sumo, Dynatrace); SaaS (Atlassian, Notion, Linear, Postman, HubSpot, Okta,
Snyk, Sonar...); generic structural rules (`generic-api-key` keyword-assignment with entropy 3.5, `jwt`, `private-key` PEM blocks,
`curl-auth-header`, `curl-auth-user`, `nuget-config-password`, `age-secret-key`, `slack-webhook-url`).

**High-signal provider prefixes observed in the rule set** (facts we may use to design our own original patterns):
`AKIA`/`ASIA`/`ABIA`/`ACCA`/`A3T` + 16 base32 chars (AWS; rule skips values ending `EXAMPLE`); `ghp_` (36), `gho_`, `ghu_`/`ghs_`
app tokens, `github_pat_` (82); `glpat-`; `sk_live_`/`sk_test_`/`rk_live_` (Stripe); `xoxb-`, `xoxp-`, `xoxe-`, `xapp-`,
`hooks.slack.com/services/`; `-----BEGIN ... PRIVATE KEY-----`; `AIza` + 35 (Google API key); `sk-ant-api03-` (Anthropic);
`sk-proj-`/`sk-svcacct-` with a fixed `T3BlbkFJ` marker (OpenAI); `hf_` (Hugging Face); `npm_` + 36; `pypi-AgEIcHlwaS5vcmc`;
`SG.` (SendGrid); `dop_v1_` (DigitalOcean); `dapi` + 32 hex (Databricks); `shpat_`; `SK` + 32 hex (Twilio, ambiguous); `PMAK-`
(Postman); `lin_api_`; `AGE-SECRET-KEY-1`; `HRKU-AA`; JWT `ey....ey....`. Global allowlist skips lockfiles, `node_modules`,
vendor dirs, images/fonts/binaries, minified well-known libs. Stopwords and entropy gates are the false-positive controls.

### 7.3 Evidence handling
Exact: File, StartLine/EndLine, RuleID, Fingerprint, Commit (git mode). Dangerous: `Secret`/`Match` and `Line` expose live
credentials; reports written to disk or pasted into a model context leak them. Always `--redact`, and prefer stdout piping to a
file outside the repo.
### 7.4 Tests
Table-driven true-positive/false-positive samples per rule (`GenerateSampleSecrets`, `tps`/`fps` lists), `detect_test.go`,
report tests per format, `testdata/{baseline,config,gitleaksignore,repos,expected}`. Good model for our own rule fixtures: each
rule ships positive and negative samples.

---

## 8. Overlaps and merge recommendation

| job | competing sources | merge into ONE Ultimatum behavior |
|---|---|---|
| Finding verification / false-positive rejection | CF-14/15/17, TOB-01 (fp-check gates), TOB-12 (brocards), CF-20 (anti-patterns) | One **verify** step: fresh context, restate claim, trace source->sink incl. strongest preventing control, check attacker control + threat model (brocards 1-3), then challenge questions (section 10.5). Verdict in {confirmed, needs_validation, rejected}. Use fp-check's "re-read the code after concluding" and brocard "attacker power vs impact" explicitly. |
| Coverage / "did we look everywhere" | CF-05/09/11 ledger, TOB-23 (c-review ledger checked against parse), ASVS chapters, WSTG categories | One **coverage ledger** whose class dimension is ASVS chapter + Cloudflare-style attack class; ASVS/WSTG IDs are tags, not the checklist. Ledger file validated by a stdlib python checker. |
| Change review | TOB-02 differential-review, CF `quick`/scoped diff runs, TOB-15 regression-hunt | **change-review**: triage by risk class not size, mandatory look at removed checks (git history), caller/blast radius, sibling paths (CF "compare siblings for equivalence"), test coverage of changed lines. Output is findings JSON, not a mandatory markdown file. |
| Variant search | TOB-04, CF hunting "variant" step, TOB-14 variant check | Variant step inside verify/remediate: build exact-match pattern first (a pattern matching nothing means misunderstood bug), generalize one element at a time, stop at >50% noise; record failed patterns. |
| Fix proof | TOB-13/14, TOB-16 | **prove-fix**: regression test fails on baseline and passes after; separate variant test; unaffected-behavior check; existing suite; marker proving the exploit test actually reached its assertion. |
| Static tool use | TOB-05, SG-*, GL-*, OSV-* | **tool adapters** with detect -> run -> parse -> normalize to leads. Tools generate leads; only the verifier makes findings. |
| Agent/LLM risk | CF-21, TOB-10 | One **ai-agent-risks** reference (section 10.9). |
| Secrets | GL-*, CF "Obvious things", TOB-07, TOB-29 | `ult-scan` original regex set + gitleaks adapter, always redacted. |
| Severity | CF-19 anchors, TOB-11 CVSS | Our rubric (10.4): impact-first, capped by demonstrated result, preconditions adjust likelihood. CVSS is an optional label, never the source of truth. |
| Test depth | TOB-16 PBT, TOB-17 mutation, TOB-18 fuzz, TOB-14 | One **test-depth ladder** (10.8) chosen by risk and by what the repo already has. |

Selection principle: take Cloudflare for process discipline (verdict semantics, ledger, independence), Trail of Bits for verification
rigor and proof-of-fix mechanics, ASVS/WSTG as vocabularies, the three CLIs as optional lead generators.

---

## 9. Delivery in Ultimatum

| id | delivery | note |
|---|---|---|
| CF-01 | native | `security` router decides overlay / review / audit by request; ambiguous -> one question |
| CF-02 | native (adapted) | Ultimatum cannot enforce an OS sandbox. Rule: never run target-controlled code unless the user's existing test command is explicitly allowed; otherwise `needs_validation` with that blocker |
| CF-03 | native (reduced) | run dir with parent-only shared files and per-agent scratch; drop the 11-step descriptor promotion (hostile-repo threat) but keep "agents never write shared files" |
| CF-04 | native | recon reference + `ult-scan --inventory` (entry points, config, deps) |
| CF-05 | native | `ledger.json` + `ult-ledger-check.py` (stdlib) |
| CF-06 | native | `quick`/`standard`/`deep` + scoped; partial-coverage banner mandatory |
| CF-07 | shared (general budget behavior) | express as agent-count budget in the audit workflow |
| CF-08 | native | re-run reads prior ledger/findings; stable fingerprints |
| CF-09, CF-10, CF-11 | native | `hunter` and `coverage-critic` plugin agents; core method rewritten |
| CF-12, CF-13 | native | `references/security/attack-classes.md` with domain sections; only load sections the recon selects |
| CF-14, CF-15, CF-17 | native | `verifier` agent, three verdicts, final-record check |
| CF-16 | native | findings schema 10.2 + `ult-findings-check.py` |
| CF-18 | native | report templates; derived from JSON only |
| CF-19 | native | rubric 10.4 |
| CF-20 | shared | anti-patterns become part of the general "evidence before claims" behavior |
| CF-21 | native | `references/security/ai-agent-risks.md` |
| CF-22 | native | python ports of both validators (no node) |
| TOB-01 | native | verifier gates + challenge questions (10.5), FP patterns (10.6) |
| TOB-02 | native | change-review workflow (10.3) |
| TOB-03 | shared | comprehension step = general codebase-orientation behavior; security adds assumptions/guarantees notes |
| TOB-04 | native | variant step |
| TOB-05 | optional-integration | semgrep (detect `semgrep --version`; fallback `ult-scan`); codeql: gap (heavy build, not credible offline) ; SARIF parsing: native small parser (read `runs[].results[]`, resolve level from rule) |
| TOB-06 | gap | rule authoring is a specialist task; point to upstream plugin if installed |
| TOB-07 | native | insecure-defaults category list reused conceptually in `ult-scan` config rules + verifier question "does the app run with the default?" |
| TOB-08 | native (short) | sharp-edges checklist inside secure-implementation overlay |
| TOB-09 | optional-integration | osv-scanner; fallback = inventory only, honest "advisories unknown" |
| TOB-10 | native | CI-workflow section of `ult-scan` + ai-agent-risks reference |
| TOB-11 | gap (optional label) | not needed; severity rubric is ours |
| TOB-12 | shared | folded into verifier (threat model, attacker-power, usage reachability, documented-behavior checks) |
| TOB-13, TOB-14 | native | `prove-fix` procedure + small python helper that runs a test command on base and patched worktrees and checks a marker |
| TOB-15 | shared | change-review plus git bisect-style guidance; no dedicated campaign |
| TOB-16 | native | test-depth reference (property catalog, tautology/vacuity checks), uses repo's PBT library if present |
| TOB-17 | optional-integration | detect mutmut / cargo-mutants / Stryker / PIT / go-mutesting; fallback: manual "mutate-by-hand" on changed security conditions (flip a comparison, delete a check) and see the test fail |
| TOB-18 | gap | fuzz/sanitizer harness work is native-code specialist; mention as escalation |
| TOB-19 | shared | requirement-by-requirement check is the ASVS coverage pass |
| TOB-20 | native | `ult-scan --inventory` lists HTTP routes/handlers/CLI commands/webhook handlers per framework heuristics, plus a "who can call this" column filled by the agent |
| TOB-21..25 | gap | specialist (crypto timing, zeroization, C/Rust, code graph, blockchain) out of scope for v1 |
| TOB-26 | gap | sends code to third parties; never default |
| TOB-27 | shared | review-fix loop = general behavior |
| TOB-28..31 | gap / out of scope | |
| ASVS-01..04 | native | `references/security/asvs-map.md`: chapter ids/names, applicability triggers, 3-5 anchor IDs per chapter, level policy; full text read from upstream file only if the user installs it (optional-integration) |
| WSTG-01 | native (map) | `references/security/wstg-map.md`: category -> source-level question; live-probe steps excluded |
| SG-01..07 | optional-integration | semgrep; detection `command -v semgrep`; local rule dir only when offline; always `--metrics=off --disable-version-check`; fallback `ult-scan` |
| OSV-01..05 | optional-integration | osv-scanner; detection `command -v osv-scanner` + offline DB dir check; fallback inventory-only |
| OSV-06 | gap by design | `fix`/image scans not run |
| GL-01..07 | optional-integration | gitleaks; detection `command -v gitleaks`; fallback `ult-scan --secrets` original regex set |

---

## 10. Concrete guidance worth encoding

### 10.1 Behavior contract (all three workflows)
1. Findings are claims about a crossed trust boundary with a concrete affected principal/resource and an observable or owner-observable
   result. A scanner hit, a missing header, or a scary-looking API is a **lead**.
2. Three verdicts only: `confirmed`, `needs_validation`, `rejected`. `needs_validation` carries the exact unresolved fact and has no
   severity. Never park speculation there.
3. The agent that proposes a finding never signs off on it. Verification happens in fresh context that receives the claim and the
   code, not the proposer's reasoning.
4. Do not execute target code or touch live systems. Run only the project's own test command, only with user consent for anything
   beyond read-only, never with network credentials. If a decisive fact lives in deployment (proxy, IdP policy, cloud IAM), emit
   `needs_validation` with the owner-observable check.
5. Secrets are never echoed. Show `AKIA****MPLE` style (prefix 4 + suffix 2-4, length); store hash of the match for dedupe.
6. Partial coverage must be stated on the first line of any report (scoped, quick, budget-limited, no prior ledger).
7. Clean result wording: "no confirmed findings within <scope>; coverage <n/m> units; not evidence of absence."

### 10.2 Recommended findings JSON schema (`findings.json`, array, sorted by `fingerprint`)

Common fields (all verdicts):
```
verdict            "confirmed" | "needs_validation" | "rejected"
fingerprint        stable id of the root cause; regex ^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$ ; no line numbers, agent, severity, verdict
title              <=100 chars
summary            2-4 sentences, plain
boundary           { attacker: "who", capability: "what they start with", crosses: "which control", asset: "affected principal/resource" }
trace[]            { kind: entrypoint|propagation|sink, file, line, scope, note }  # first=entrypoint, last=sink; repo-relative
evidence[]         { file, line, note }  # includes the strongest preventing control that was checked
refs               { asvs: ["V8.2.2"], wstg: ["WSTG-ATHZ-04"], cwe: ["CWE-639"] }   # optional tags, never prose copies
found_by           "hunter:<id>" | "tool:semgrep:<rule>" | "review"
verified_by        agent id (must differ from found_by agent); verification_notes
```
`confirmed` adds:
```
root_cause, intended_behavior
preconditions[]    { kind: authn_level|authz_role|user_interaction|system_config|network_position|data_state|timing|third_party, note }
reproduction       { interface: http|cli|library|file|message|local-test, steps[], inputs[], observed_result, run: {command, exit_code, output_excerpt_redacted} }
severity           { likelihood: {score, reason}, impact: {score, reason}, overall }   # overall <= impact ; scores: info|low|medium|high|critical
confidence         { score: low|medium|high, reason }
remediation        { strategy, invariant, change_sketch[] {file, note}, regression_test: {file?, idea} }
fix_proof?         { status: not_attempted|verified|failed, base_result, patched_result, variant_checked: bool, suite_result }
```
`needs_validation` adds: `claimed_root_cause`, `blockers[]` (>=1, each a specific missing fact), `validation_plan { local?, owner_observed? }` (>=1).
`rejected` adds: `claimed_root_cause`, `reason` (which control/fact refutes), `rejected_by_pattern?` (id from 10.6).
Validator rules (port from Cloudflare): required fields per verdict, no unknown keys, unique fingerprints, sorted, repo-relative safe
paths (no abs, `..`, control chars), line >= 1, entrypoint/sink ordering, `overall <= impact`, no severity on needs_validation,
`verified_by != found_by`, no field containing a secret-looking token (run the redactor over the whole file; fail if it matches).

### 10.3 Ledger schema (`coverage-ledger.json`, array of units)
```
coverage_id   percent-encoded refs joined by "::" -> surface::boundary::subsystem::class   (class is an Ultimatum attack-class id)
refs          { surface: "src/api/orders.py#POST /orders/{id}", boundary: "src/authz.py#require_owner", subsystem: "api", class: "access-control" }
standards     ["ASVS:V8", "WSTG-ATHZ"]       # tags only
paths[]       starting paths
status        planned|in_progress|covered|candidate|blocked|deferred|out_of_scope|not_applicable
owner         null unless in_progress/blocked/covered/candidate
checks[]      { agent, paths[], invariant, method: source|test|tool, result, artifact|null }
fingerprints[] only for candidate
unresolved[]  reason(s) for deferred/out_of_scope/not_applicable/blocked
wave, prior_status (new|prior_confirmed_same_source|prior_confirmed_changed_source|prior_needs_validation|prior_deferred|prior_covered_same_source|prior_covered_changed_source|none)
attempts[]    archived earlier evidence when a critic reopens a unit
```
State invariants (adapted): `planned` -> no owner, no checks; `deferred|out_of_scope|not_applicable` -> reason required, no owner;
`in_progress` -> owner, no evidence yet; `covered` -> owner + >=1 check with paths; `candidate` -> owner + checks + fingerprints;
`blocked` -> owner + partial checks + blocker. Unit `paths` = union of check paths. Duplicate IDs fail. Sort lexicographically.
ASVS dimension: separate small table `asvs-applicability` of chapter -> `applicable|not_applicable(reason)|needs_owner` so V17/WebRTC,
V10/OAuth, V4.3 GraphQL are dropped with a recorded reason rather than silently.

Ledger-level report block: counts per status, list of deferred/out_of_scope, profile, whether a prior ledger existed, last critic result.

### 10.4 Severity rubric (demonstrated impact + preconditions)
Score **impact** from what was actually shown, **likelihood** from preconditions, then `overall <= impact`.

Impact anchors:
- critical: unauthenticated or low-priv actor gets code execution on a server/dev machine they do not control, takeover of arbitrary
  accounts, or full data-store read/write.
- high: complete bypass of an explicit control with real consequences (authn bypass, cross-tenant read/write, authenticated RCE, stored
  script run in other users' sessions, secret exfiltration from agent context to attacker).
- medium: real boundary violation with narrow blast radius or limited data (single-resource IDOR of low-sensitivity data, reflected
  XSS needing interaction, SSRF limited to non-metadata hosts).
- low: disclosure of non-secret internals, effect needing sustained effort for small gain.
- informational: confirmed but minimal; mainly a prerequisite in a chain.

Likelihood from preconditions: unauthenticated network < any authenticated user < privileged role < local/adjacent < physical; add
user-interaction and non-default configuration as reducers; add "default configuration, internet exposed" as booster. A precondition
that already grants the attacker the impact (attacker must be admin to do admin things) removes the finding (brocard 2).

Hard caps: self-impact (user attacks only themselves) <= info; defense-in-depth gap with a working primary control = hardening note, no
severity; needs_validation = no severity; unproven chain steps cap at the proven part; DoS counts only if shared availability impact
is shown locally with a bounded harness; dependency advisory without reachable use = `needs_validation` or hardening, not a finding.
Always write the sentence "An attacker with <capability> can <action> to <concrete damage>"; if the damage cannot be stated, lower the
score.

### 10.5 Verifier challenge questions (fresh context)
1. Restate the claim in one sentence: attacker, capability, action, victim, damage. Can it be stated without hand-waving?
2. Is the entrypoint reachable by that attacker (route registered, flag on by default, auth middleware actually applied to this path)?
3. What is the strongest control on the path (middleware, framework default, DB constraint, allowlist, ownership filter in the query)?
   Quote it. Does it fire for this input?
4. Does attacker-controlled data actually reach the sink, or is the value server-generated, constant, or from trusted config/storage?
5. After the last check, is the value transformed (decode, normalize, concatenate, deserialize) so the check no longer holds?
6. Do sibling paths (batch, bulk, legacy v1, retry, export, admin) enforce the same rule? If one does and this one does not, say so.
7. Does the attacker already hold the power this "exploit" grants? Is the harm only to themselves?
8. Is the behavior documented, standard for this framework, or required by the product? Is the "fix" worse than the "bug"?
9. What deployment fact would change the answer (proxy strips header, WAF, IdP policy, network policy)? Is it visible in the repo? If
   not and decisive: needs_validation, with the exact owner check.
10. Is there a test or fixture, or a minimal harness, that shows the behavior without touching live systems? Run it if the user's
    environment permits; otherwise say not run.
11. Re-read the cited lines now. Do they say what the finding says (line numbers drift; models invent mitigations and invent flaws)?
12. Are severity, likelihood and impact justified only by what was shown, not by the worst imaginable follow-on?
13. Am I dismissing this because the exploit looks complicated? Complexity lowers likelihood, not existence.
14. Is this the same root cause as an existing fingerprint? Merge, do not duplicate.

### 10.6 False-positive patterns to reject (record as `rejected_by_pattern`)
- FP-01 pattern-only: dangerous function name present but argument is constant or validated upstream.
- FP-02 trusted source mislabeled untrusted: config, build-time values, server-side storage written only by trusted components.
- FP-03 missing header/flag with no sensitive consequence (cookie lacks HttpOnly but holds no secret and JS needs it).
- FP-04 test, example, fixture, docs, vendored or generated code (`tests/`, `examples/`, `node_modules`, `.min.js`) presented as production.
- FP-05 placeholder secrets: `changeme`, `YOUR_API_KEY`, `xxxxxxxx`, `EXAMPLE` suffix, `<token>`, repeated chars, low entropy, env lookups
  with no default.
- FP-06 defense-in-depth gap where another layer verifiably blocks the attack.
- FP-07 self-impact or same-principal authority (user can only read own data via own token).
- FP-08 attacker needs capability equal to the impact (admin-only function that does admin things).
- FP-09 theoretical race/TOCTOU with no demonstrated concurrent access or no security-relevant state between check and use.
- FP-10 integer/bounds "overflow" where an earlier check makes the condition unreachable.
- FP-11 crash/panic/exception on malformed input in a non-shared, self-restarting context presented as DoS.
- FP-12 dependency advisory for a package or code path the project never imports, or already patched by lockfile resolution.
- FP-13 prompt-injection text with no deterministic capability, sink, or cross-principal reach behind it.
- FP-14 documented/intentional behavior (debug flag gated by build, CLI that deliberately runs shell commands for its user).
- FP-15 hardcoded value that is a public identifier, not a secret (client id, public key, publishable key `pk_live_`, DSN public key).
- FP-16 regex hit inside a comment, lockfile hash, base64 image, minified bundle, or JWT example in docs.
- FP-17 "missing rate limit/CSRF/auth" on an endpoint that is public or token-authenticated by design.
- FP-18 guessed deployment behavior (assumes the proxy is absent/present) without evidence.
- FP-19 finding supported by line numbers that do not contain the cited code.
- FP-20 severity inflated to critical by chaining an unproven step.
Also reject by default: scanner output relayed without reading the code.

### 10.7 Workflows

**secure-implementation (overlay, runs while editing)**
Trigger (any of): auth/session/token/password code; authorization checks or new routes/handlers; SQL/ORM raw queries; shell/process
spawn; file path, upload, download, archive extraction; deserialization/YAML/pickle/XML; template rendering; redirects/URL fetching
(SSRF); crypto/randomness/hashing; CORS/cookies/headers; webhooks/callbacks; secrets/config/IaC/Dockerfile/CI workflow; LLM prompt
construction, tool definitions, MCP/hooks/agent permissions; dependency or lockfile edits.
Steps: (1) one-line boundary note: who controls the input, what asset is at stake, where the decision is enforced. (2) choose the safe
primitive in the project's own stack (parameterized query, `subprocess` with argv list, path resolve + containment check, allowlist
over denylist, constant-time compare, CSPRNG, framework escaping) and reuse existing helpers before inventing. (3) enforce authz at the
last trusted layer, per object, not only per route. (4) fail closed; errors generic to clients, detail to logs without secrets.
(5) write at least one negative test (attacker input rejected; other tenant denied) beside the happy path. (6) run `ult-scan` over
changed files; read each lead. (7) state residual assumptions in the final message. Keep the overlay to a short checklist; load deeper
references (ASVS chapter map, sharp-edges) only when the trigger class matches.

**change-review (diff plus path)**
(1) Resolve the diff (`git diff <base>...HEAD`, staged, or PR). (2) Classify each hunk by risk class, not size: auth/crypto/validation
removal/external call/config default/dependency/CI. A "refactor" touching a check is high until proven otherwise. (3) For every removed
or loosened check: `git log -S`/blame to learn why it existed. (4) Trace the changed function's callers and the execution path to
its entrypoints; read siblings that produce the same effect (batch, bulk, v1/v2, export, retry). (5) Check that changed lines have tests
and that a security-relevant test would fail if the check were deleted. (6) Run `ult-scan` on the changed files plus semgrep/gitleaks/osv
if present (diff-aware: semgrep `--baseline-commit`). (7) Hunters limited to the touched units; verifier on every candidate. (8) Output:
findings JSON + short summary, blast radius (caller count), coverage statement (what was and was not read), confidence.
Never promise "no issues"; say what was covered.

**full-audit (explicit request only)**
Phases: 0 setup (scope, profile, budget, output dir outside repo, source ref, dirty-tree note) -> 1 recon (stack/entry points,
principals/authority, entry->copy->sink inventory, test/run visibility; AI-agent surfaces if present) -> 2 trust-boundary map ->
3 coverage ledger seeded from surfaces x boundaries x attack classes (+ASVS applicability table) -> 4 hunter waves on ledger units,
structured JSON results only -> 5 coverage critic (fresh) -> repeat until clean or profile limit -> 6 fresh verifier per candidate ->
7 write findings.json, run checker -> 8 fresh record check for confirmed/needs_validation -> 9 report + findings JSON -> 10 optional
remediation with proof (fix at invariant, regression test failing on baseline, variant search, suite run).
Profiles: `quick` (coarse units, one hunter wave, one critic, one verifier per candidate), `standard`, `deep` (split by lifecycle mode,
critic to clean pass, second pass on prior-covered units). Evidence bar identical across profiles. Budget = max agent invocations;
reserve critics + verifiers before hunters; if the reserve cannot be funded, run nothing and say why.
Unreached units are `deferred` with a reason, never silently dropped. Re-runs read prior ledger and findings.

### 10.8 Test-depth ladder (choose by risk, repo tooling, cost)
0. Existing tests run and baseline recorded (exit code + failing set) before any change.
1. Example tests for the changed behavior, including negative/security cases.
2. Boundary and sad-path set: empty, null, zero, negative, max, over-limit, duplicate, mixed encoding, stale, revoked, concurrent.
3. Property-based tests where code has algebraic shape (roundtrip, inverse, oracle, idempotence, invariant, commutative). Strongest
   property the code supports; no-crash alone rarely justifies the dependency. Reject tautologies (assertion recomputes the
   implementation) and vacuity (filters that discard nearly all inputs or zero cases). Use the repo's PBT library (Hypothesis,
   fast-check, proptest, etc.); adding one is the user's decision.
4. Differential/oracle: new vs reference implementation, patched vs base.
5. Mutation check on security conditions: flip a comparison, drop a guard, swap `and`/`or`; a surviving mutant means the test suite does
   not guard that decision. Use a mutation tool if installed; otherwise hand-mutate 3-5 key lines and confirm a test fails each time.
6. Fuzz/sanitizer for parsers and native code: escalate to the user; do not improvise harnesses for untrusted parsers without a sandbox.
Proof-of-fix contract (each item recorded with command + exit code + raw output tail): control check passes on base and patch; exploit
test fails on base and passes on patch; variant test fails on base and passes on patch; unaffected behavior unchanged; targeted
regression check passes; existing suite passes. The exploit/variant test prints a unique marker line on stdout immediately before its
assertion so an import error, build failure, or timeout cannot be mistaken for a reproduction (a timeout is a gap, not a regression).
Prefer argv arrays over shell strings; run with a minimal fixed environment; keep the test unaware of which revision it runs on.

### 10.9 AI-agent risks reference (what to put in `ai-agent-risks.md`)
Rules: prompt injection is only a finding when a deterministic boundary fails behind it; guardrail prompts are not controls; tool
descriptions, tool results, retrieved documents, memory, MCP metadata, issue/PR text, filenames and web pages are untrusted input.
Checks:
- Four maps: identities, capabilities, writable context/memory sources, output sinks. Connect attacker-writable source -> model context
  -> tool with authority -> sink.
- Overprivileged tools: broad filesystem/shell/network/git credentials; tool handlers that do not re-check requester + resource;
  shared service identity (confused deputy). Least privilege per tool, per task, with path/host allowlists enforced in code.
- Action binding: approval covers exact tool + full normalized arguments + target; retries/resume/batch cannot mutate the approved
  action; no "approve once, run many".
- Exfiltration paths: markdown image/link rendering, URL fetch tools, DNS/HTTP from shell, commit messages, issue comments; egress
  allowlist; secrets never placed in prompts, tool args, logs or transcripts.
- Memory/persistence poisoning: who can write memory, instruction files, skills, hooks, `CLAUDE.md`, MCP configs; treat repo-supplied
  instruction files and hooks as untrusted when the repo is untrusted (a hook is arbitrary code execution); invisible Unicode/tag
  characters in instruction text.
- MCP/sub-agent trust: pin and verify server identity, no tool-name collisions, delegated agents get minimum authority and their
  results are untrusted on return, no credentials inherited by default.
- Tool schema vs handler disagreement (aliases, extra fields, coercion); structured output narrows shape, not authority.
- Unbounded loops/spend: per-request budgets, idempotency, cancellation.
- CI with AI agents (nine vectors seen upstream, restated): attacker text reaching the agent via env-var intermediaries or direct
  `${{ }}` expression expansion; agent fetching attacker-controlled data (PR/issue/log content); `pull_request_target` with checkout of
  head code; error/log text fed back; subshell expansion of untrusted values; executing model output; permissive sandbox/permission
  settings (bypass flags, wide tool allowlists); wildcard user allowlists. Fix: least-privilege tokens, no secrets on untrusted
  triggers, restrict who can invoke, never evaluate model output as code.
- Local tool-config hygiene to flag: `bypassPermissions`/skip-permission flags in settings or CI, `Bash(*)` allow rules, broad
  `enableAllProjectMcpServers`-style auto-trust, hooks that curl|sh, MCP servers launched via unpinned `npx`/`uvx`, secrets inline in
  `.mcp.json`/settings.

### 10.10 What `ult-scan` (stdlib python fallback) should detect, honestly

Output contract: JSON lines or array of **leads**, never "findings": `{rule_id, class, severity_hint (low|med|high, advisory only),
path, line, snippet_redacted, why, confidence (pattern-only|contextual), standards[]}`; exit 0 = scan completed (even with leads),
exit 2 = scan error/incomplete, distinct nonzero when `--fail-on-leads`. Always report `files_scanned`, `files_skipped` (+reason:
binary, size cap, excluded dir), and rule-pack version. Skip by default: `.git`, `node_modules`, `vendor`, `dist`, `build`, lockfiles
for secret scanning, binaries, files > 1 MB; honor `.gitignore` only when asked (secrets live in ignored `.env` files: **do** scan
`.env*` locally but flag only if tracked by git, using `git ls-files` when available).

1. **Secrets (original regex set; redaction mandatory)**
   - Structured prefixes: AWS access key id (`AKIA|ASIA` + 16 base32; ignore `EXAMPLE` suffix), GitHub (`ghp_`, `gho_`, `ghu_`,
     `ghs_`, `ghr_`, `github_pat_`), GitLab `glpat-`, Stripe `sk_live_`/`rk_live_` (flag `sk_test_` as low), Slack `xox[bpae]-`
     and webhook URLs, Google `AIza`, Anthropic `sk-ant-`, OpenAI `sk-proj-`/`sk-svcacct-`, npm `npm_`, PyPI `pypi-AgEI`, SendGrid
     `SG.`, DigitalOcean `dop_v1_`, Hugging Face `hf_`, Twilio `SK` only when keyword nearby.
   - PEM blocks: `-----BEGIN (RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY( BLOCK)?-----` (header alone is enough for a lead).
   - JWT shape `eyJ...\.eyJ...\.` (low unless in non-test code with real-looking claims).
   - Credentials in URLs `scheme://user:pass@host`, `Authorization: Bearer|Basic <long>` literals, `.netrc`, `.npmrc` `_authToken`,
     `docker config.json` `auth`.
   - Keyword assignment (`password|secret|token|api[_-]?key|private[_-]?key` = string literal) gated by: length >= 12, Shannon
     entropy >= ~3.5 bits/char for non-words, not a placeholder (FP-05), not an env lookup, not in test/docs paths unless high-signal.
   - Fallback secrets: `os.environ.get("X", "literal")`, `process.env.X || "literal"`, `getenv("X", "literal")` feeding
     sign/encrypt/session names (insecure default; the literal runs when the var is missing).
   - Redaction: snippet shows first 4 and last 2 chars of the match, `[len=N]`, and `sha256[:8]` for dedupe; the raw value never
     enters stdout, JSON, logs, or the model context. Inline suppression `ult:ignore <rule> reason` is itself reported when it appears in
     a diff.
2. **Risky sinks per language (pattern leads; the verifier decides)**
   - Python: `eval/exec/compile`, `pickle/marshal/shelve.load(s)`, `yaml.load` without SafeLoader, `subprocess(... shell=True)`, `os.system/popen`,
     `input()` py2, string-built SQL passed to `execute`, `tempfile.mktemp`, `verify=False`, `hashlib.md5/sha1` for security, `random` for tokens,
     `Flask(debug=True)`/`DEBUG = True`, `assert` for auth, `xml.etree` on untrusted XML, `tarfile.extractall`/`zipfile.extractall`
     without member checks, `requests` to user-supplied URLs.
   - JS/TS: `eval`, `new Function`, `child_process.exec` with interpolation, `innerHTML/outerHTML/document.write/insertAdjacentHTML`,
     `dangerouslySetInnerHTML`, `vm.runIn*`, template-literal SQL, `Object.assign`/deep-merge on request bodies (prototype pollution),
     `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`, `Math.random` for tokens, `jwt.verify` with `algorithms` missing or
     `none`, `cors({origin: true|'*', credentials: true})`, `res.redirect(req.query...)`, `fs` with request-derived paths.
   - Go: `exec.Command("sh","-c",...)`, `fmt.Sprintf` into `db.Query`, `InsecureSkipVerify: true`, `math/rand` for secrets, `template.HTML`,
     `http.ListenAndServe` without timeouts.
   - Java/Kotlin: `Runtime.exec`, `ObjectInputStream.readObject`, `Statement` + concatenation, `DocumentBuilderFactory` without XXE
     features, `MessageDigest.getInstance("MD5"|"SHA-1")`, `Cipher "AES/ECB"`, `TrustAllCerts`, `@CrossOrigin("*")`.
   - Ruby/PHP: `eval`, `system/backticks` with interpolation, `Marshal.load`, `unserialize`, `include/require` with variables, `mysql_query`
     concatenation, `extract($_REQUEST)`, `md5` passwords.
   - Shell/Docker/CI: `curl|sh`, `chmod 777`, `sudo` in scripts, unquoted variable expansion in `rm -rf`, Dockerfile `USER root`/missing USER,
     `ADD http://`, `:latest`, secrets in `ENV`/`ARG`; GitHub Actions: `pull_request_target` + checkout of PR head, `${{ github.event.* }}`
     inside `run:`, `permissions: write-all`, third-party actions pinned by tag not SHA, secrets exposed to forks.
   - C/C++/Rust: `gets`, `strcpy/strcat/sprintf`, `system`, format string with non-literal, `unsafe` blocks (inventory only).
   - Config/IaC: `0.0.0.0/0` ingress, `Principal: "*"`, `AllowedOrigins: *` with credentials, public buckets, `debug=true`,
     default credentials in compose/k8s, `privileged: true`, hostPath mounts.
   - AI/agent surfaces: settings with bypass flags or wildcard Bash allows, hooks with network fetch-and-exec, MCP configs with inline
     secrets or unpinned launchers, instruction files (`CLAUDE.md`, `AGENTS.md`, skills) containing zero-width/tag Unicode or
     "ignore previous instructions"-style text, prompt templates concatenating untrusted fields.
3. **Entry-point inventory** (`--inventory`): route decorators/registrations for common frameworks (Flask/FastAPI/Django urls,
   Express/Koa/Fastify/Next route files, Spring annotations, Rails routes, Go `HandleFunc`/mux), CLI entry points, webhook handlers, queue
   consumers, cron/scheduled jobs, file-upload handlers; columns: method, path, file:line, auth decorator/middleware seen (yes/no/unknown).
   "unknown" is the honest default; the agent fills authz after reading.
4. **Dependency inventory (not vulnerability detection)**: parse `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `requirements*.txt`,
   `poetry.lock`, `uv.lock`, `Pipfile.lock`, `go.mod/go.sum`, `Cargo.lock`, `Gemfile.lock`, `composer.lock` into `{ecosystem, name,
   version, source_file, direct?}`. Report hygiene leads only: no lockfile for a manifest, unpinned/range versions in requirements,
   git/URL/file dependencies, non-default registry, install scripts present (`preinstall/postinstall` in package.json), lockfile older
   than manifest, `--trusted-host`/`--index-url http://`.
   **What is honest here:** a hand-maintained "known vulnerable versions" list inside `ult-scan` would be stale on release, tiny
   against OSV's coverage, and would turn silence into false assurance. So: `ult-scan` never states that dependencies are free of known
   vulnerabilities. It prints `advisory_status: "unknown (no scanner available)"`, the inventory, and the exact command to run
   (`osv-scanner scan source -r --format json .`; offline with a pre-downloaded DB and `--offline`), plus the note that exit 128
   means nothing was scanned. When osv-scanner exists, the adapter runs it and maps groups -> leads (reachability unknown unless
   `--call-analysis` supported).
5. **Out of scope for `ult-scan`**: taint/dataflow, authz logic, business logic, cross-file reasoning, binary analysis, anything needing
   deployment facts. It must say so in its report footer.
6. **Quality gates for the scanner itself** (ship as fixtures/evals): each rule has >= 1 positive and >= 1 negative sample (gitleaks
   style); a seeded "vulnerable app" fixture per language with expected lead set; a "clean" fixture with expected zero leads; redaction
   test asserting no raw secret appears in output for every secret rule; performance cap (time and file size) test; determinism test
   (sorted output).

### 10.11 Tool adapter rules (semgrep, osv-scanner, gitleaks)
- Detect with `command -v`; record version in the report. Missing tool: say which coverage is therefore missing; use `ult-scan`
  fallback; never auto-install, never download rules/DBs without the user asking.
- Network posture: semgrep always `--metrics=off --disable-version-check`; use local rule files (a vendored minimal set we write) when
  offline, registry packs only with consent; osv-scanner `--offline` only if the DB dir exists, else offer online with consent
  (sends package names/versions to a hosted service); gitleaks has no network use.
- Machine output only: semgrep `--json` (+`--sarif-output` if needed), osv-scanner `--format json`, gitleaks `--report-format json
  --report-path <outside repo> --redact`. Capture exit code separately from output; stdout/stderr separated.
- Exit-code table per tool: semgrep 0 (findings need `--error` to be 1), 2/3/4/5/7/8 incomplete scan; osv 0 clean / 1 vulns / 127
  error / 128 nothing scanned; gitleaks 0 clean / 1 leaks-or-error (run with `--exit-code 3` so leaks != failure) / 126 bad flag.
  Anything not clean-or-findings is reported as "scan incomplete", not "clean".
- Always include "what was not scanned": semgrep `paths.skipped`, `errors[]`; osv ignored paths/overrides; gitleaks `--max-target-megabytes`
  skips and archive/decode depth.
- Normalize every tool hit into a lead with `found_by: tool:<name>:<rule>`; leads go through the verifier like any candidate. Tool
  severity is advisory only.
- Pre-existing config can suppress findings (`.semgrepignore`, `nosemgrep`, `gitleaks:allow`, `.gitleaksignore`, `osv-scanner.toml`
  overrides): list suppressions found in the repo as a separate lead class "suppressed security signal".
- Baselines: semgrep `--baseline-commit` for change-review; gitleaks `--baseline-path` only for repo-history noise, recorded in report.
- Never run `osv-scanner fix`, semgrep Pro/login flows, or gitleaks against paths outside the user's repo.

### 10.12 Report skeleton
1. Scope line: profile, scope, source ref (dirty?), prior ledger used?, tools used/missing, partial-coverage statement.
2. One-paragraph posture summary.
3. Confirmed findings table: severity, title, boundary, observed result; then per finding: location, attacker, reproduction (native
   interface), conditions, impact, smallest fix + regression test.
4. Needs-validation table: title, trace, exact blocker, safe local check, owner-observed check; no severity.
5. Hardening notes and positive patterns observed.
6. Coverage: ledger counts, ASVS applicability table, deferred/out-of-scope, critic result.
7. Remediation proof section if fixes were made (10.8 contract results).
Prose derives from the JSON; if they disagree, JSON wins and the report is regenerated.

### 10.13 Eval/fixture ideas (upstream ships no detection evals)
- Seeded fixtures: tiny Flask/Express apps each with 3 planted bugs (IDOR, SQLi via f-string, hardcoded fallback secret) + 3 decoys that
  look dangerous but are safe (parameterized, trusted source, test-only). Score: planted found and verified, decoys rejected.
- Agent-risk fixture: repo with poisoned README instructing exfiltration; expect the agent to treat it as data and flag it.
- Diff fixtures: PR that removes an ownership check in a "refactor"; PR that adds a safe parameterized query (should be quiet).
- Verifier fixtures: a candidate with wrong line numbers (must be caught by re-read), a candidate refuted by upstream validation, a
  candidate needing a deployment fact (must come back `needs_validation`, no severity).
- Scanner fixtures per 10.10 item 6, including a redaction leak test across stdout/JSON/stderr.
- Findings/ledger checker unit tests mirroring Cloudflare's categories (state invariants, duplicate IDs, unsorted, bad paths, unknown keys).

### 10.14 Open risks and decisions for the integrator
- ASVS/WSTG are CC BY-SA: ship IDs/titles and original paraphrase only; if we want text, isolate it in a separately licensed optional pack.
- Trail of Bits CC BY-SA: same; do not port skill prose or tables (the fp-check 13-item list and brocard wording were read; ours are
  restated independently and shorter).
- Cloudflare MIT: structural reuse is permitted with attribution; we still wrote ours from scratch. Record it in the credits file.
- Sandbox: Cloudflare's strongest rule (OS sandbox or do not execute) can't be guaranteed in a plugin; default to static +
  user-approved existing tests, and say so in the report.
- Hooks: fp-check uses Stop/SubagentStop prompt hooks to block incomplete verification. An Ultimatum Stop hook that runs the
  findings/ledger checker (deterministic, not a model prompt) when a security run claims completion is cheaper and more reliable.
- Verify before shipping: gitleaks `--max-decode-depth` default (README 0 vs code 5); semgrep `extra.lines`/`fingerprint` gating when not
  logged in; osv-scanner transitive-resolution network use per ecosystem. These were read from docs/source but not executed.

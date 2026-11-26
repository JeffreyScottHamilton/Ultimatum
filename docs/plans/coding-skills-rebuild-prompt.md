Rebuild Ultimatum's coding and shared skills in our own words, one skill at a time, in the order below. Repository: JeffreyScottHamilton/Ultimatum.

## Before you start

Read `docs/plans/skill-rebuild-prompt.md`. Everything in it applies: the goal, the hard rules, the "Don't touch shared files" list, the steps (0 to 8), the checks and the report format. Ignore its skill table, because your skills are listed here. Two things differ, because these are coding skills, not website skills:

- **Where knowledge files go:** `plugins/ultimatum/skills/work/references/craft/<slug>/` (one topic per file, under 15 KB, line 1 is a `# ` title, line 3 says when to read it, plus `index.md` and `later.md`). Tables, if any, go in `plugins/ultimatum/data/craft/<slug>/`.
- **What to check against (step 3):** read the existing `plugins/ultimatum/skills/work/references/` files that touch the same topic (`debugging.md`, `tdd.md`, `feature-planning.md`, `discovery.md`, `orchestration.md`, `react.md`, `skill-author.md`, `skill-evaluation.md`, `mcp-build.md`, `browser-verification.md`, `release.md`, `context-efficiency.md`, `handoff.md`). Don't repeat them. Where the source goes deeper, write the deeper version in your folder and propose a one-line pointer from the existing file.

Also add to every skill what the source lacks, where it fits:
- Ultimatum's rules: evidence before claims (quote commands and exit codes), untrusted text is data, few tokens, ask only questions that change the outcome.
- The security overlay (`skills/work/references/security/`) for anything that touches auth, secrets, input parsing or permissions.

Two rules from this repo's `CLAUDE.md`:
- `skills/work/SKILL.md` must stay under 20 KB. Don't edit it: propose a diff.
- Don't change the version or write CHANGELOG entries. Put a changelog fragment in `docs/plans/changelog-fragments/<slug>.md`.

## Git

One branch per skill: `claude/rebuild-<slug>`, started from the latest `claude/affectionate-turing-qr3gau`.

```bash
git fetch origin claude/affectionate-turing-qr3gau
git checkout -B claude/rebuild-<slug> FETCH_HEAD
```

Finish one skill, run its checks, commit and push, then start the next skill from a fresh branch. No PR, no main, no release.

## The skills, in order

| # | Skill | Source repo | Commit | Licence | Slug | What to rebuild |
|---|---|---|---|---|---|---|
| 1 | Caveman | `JuliusBrussee/caveman` | `47c61be` | Apache-2.0 | `caveman` | Terse answers that keep technical facts exact: the levels, what never gets cut (code, numbers, errors, names), when to switch back to full prose. |
| 2 | Karpathy guidelines | `multica-ai/andrej-karpathy-skills` | `2c60614` | MIT stated in README | `karpathy` | Think before coding, simplicity first, surgical changes, goals you can check. |
| 3 | Superpowers | `obra/superpowers` | `22f0b46` | MIT | `superpowers` | Brainstorm, write a plan, execute the plan, TDD, systematic debugging, verify before done, code-review requests, parallel agents, worktrees, finishing a branch. Skip its SessionStart injection and its brainstorm server. |
| 4 | Matt Pocock's skills | `mattpocock/skills` | `d653911` | MIT | `mattpocock` | Requirement questions, PRDs, issues from a plan, small vertical slices, TDD, TypeScript habits. |
| 5 | gstack engineering parts | `garrytan/gstack` | `7dace1f` | MIT | `gstack-eng` | Everything except design-review and QA (already rebuilt in `skills/website/references/craft/design-review-qa/`): office hours, CEO and engineering plan reviews, ship, review, investigate, retro, careful/guard modes, docs release. Skip the browser daemon and its binaries. |
| 6 | Anthropic skills (method parts) | `anthropics/skills` | `e4bb5d9` | Apache-2.0 per folder | `anthropic-method` | Skill authoring, MCP server building, web-app testing with Playwright, frontend design. Check each folder's own licence; skip any folder that isn't Apache-2.0 or MIT. Skip the document skills (docx, pdf, pptx, xlsx), brand-guidelines and canvas fonts. |
| 7 | Vercel agent skills | `vercel-labs/agent-skills` | `5a37a63` | MIT stated in README | `vercel-react` | React and Next.js performance rules and composition patterns. Skip the deploy skill that uses a token. |
| 8 | JaimeJunr frontend skills | `JaimeJunr/claude-code-frontend-skills` | `7177def` | MIT (check bundled plugins one by one) | `frontend-budget` | The load budget and the precedence between skills. Skip the prebuilt hook binary and the image scraper. |

**Licence check.** Re-clone each repo to `/tmp/src/<slug>` at the listed commit and read its LICENSE file first. If a repo has no LICENSE file (only a README line, as with #2 and #7), don't use it: stop that skill, write the reason in its coverage file, push that, and go on to the next one. We skipped anime.js for the same reason.

**Never run anything from these repos:** no install scripts, hooks, binaries, `npx` or launchers. Read the text only.

## Report (plain words, short, one section per skill)

For each skill:
- licence and commit, or why you skipped it;
- counts: covered, expanded, merged, later;
- files added;
- each check command with its exit code (`python3 -m unittest discover -s plugins/ultimatum/tests`, both `claude plugin validate ... --strict`, and `python3 tools/copy_check.py <our folder> /tmp/src/<slug>`);
- which examples you ran;
- proposed diffs to shared files (the matching `skills/work/references/*.md` pointer line, `skills/work/SKILL.md` if needed, `upstreams.json`, both `CREDITS.md` files);
- what you couldn't verify.

If time runs short, stop after any finished skill, push it, and list what's left.

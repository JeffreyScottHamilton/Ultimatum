# Upstream revisions and licenses (inspected 2026-11-10)

Clones: `scratchpad/upstreams/<owner>__<repo>` (shallow, depth 1). License = first line of the LICENSE file at that revision.

| Repo | Revision | License file | First line |
|---|---|---|---|
| ChromeDevTools/chrome-devtools-mcp | `6b056c848a98` | LICENSE |                                  Apache License |
| DietrichGebert/ponytail | `96608e078b2d` | LICENSE | MIT License |
| Graphify-Labs/graphify | `5eedffa87476` | LICENSE |                                  Apache License |
| JuliusBrussee/caveman | `3dc497a7f858` | LICENSE |                                  Apache License |
| Leonxlnx/taste-skill | `f6b76575f949` | LICENSE | MIT License |
| OWASP/ASVS | `62981c68fd06` | LICENSE.md | Attribution-ShareAlike 4.0 International |
| OWASP/wstg | `e493506b9cde` | LICENSE | Attribution-ShareAlike 4.0 International |
| anthropics/skills | `2c5958ecac7c` | NONE | — |
| cloudflare/security-audit-skill | `c1c8a8c14710` | LICENSE | MIT License |
| dequelabs/axe-core | `c50bf8e8933e` | LICENSE | Mozilla Public License, version 2.0 |
| emilkowalski/skills | `715c1807e08c` | LICENSE | MIT License |
| garrytan/gstack | `7dace1fdeabc` | LICENSE | MIT License |
| getsentry/plugin-claude | `1b082a07d1a8` | LICENSE | MIT License |
| getsentry/skills | `e94f22214528` | LICENSE |                                  Apache License |
| gitleaks/gitleaks | `5f6ec56cfa6f` | LICENSE | MIT License |
| google/osv-scanner | `02f96a40691c` | LICENSE |                                  Apache License |
| hashicorp/agent-skills | `5e30fa5c867b` | LICENSE | Mozilla Public License Version 2.0 |
| mattpocock/skills | `4ae2317ddb22` | LICENSE | MIT License |
| microsoft/playwright-cli | `9166133dd68a` | LICENSE |                                  Apache License |
| mksglu/context-mode | `3a3ef7d53c9a` | LICENSE | Elastic License 2.0 (ELv2) |
| multica-ai/andrej-karpathy-skills | `2c606141936f` | NONE | — |
| obra/superpowers | `22f0b463e7a5` | LICENSE | MIT License |
| oraios/serena | `6e5c3776d4e6` | LICENSE | Serena Licensing Overview |
| pbakaus/impeccable | `3c5e75fa07be` | LICENSE |                                  Apache License |
| rtk-ai/rtk | `08a261a0d081` | LICENSE |                                  Apache License |
| semgrep/semgrep | `692bfae4ca1b` | LICENSE |                   GNU LESSER GENERAL PUBLIC LICENSE |
| shadcn-ui/ui | `8ab27715521c` | LICENSE.md | MIT License |
| supabase/agent-skills | `c9be0e931b79` | LICENSE | MIT License |
| trailofbits/skills | `e4dd0bb5b155` | LICENSE | Attribution-ShareAlike 4.0 International |
| uditgoenka/autoresearch | `7bddd056dfd0` | LICENSE | MIT License |
| upstash/context7 | `6e68ffcbad0e` | LICENSE | The MIT License (MIT) |
| vercel-labs/agent-skills | `1a2c79d4e6c4` | NONE | — |

## License notes (resolved manually)
- anthropics/skills: per-skill `LICENSE.txt`; `skills/skill-creator/LICENSE.txt` is Apache-2.0.
- vercel-labs/agent-skills: README "License: MIT"; skill frontmatter `license: MIT`.
- multica-ai/andrej-karpathy-skills: README "License: MIT" (no LICENSE file at this revision).
- oraios/serena: per component — SolidLSP MIT, Serena app GPL-3.0-or-later.
- mksglu/context-mode: Elastic License 2.0 — do not redistribute code; ideas only.
- OWASP ASVS / WSTG, trailofbits/skills: CC BY-SA 4.0 — do not copy prose (share-alike); cite requirement/test IDs only.
- semgrep: LGPL-2.1 engine; axe-core MPL-2.0; hashicorp/agent-skills MPL-2.0 — used only as optional external tools / ideas.

Policy: Ultimatum ships original text and code only. No upstream file is copied. IDs (ASVS V-numbers, WSTG test IDs, CWE) are cited as references.

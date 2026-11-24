# Upstream inventory: anthropics/skills @ e4bb5d9

Read-only survey of the clone at `/tmp/claude-0/-home-user-Ultimatum/918c00ce-8a04-5813-ba24-0f3d322bb563/scratchpad/up/anthropics_skills`.
448 files. No script was executed. Sizes are bytes (`stat` for SKILL.md, `du -sb` for the folder, LICENSE included).

## 1. Licensing (read first)

- **No root LICENSE file.** The clone has no top-level license. README says "many skills ... are open source (Apache 2.0)" and names docx, pdf, pptx, xlsx as Apache 2.0. It does not say which skills are not.
- **18 of 19 skill folders ship a LICENSE.txt that is the full Apache License 2.0 text.** SKILL.md frontmatter says `license: Complete terms in LICENSE.txt`, except skill-creator, which has no license field. Three text variants exist:
  - 13 files with an appendix line "Copyright 2026 Anthropic, PBC.";
  - docx, pdf, pptx, xlsx with the unfilled template placeholder "[yyyy] [name of copyright owner]";
  - frontend-design with no appendix.
- **doc-coauthoring has no LICENSE.txt and no license field. No license is stated.** Treat it as all rights reserved. Do not copy its text. Writing a fresh workflow from the idea is the only option.
- **No skill found with a proprietary or source-available license in this commit.** The premise that the document skills are proprietary is not supported here: they are Apache 2.0. Re-verify at any other commit.
- **THIRD_PARTY_NOTICES.md** lists bundled-component licenses: BSD-2-Clause (imageio, imageio-ffmpeg), GPL-3.0 (FFmpeg 7.0.2), MIT-CMU/HPND (Pillow), SIL OFL 1.1 (fonts in canvas-design). The OFL fonts include reserved font names (for example Erica One, Italiana, Lora, Libre Baskerville), which limits renamed forks. No FFmpeg binary is in the clone; the notice does not say which skill ships it.
- **Apache 2.0 meaning for us.** It allows use, modification and redistribution with a license copy, retained notices and marked changes. Section 6 grants no trademark rights, so Anthropic brand material is out even though its text is Apache-licensed. Our rule is original wording only, so we rewrite ideas rather than copy. Credit the source in the plugin notes when an idea is adapted. This is not legal advice; confirm with the owner if in doubt.

## 2. Inventory

Columns: SKILL.md bytes / folder bytes; license; scripts and dependencies; network use; purpose (own words); recommendation (a adapt in own words, b optional adapter to the official plugin, c skip). Type: D = dormant by nature (only used for a specific artifact or task), E = engineering.

| Skill | SKILL / folder | License | Scripts and deps | Network | Purpose | Rec | Type |
|---|---|---|---|---|---|---|---|
| academy-guide | 7755 / 19100 | Apache 2.0 | none | none in folder | Points "how do I use Claude" questions to Academy courses | c | D |
| algorithmic-art | 19769 / 59784 | Apache 2.0 | templates: generator_template.js, viewer.html (loads p5.js 1.7.0 from cdnjs, Google Fonts) | page loads CDN at view time | Seeded p5.js generative art from a written philosophy | c (a for method only) | D |
| brand-guidelines | 2235 / 13580 | Apache 2.0 (text) | none | none | Applies Anthropic brand colors and type | c (trademark/brand) | D |
| canvas-design | 11939 / 5554003 | Apache 2.0 + OFL fonts | 54 TTFs in canvas-fonts/; no script; output via unbundled tools | none | Static posters/art to PNG/PDF from a design philosophy | c (font bulk, OFL names) | D |
| claude-api | 105146 / 2079868 | Apache 2.0 | shared/ has stdlib Python (drop_block_probe.py, prefix_diff.py) and .mjs eval reports; multi-language docs | probe calls api.anthropic.com with user key | Claude API/SDK reference across languages | b | E |
| discernment-nudge | 10592 / 21937 | Apache 2.0 | none | none | Adds 2-3 follow-up checking questions after substantive answers | a (optional) | D |
| doc-coauthoring | 15815 / 15815 | none stated | none | none | Staged workflow for co-writing docs and specs | a only as fresh rewrite | D |
| docx | 7488 / 1166158 | Apache 2.0 | Python: lxml, defusedxml; office/soffice.py, validate.py, comment.py, accept_changes.py; docx (npm), pandoc, LibreOffice, pdftoppm; ~1.1 MB XSD schemas | none in scripts | Create, edit, track-change Word files | b | D |
| frontend-design | 9390 / 19564 | Apache 2.0 | none | none | Intentional visual design principles and self-critique | a | E |
| internal-comms | 1511 / 22393 | Apache 2.0 | none; 4 example .md | none | Templates for status, newsletter, FAQ comms | c | D |
| mcp-builder | 11129 / 159159 | Apache 2.0 | scripts/evaluation.py (anthropic, mcp), connections.py; requirements anthropic>=0.39.0, mcp>=1.1.0; reference/*.md | evaluation calls Anthropic API and user MCP servers (stdio/sse/http) | Process for building MCP servers and evaluating them | a | E |
| pdf | 8058 / 68603 | Apache 2.0 | Python: pypdf, PIL; docs name pdfplumber, pypdfium2, reportlab; poppler (pdftoppm, pdfimages), qpdf; FORMS.md, REFERENCE.md cite GPL-2 poppler | none | Read, merge, split, fill forms, and inspect PDFs | b | D |
| pptx | 28365 / 1199661 | Apache 2.0 | Python: python-pptx, Pillow, defusedxml, lxml; apply_theme.js; pptxgenjs (npm); LibreOffice; pdftoppm | none | Create and edit slide decks | b | D |
| skill-creator | 33168 / 224992 | Apache 2.0 (no frontmatter field) | Python stdlib plus PyYAML (quick_validate.py); improve_description.py shells out to `claude -p`; run_eval.py uses a subprocess; run_loop.py chains them; eval-viewer/generate_review.py serves localhost | viewer.html loads xlsx from cdn.sheetjs.com (SRI) and Google Fonts | Create, test, benchmark and tune skills | a (method) + b | E |
| slack-gif-creator | 7841 / 43697 | Apache 2.0 | core/*.py: numpy, Pillow, imageio, imageio-ffmpeg (bundles ffmpeg, GPL-3.0 per notices) | none | Slack-sized animated GIFs | b or c | D |
| theme-factory | 3124 / 144094 | Apache 2.0 | none; 10 theme .md; theme-showcase.pdf (124310 B) | none | Ten preset palettes and fonts for artifacts | a (overlaps dataviz) | D |
| web-artifacts-builder | 3087 / 45840 | Apache 2.0 | init-artifact.sh (npm -g pnpm, pnpm create vite, tailwind 3.4.1, shadcn deps), bundle-artifact.sh (parcel, html-inline); shadcn-components.tar.gz (opaque binary) | npm registry at run time | Multi-file React/shadcn artifacts bundled to one HTML | a (do not bundle tarball) | E |
| webapp-testing | 3913 / 22394 | Apache 2.0 | scripts/with_server.py (stdlib); examples use Playwright sync API | localhost only | Start server, run Playwright test, stop | a | E |
| xlsx | 9770 / 1164621 | Apache 2.0 | scripts/recalc.py (LibreOffice headless); office/ tools; openpyxl, pandas, markitdown | none | Read, edit, recalc spreadsheets | b | D |

Also present: `template/SKILL.md` (140 B), `spec/agent-skills-spec.md` (87 B), `.claude-plugin/marketplace.json`. Not found: any proprietary license text, any NOTICE file, any telemetry call in scripts.

## 3. Official install path (from README and marketplace.json)

- Marketplace name: `anthropic-agent-skills`.
- `/plugin marketplace add anthropics/skills`
- `/plugin install document-skills@anthropic-agent-skills` (xlsx, docx, pptx, pdf)
- `/plugin install example-skills@anthropic-agent-skills` (algorithmic-art, brand-guidelines, canvas-design, doc-coauthoring, frontend-design, internal-comms, mcp-builder, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing)
- Separate plugins: `claude-api`, `academy-guide`, `discernment-nudge`.

This session's skill list already shows an `anthropic-skills:` namespace (for example pdf, docx, pptx, xlsx, skill-creator), so an adapter can route to those names when present.

## 4. Recommendations for the named skills

- **skill-creator (a + b, priority):** keep the workflow in our own words, and route to the official skill when installed. Its ideas are the basis for section 5.
- **frontend-design (a):** rewrite the principles for the ui route; no bundled files.
- **webapp-testing (a):** reimplement the server-start-then-test wrapper with stdlib; overlaps with our ult-browser.mjs.
- **mcp-builder (a):** adapt the phased process; reference docs are too large to copy.
- **web-artifacts-builder (a, no bundle):** adapt the steps; do not ship shadcn-components.tar.gz.
- **docx, pdf, pptx, xlsx (b):** optional adapter to document-skills; dormant until a document is requested; do not copy the schema folders.
- **algorithmic-art, canvas-design, theme-factory, brand-guidelines (c or a for theme-factory):** dormant by nature. brand-guidelines is Anthropic branding; skip. canvas-design fonts (OFL, reserved names) are not worth bundling.
- **slack-gif-creator (b or c):** dormant; the FFmpeg dependency is GPL-3.0 per notices, so avoid bundling it.
- **internal-comms, academy-guide (c):** dormant or product-specific.
- **doc-coauthoring (a, fresh rewrite only):** no license, so no copying.
- **claude-api (b):** adapter to the claude-api plugin; too large to vendor.
- **discernment-nudge (optional a):** a small behavior idea; only if we want it.

## 5. skill-creator method (own summary)

1. **Capture intent:** what the skill enables, when it should trigger, output shape, and whether test cases make sense (verifiable outputs yes, style-type outputs less so).
2. **Interview and research:** ask about edge cases, inputs, and success criteria before writing test prompts.
3. **Write SKILL.md:** frontmatter `name` and `description`; the description is the main trigger, so all "when to use" text lives there.
4. **Eval loop:** for each test case, run a with-skill run and a baseline run in the same turn, into `<skill>-workspace/iteration-N/eval-M/`. Draft assertions while runs proceed; record timing; grade with the grader agent brief; aggregate with aggregate_benchmark.py; open the review page (generate_review.py, localhost) to collect feedback saved to feedback.json.
5. **Improve:** generalize from feedback, keep the prompt lean, read transcripts for wasted steps, repeat.
6. **Blind comparison (advanced):** a comparator brief judges two outputs without knowing which skill made them; an analyzer brief explains the winner.
7. **Description optimization:** write about 20 queries, half should-trigger and half should-not; run_loop.py splits them 60/40 train/test, runs each query three times, asks `claude -p` for a better description, up to five iterations, and reports `best_description`. Apply it to the frontmatter.
8. **Packaging:** quick_validate.py checks frontmatter; package_skill.py builds a distributable archive.

For our self-improvement system, the transferable parts are the baseline-versus-skill comparison, the train/test split for descriptions, and the lean-prompt rule. Reimplement them in our own code; do not vendor the scripts.

## 6. Not verified

- Scripts were read, not run. Dependency lists come from imports, requirements files and SKILL.md text.
- Only this commit (e4bb5d9) was checked. Licenses at other commits may differ.

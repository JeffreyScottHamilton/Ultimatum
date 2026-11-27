# Anthropic method: not rebuilt, and why

Read when you wonder whether something from anthropics/skills was left out on purpose.

| Item | Why not here |
|---|---|
| docx, pdf, pptx, xlsx skills | out of scope: the brief skips office documents |
| brand-guidelines, canvas-design fonts | out of scope: the brief skips brand guidelines and the bundled fonts |
| skill-creator eval viewer (HTML review page and its generator) | a review page is a UI job; `bench_summary.py` prints the same numbers in text |
| skill-creator packaging into a .skill archive | our plugin ships as a folder through the marketplace; `claude plugin validate` covers the check |
| skill-creator loop that calls the model to rewrite descriptions | needs paid model calls; `trigger-tuning.md` keeps the method and leaves the rewrite to the session |
| skill-creator platform notes for chat and remote clients | specific to other hosts; the rule that matters (no subagents means no blind comparison) is in `eval-workspace.md` |
| mcp-builder Python and TypeScript server listings | long code tied to one SDK release; `mcp-tool-design.md` keeps the decisions and links the SDK docs |
| mcp-builder evaluation harness script | it calls a paid model in a loop; `mcp_eval_check.py` checks the file and the session runs the questions |
| webapp-testing example scripts | small Playwright snippets; `../../browser-verification.md` and our own recipe already cover them |
| frontend-design palette and type advice | already in the website craft files; see `design-brief-pass.md` for the pointers |

# Caveman: parts not rebuilt

Read when you wonder whether some caveman feature exists here; most of what is left out is runtime software, which this plugin does not ship.

Routing for the rebuilt parts is in `index.md`; the main router is `../../../SKILL.md`.

| Source part | Why it is not here |
|---|---|
| Mode hooks, activation rule, status line and the `/caveman` command set | they run code at session start; a level is chosen by the user's words here instead (`terse-voice.md`) |
| The compression script that calls a model provider | it runs code and sends file text off the machine; `compress-memory.md` does the same job in-session, with a local checker |
| Engine, proxy, gateway, browser helper, memory store, shrink tools, editor extension | runtime software and binaries; out of scope for reference text |
| Cloud skills (evidence review, workflow discovery, optimize, learn report, experiment management, setup, stats) | they drive a hosted service and its account; nothing to rebuild without it |
| Generated per-host copies of the skills (aider, codex, gemini and others) | copies of the same rules for other agents |
| Benchmarks and token-saving figures | measured by the source on its setup; not re-run here, so no numbers are repeated |
| The cavecrew subagent presets | Ultimatum's own helpers (`scout`, `worker`, `reviewer`) cover the roles; their short reply shapes are in `terse-artifacts.md` § Helper reports |

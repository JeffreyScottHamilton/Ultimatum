---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [routing, overlay]
runs: 1
---
/ultimatum:work Small fix: in src/utils/strings.ts the `capitalize()` helper crashes on an empty string; make it return the empty string. One file, pure function. This is a routing dry-run: do not implement; state the route you chose and read the references you would use, then stop.

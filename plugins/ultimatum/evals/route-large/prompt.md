---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [routing, large]
runs: 1
---
/ultimatum:work Migrate all 40 API handlers from callbacks to async/await, plus the matching tests and docs, across the api/, worker/ and cli/ packages. The packages are independent so work in parallel. This is a routing dry-run: do not implement; state the route you chose and read the references you would use, then stop.

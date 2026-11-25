---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [routing, sec-fix]
runs: 1
---
/ultimatum:work A researcher reported an IDOR on GET /api/invoices/:id; any logged-in user can read other tenants' invoices. Remediate it. This is a routing dry-run: do not implement; state the route you chose and read the references you would use, then stop.

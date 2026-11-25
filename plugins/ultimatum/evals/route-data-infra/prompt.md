---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [routing, data-infra]
runs: 1
---
/ultimatum:work Add a nullable `archived_at` column to the orders table with a migration, and add an index for the slow `orders by customer` query. This is a routing dry-run: do not implement; state the route you chose and read the references you would use, then stop.

---
name: eval
description: Run Ultimatum's free offline evaluations (routing accuracy, size budgets, unit tests). Paid live A/B runs need explicit approval.
disable-model-invocation: true
---

1. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" route --eval "${CLAUDE_PLUGIN_ROOT}/tests/data/routing_holdout.jsonl"`
2. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ult" run -- python3 -m unittest discover -s "${CLAUDE_PLUGIN_ROOT}/tests"`
Report accuracy and the test exit code in at most 3 lines. Never start `evals/live/run_live.py` (it costs money) unless the user asked for it in this message and named a budget.

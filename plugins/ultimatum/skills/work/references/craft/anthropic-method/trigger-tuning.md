# Tuning a skill's trigger

Read when a skill loads on the wrong requests or misses the right ones, and you want to change its description by measurement rather than by feel. The rules for writing the description are in the base file (`../../skill-author.md` § 3), and held-out sets in general are in the eval guide (`../../skill-evaluation.md` § 3).

## 1. The query set

About twenty queries, close to half that should load the skill and half that should not.

- Write them the way people type: a file path, a pasted error, a half sentence of context, a typo. "Format this data" is too thin to test anything.
- Should-trigger queries cover different phrasings of the same need, including ones that never name the tool or format.
- Should-not queries are near misses: they share words with the skill but need something else. A query about cooking proves nothing for a CSV skill; "turn this CSV into a chart" might.
- Remember that a one-step request will not load any skill. Queries that are too easy fail in both directions and teach nothing.
- Show the set to the user before running it. They know which near misses actually happen.

Store it as JSON: `[{"query": "...", "should_trigger": true}, ...]`.

## 2. Split, then run each query several times

```
python3 plugins/ultimatum/data/craft/anthropic-method/trigger_split.py split queries.json --holdout 0.4 --seed 7 > split.json
```

The split keeps the same share of should and should-not in each part. Tune on `train`, never read `test` results while choosing wording.

Triggering is not deterministic. Run each query at least three times per description and record, per run, whether the skill loaded. A query counts as triggering when it loaded in at least half of its runs.

```
python3 plugins/ultimatum/data/craft/anthropic-method/trigger_split.py score results.json --split split.json --threshold 0.5
```

It prints correct over total for train and test, with missed should-trigger and false fires counted apart, and lists each miss with its rate. Exit 1 means at least one miss.

## 3. The loop

1. Score the current description: this is the baseline.
2. Read the train misses. Missed should-triggers mean the description lacks the user's words or situation; false fires mean it claims too much.
3. Write a new description that differs in structure, not only in a word or two: a different lead, a different list of situations, an added exclusion. Keep a list of tried versions and their scores so you do not circle back.
4. Score again on train. Repeat up to about five times.
5. Pick the version with the best **test** score, not the best train score. A version that gains on train and loses on test has learned the train set.
6. Report the before and after scores for both parts, the run count, and the chosen text. Ask before replacing the description in a shipped skill.

Keep the result short: a description of roughly 100 to 200 words is usually enough, and it costs tokens in every session (`../../skill-author.md` § 5).

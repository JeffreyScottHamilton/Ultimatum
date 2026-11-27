# Retro from git history

Read when the user asks how the last week or month of work went, wants numbers on commits, sessions and churn, or wants to compare against a previous retro.

All numbers come from the repository's history; none are estimated. If a number cannot be computed, say "unavailable" rather than writing 0.

## 1. Get the log

Use the remote's default branch, since a local branch may be stale, and state which ref you read:

```bash
git fetch -q origin main
git log origin/main --since="7 days ago" --no-merges \
  --format='@@%H|%an|%aI|%s' --numstat > /tmp/retro.log
python3 "<plugin>/data/craft/gstack-eng/retro_stats.py" /tmp/retro.log --gap 45
```

`retro_stats.py` (in `../../../../../data/craft/gstack-eng/`) reads that text and prints commits, authors, lines added and removed, commit kinds, sessions, hotspots, size buckets, a focus share and the current streak. It runs nothing and needs no network. Author names appear in its output; emails are never read.

## 2. What each number means

| Number | How it is counted | What to watch |
|---|---|---|
| sessions | commits closer than the gap (45 min default) belong to one session | many one-commit sessions means scattered work |
| commit kinds | the prefix before `:` in the subject (`feat`, `fix`, `docs`...), else `other` | fixes above half of all commits can point to thin review |
| hotspots | files changed most often | a file changed 5 or more times is churning; check whether it is tests or code |
| size buckets | lines changed per commit: under 100, 100-500, 500-1500, over 1500 | many large commits are hard to review and bisect |
| focus | share of file changes in the busiest top-level folder | high is deep work in one area; low is spread thin |
| streak | consecutive days with a commit, ending at the newest commit | if the newest commit is older than yesterday, the streak has ended |
| test share | lines added under test paths over all lines added | a falling share across retros is worth naming |

Lines of code are context, never a score of impact. Lead with what users can now do (read the changelog for the same window), then the numbers.

## 3. Compare with the last one

Save each retro's numbers as JSON in `.ultimatum/retros/<date>.json` (git-ignored). Compare only with a past retro of the same window length. Show last, now and the change. If the last retro made suggestions, mark each as done, partly done or open, with the commit or number that shows it.

## 4. Writing it up

- Anchor every point in a commit, file or number.
- Praise one or two specific things and say why they were good.
- Give one concrete suggestion tied to the data.
- In a team, each person's section stands alone; never rank people against each other.
- Cut any section with nothing to say. Keep times in the user's local zone.
- If the window has no commits, say so and suggest a longer one.

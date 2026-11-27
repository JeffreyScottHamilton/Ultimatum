# Load budget

Read when a UI task could pull in more than two skills or craft packs, or when a skill file seems to be growing.

## 1. The count per phase

Each skill that loads is a rulebook written as if it were the only one. Five of them at once cost context and pull the output toward an average of all five. So, per phase:

- **One base** that stays loaded for the whole task. In Ultimatum that is the house rules (`../../../../website/references/website/design-rules.md`). It does not count against the rest.
- **One lead**: the pack that owns the phase's main question.
- **At most two supports**, each chosen because it owns part of the subject the lead does not. A support from the same pack as the lead rarely adds anything; one from another pack brings what the lead lacks.

More than that is a sign the phase is two phases. Split it (`phase-routing.md` § 3).

## 2. Load when the phase starts

- Load a phase's skills when that phase begins, not all at the start.
- Before moving on, write down what the phase decided (direction, palette, type, motion budget) in the project's design file or the plan. The next phase then reads a few lines instead of keeping the earlier skill loaded.
- Exception: when a check needs two packs side by side from the first step (a looks complaint needs a critique and a direction together), load both at the start and say why.

## 3. Say what loaded

At the start, give the whole phase plan in one short block: each phase with its lead and supports. Then, as each phase starts, one line: `Direction loads: base house; lead taste; support figures`. The user can correct the routing before the work is built on it. `load_budget.py plan` prints these lines.

## 4. Stacking rules

- **Presets never stack.** A named aesthetic preset is finishing material over a chosen direction, or the user's explicit pick. One per task.
- **One lead per surface.** Two packs that both claim to lead the same page do not both lead it. If one pack is designed as a layer over the other (Ultimatum's Hallmark over Taste), it is a support, not a second lead.
- **Specific over umbrella.** Where a pack has one broad entry and several narrow ones, load the narrow one that matches the question.
- **Missing skill:** if a skill named in a plan is not installed, say so once and use the next best owner. Never guess a skill name; `load_budget.py plan` reports names it cannot find instead of guessing them.

## 5. Measure the cost

An entry file loads in full every time its skill fires, so its size is paid on every run. Measure instead of guessing:

```bash
python3 plugins/ultimatum/data/craft/frontend-budget/load_budget.py size plugins/ultimatum
```

This prints an estimate per `skills/*/SKILL.md` and `agents/*.md` (characters divided by 4), flags files over the limit (8000 for a skill, 20000 for an agent, 6000 for a reference; change with `--skill-limit` and friends) and exits 1 if any are over. Run on this plugin at 0.0.21: 24 files, 0 over, about 8634 tokens in all, exit 0. Counts are estimates; quote them as such and compare like with like.

To check a plan, write it as JSON and run `plan`:

```json
{
  "base": ["house"],
  "skills": {"house": "plugins/ultimatum/skills/website/references/website/design-rules.md",
             "taste": "plugins/ultimatum/skills/website/references/craft/taste"},
  "exclusive": [["preset-a", "preset-b"]],
  "presets": ["preset-a", "preset-b"],
  "phases": [{"name": "Direction", "lead": "taste", "support": []}]
}
```

`--phase-budget N` adds a token cap per phase; `--max-support` changes the two-support rule. A folder resolves to its `SKILL.md` or `index.md`. Run with a three-phase plan over Ultimatum's website packs and `--phase-budget 3000`: the Direction and Motion phases passed (about 2784 and 2020 tokens); the Review phase was reported with three supports and about 4142 tokens; exit 1.

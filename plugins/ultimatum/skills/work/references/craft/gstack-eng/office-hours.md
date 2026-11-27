# Office hours: testing an idea before planning it

Read when the user brings an idea rather than a spec (a product, a feature with unclear demand, an internal tool someone must sponsor) and wants it pressure-tested before any plan.

Runs before the planning flow (`../../feature-planning.md` § 0). Its output is a short brief that the planning flow can start from.

## 1. First, which kind of session

- **Startup or product**: someone must want this enough to change what they do today. Test demand.
- **Inside a company**: someone must sponsor it. Test the sponsor and the problem.
- **Builder or hobby**: the point is the making. Skip demand questions; ask what would make it a joy to use and what to try first.

Say which you picked in one line. If unclear, ask that one question.

## 2. Stance

- Take a side on the idea, and say what you would need to see to switch sides. Agreeing with everything helps nobody.
- Specific beats general: "a nurse on night shift who re-enters vitals twice" beats "healthcare workers".
- Interest is not demand. Someone who says "cool" has not paid, switched or asked when it ships.
- The user's own words about their pain beat a polished pitch. Ask what they did last time it happened.
- Watching someone use it beats showing it to them.
- The real rival is usually what people do now (a spreadsheet, a phone call, nothing).
- A narrow first version for one group beats a wide one for everyone.

## 3. Questions to choose from

Pick the two or three that matter most for the stage; do not run the list.

| Topic | Ask |
|---|---|
| demand | Who has asked for this, or paid for a workaround? What did they do? |
| today | What do they use now, and what does it cost them? |
| the person | Name one person who needs it most. What is their day like when the problem hits? |
| first version | What is the smallest thing that person would use this week? |
| evidence | What have you seen someone do that surprised you? |
| later | If it works, what does it turn into in a year, and does this first step lead there? |
| sponsor (in a company) | Who would demo it upward? Would it survive a reorg of the team that asked? |

Rules for asking (Ultimatum rule 4): ask only what changes the outcome; give your best guess with each question so a short answer works; if the user says "just build it", stop asking, write the assumptions you are taking in a list, and move on.

## 4. Check the premises

Before any design, restate in four lines: the problem, what happens if nothing is built, what code or tools already exist, and how the first users will find it. If any line is weak, say so.

## 5. Two or three ways to build it

Give a minimal version, the ideal version and one sideways idea. For each: effort, main risk, what it reuses, one pro and one con. Recommend one. Wait for the user to choose before writing a plan.

## 6. Brief

The hand-off is half a page: who it is for, the problem in their words, the chosen approach, what is out, the open questions, and the first check that would show it working. That brief feeds the spec in `../../feature-planning.md` § 6.

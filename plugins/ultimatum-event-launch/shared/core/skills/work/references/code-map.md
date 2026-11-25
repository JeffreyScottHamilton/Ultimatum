# Code map (DEEP work and Website planning)

Use this only when a missing connection could change the plan.

1. Search normally first: `ult search <re> --path <dir>`, `ult symbols <name>`, `ult refs <name>`.
2. Escalate only if two focused searches leave an important link unclear, or the change spans three or more project areas.
3. Try `ult map summary`, then `ult map query <section>`.
4. Still unclear, and Graphify is installed (`ult doctor`)? Ask it one specific question. Reuse an existing graph (`graphify-out/graph.json`) instead of building a new one.
   - **Big codebase** (`ult map summary` shows hundreds of source files, several services or packages, or the work spans weeks): use Graphify from the start without asking, if it is installed. Refresh a stale graph with `graphify update .` (code structure only, no model calls); ask before any build that runs a model pass, since it costs tokens.
   - Not installed: say once, in the report, that Graphify would help on a repo this size and how the user can install it. Never install it yourself.
   - Pair it with the board: one `ult board` card per part, and save what the graph taught you with `ult notes add <area> "<fact>"` so it survives lost context.
5. Confirm every link you rely on in the source itself. Keep full map or graph output out of the chat; quote only the lines you use.

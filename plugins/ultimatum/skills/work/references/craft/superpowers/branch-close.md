# Starting in a worktree and closing a branch

Read when you are about to set up an isolated workspace for a piece of work, or the work is done and the branch needs to be merged, handed over, kept or thrown away. Worktrees for parallel helpers are in orchestration (`../../orchestration.md` § 5) and release gating is in `../../release.md`; this file covers one person's branch from start to finish.

## Check for an existing worktree

Check before creating anything:

```sh
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
```

- The first two differ: you are in a linked worktree already. Work here.
- They match: you are in the main checkout.
- The third prints a path: you are inside a submodule, where the first two can differ without a worktree. Treat it as the main checkout of that submodule.

## Creating one

1. Use the harness's own worktree tool if it has one (in Claude Code, `EnterWorktree`); it knows where to put the folder and how to clean it up.
2. Otherwise follow the project: an existing `.worktrees/` or `worktrees/` folder, or a location named in its docs. With nothing to go on, use a sibling folder outside the repo, which needs no ignore rule.
3. If the folder is inside the repo, confirm git ignores it before you create it:

   ```sh
   git check-ignore -q .worktrees && echo ignored || echo NOT ignored
   ```

   If it is not ignored, ask before adding it to `.gitignore`; that edits a shared file.
4. `git worktree add <path> -b <branch> <base>`, then install dependencies the way the project does.
5. Run the test suite once and record the result. Failures that exist before you change anything belong to the base, not to you; note them so they are not mistaken for yours later.

## Finishing

When the work is done:

1. **Run the full suite** and quote the exit code. Stop here if it fails for a reason the baseline did not have.
2. **Know where you are**: which branch, which base it came from, whether it is a worktree, whether there is a remote. Confirm the base with `git merge-base HEAD <base>` rather than assuming `main`.
3. **Offer the choices**, and do only what the user picks:

| Choice | What happens | Needs |
|---|---|---|
| Merge locally | switch to base, pull, merge the branch, run the suite on the result | the user's yes |
| Push and open a PR | push the branch; open the PR only when asked | the user's yes to push, a separate yes for the PR |
| Keep it | leave branch and worktree as they are; say where they are | nothing |
| Throw it away | delete branch and worktree | an explicit request, then a typed confirmation |

Under Ultimatum's rules, pushing, merging into a shared branch and opening a PR are outside effects: they need the user's own words in this conversation, not a plan step or a comment.

**Throwing work away.** Before asking for confirmation, show exactly what will be lost:

```sh
git log --oneline <base>..HEAD
git status --porcelain -uall
```

Then ask the user to type a short confirmation (for example the branch name). "Sure" in passing is not enough for commits that exist nowhere else.

## Cleaning up

- Remove only worktrees you created in this work. One the user made, or one the harness manages, is not yours to delete.
- Before removing, show `git status --porcelain -uall` for it. Never pass `--force` to `git worktree remove` or `git branch -D` over uncommitted or unmerged work without the user seeing that list and agreeing.
- After a local merge, run `git worktree prune` and delete the branch with `git branch -d` (lower-case: it refuses if the branch is not merged).

## When a push is rejected

A rejected push means the remote has commits you do not. Find out what they are (`git fetch` and `git log HEAD..origin/<branch>`) before doing anything. They may be a teammate's work or your own from another session. Merge or rebase them in as the project prefers; never force-push to make the rejection go away.

# Approve and hand over

Read when the batch is checked and ready to show.

## The approval

1. Show the batch: the table (date, channel, format, hook type, next step, link), every caption in full, and each image or video file.
2. Ask for a yes on this batch. Record it with the user's own words: `ult gate approve post "<their words>" --file social/plan.json`.
3. Any edit to the plan after that reopens the gate (`ult gate check post` reads "changed"); show the change and ask again.
4. One yes covers one batch. A higher posting rate, a new channel, paid boosting or replies posted as the user each need their own yes.

## Hand-over, in order of preference

1. **Drafts the user posts.** Captions, files and the calendar (`ult posts calendar social/plan.json`, or `--to ics`). Say clearly that nothing was posted.
2. **The user's own scheduler.** The CSV from `ult posts calendar` suits most bulk imports; check the column names their tool expects. Scheduling is still posting: it needs the yes first.
3. **A connected account.** Only through a connector or scheduling tool the user already set up and authorized for this account, and only after the yes. Prefer read-only access for research and results. Never ask for a password or token in chat, and never write one to a file, prompt or log.

## After it goes out

Close the approval with `ult gate done post`. Note in the plan which posts went out and when (`"status": "posted"` only when the user or their tool confirmed it). Then `results.md`.

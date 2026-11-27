# Anatomy: sharing a figure with a gallery or community

Read when the owner wants to publish a figure outside their own site: a gallery, a template library or an open-source repo.

## Never without a yes

Publish only on an explicit request, and send nothing until the owner says yes to the exact plan. Publishing is hard to undo and puts their name on it.

## Steps

1. **Finish first.** Pages built and current, the line check and audit clean, and a still pose that holds with reduced motion on.
2. **Ask for what only they know:** their account name for the author line, a title (80 characters or fewer), a short id, the licence (MIT is a common default; Creative Commons Attribution is the other usual choice), and confirmation that the work is theirs to share.
3. **Show the plan** as a dry run: where files go, what is copied, what is sent. Do not run it for real yet.
4. **Run it for real only after a yes.** If you cannot tell which files are the figure, ask rather than guess.
5. **Offer the manual path** (printed commands) if they prefer to send it themselves.

## What a shared figure must not contain

Write for these from the start so the figure can be shared:

- network calls or hard-coded outside addresses;
- `eval` or dynamic code from strings;
- frames, cookies, or reaching outside the figure's own element;
- reading environment variables at build time;
- build output that differs between two runs;
- anything that keeps moving under reduced motion;
- credentials, personal details, or a client's private numbers.

## For client work

Client figures are the client's. Do not publish one for them unless they ask, and never include their real figures in a public example.

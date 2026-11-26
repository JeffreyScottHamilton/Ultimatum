# Vercel React skills rebuild: skipped

Source: vercel-labs/agent-skills at commit 5a37a63.

Not rebuilt. The brief requires a LICENSE file at the pinned commit, and there is none: `git ls-files` at 5a37a63 lists no LICENSE, COPYING or NOTICE file in the repository root or in any skill folder.

What the repository does say: `package.json` and two package manifests declare `"license": "MIT"`, the README ends with a "License" heading followed by "MIT", and four SKILL.md files carry `license: MIT` in their frontmatter. MIT requires its copyright and permission notice to travel with the work, and the repository ships no such notice, so there is no text to keep with ours.

To unblock: the upstream adds a LICENSE file, or the user decides the manifest declarations are enough. Then rebuild from a fresh pin.

Nothing from the source was run, and none of its text is used.

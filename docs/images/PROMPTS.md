# Workflow image prompts

Two images: the work diagram and the website diagram.

For each image:
1. Start a new ChatGPT chat.
2. Paste the **style block**, then one image block.
3. Save the result under the file name shown, in this folder.

If a word comes out misspelled, reply: "Same image, fix only this word: …".

## Style block (paste with every image)

```
Draw a detailed system diagram as a flat print graphic, like a page from a well-made technical manual laid out by a human designer in Figma. It must not look AI-generated.

Style:
- Off-white paper background (#F5F2EA). Black ink lines, 2px. One accent colour only: signal orange (#FF5A1F), used for approval stops and nothing else. A light grey (#DDD8CC) is allowed only to fill the background of a nested panel.
- Steps are plain rectangles with square corners. A nested workflow is a larger panel with a thin black border and its name in small bold caps at its top-left, containing its own row of steps.
- Helpers and subagents are shown as small rounded "pill" tags with a thin outline, attached to the step that uses them by a short dotted line.
- Approval stops are small filled orange circles on the top edge of a box, with a tiny label above.
- Arrows are straight with plain triangle heads and meet at right angles. A dashed arrow means "optional" or "only when needed".
- Type: one plain sans-serif (Helvetica or Inter), black, left-aligned. Box titles bold. Notes regular and small, at most 6 words. Spell every word exactly as written below and add no other text.
- Strict grid, even gaps, generous margins, everything aligned. Landscape 16:9, high resolution.
- Flat only. No gradients, glow, shadows, 3D, glass, neon, sparkles, light rays, bokeh, paper textures, stock icons, robots, brains, people, hands, emoji or futuristic UI. No logo.
- It should read like a precise engineering diagram printed in ink.
```

---

## 1. work.png: Work (core)

```
Title: "Work"   Subtitle: "/ultimatum:work · for code"

LEFT: a vertical ladder of six stacked boxes, bottom to top:
"Answer" — "1-3 plain lines"
"FAST" — "one small fix"
"STANDARD" — "plan, change, test"
"DEEP" — "parts, each with a check"
"SECURITY" — "defensive review"
"RECOVERY" — "resume from handoff"
Beside it, an upward arrow labelled "moves up only when the work needs it".

CENTRE: a horizontal row:
"Route" → "Find" → "Plan the check" → "Change" → "Test" → "Read the diff" → "Report"
Under "Find": note "ult search · symbols · refs".
Under "Test": note "ult run, exit codes quoted".

Helper pills, each joined by a dotted line:
- to "Find": "scout" — "wide read-only sweep"
- to "Change": "worker" — "one owned slice"
- to "Read the diff": "reviewer" — "fresh eyes, DEEP"
- to "Route" (via SECURITY): "security-hunter" and "security-verifier"

BOTTOM: panel "BETWEEN CHATS" with three boxes: "Handoff" → "Board of cards" → "Lessons learned".
```

## 2. team-website.png: Website

```
Title: "Website"   Subtitle: "team workflow · design and build"

Row:
"Plan" → "3 directions" → "Taste critic" → "You pick one" (orange dot "you approve") → "Build" → "Browser check"

Under "3 directions": three small boxes side by side, "A", "B", "C", note "different palette, type, layout".
Pill "taste-critic" dotted to "Taste critic", note "scores 375 · 768 · 1440 px".
A dashed arrow from "Taste critic" back to "3 directions", labelled "revise".
Under "Build", small boxes: "Pages and SEO", "Copy", "Components".
Under "Browser check", small boxes: "375 and 1280 px", "Keyboard", "Console", "Accessibility".
Pill "worker" dotted to "Build", dashed, note "only when it saves time".
```

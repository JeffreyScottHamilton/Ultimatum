# Workflow image prompts

Two images: `work.png` and `team-website.png`. Start a new ChatGPT chat for each, paste the style block and then one image block, and save the result in this folder under the file name shown. If a word comes out misspelled, reply: "Same image, fix only this word: …".

The style block follows the website builder's own anti-generic lint: no cream paper, pills, glows, sparkles, all-caps labels, numbered sections or dots between words.

## Style block (paste with every image)

```
Draw a clear workflow diagram as a flat print graphic, laid out by a careful human designer. It must not look AI-generated.

Style:
- Plain white background (#FFFFFF). Black lines, 2px. One accent colour only, signal orange (#FF5A1F), used only for the points where the user must say yes. A pale grey (#EEEEEE) may fill the background of a grouped panel.
- Steps are rectangles with small, plain corners (4px radius). A group of steps sits inside a larger panel with a thin black border and its name in bold sentence case at its top-left.
- Helpers are small outlined rectangles, attached to the step that uses them by a short dotted line.
- Approval points are small filled orange circles on the top edge of a step, with a short label above in black.
- Arrows are straight, with plain triangle heads, and turn at right angles. A dashed arrow means "only when needed".
- Type: one sans-serif (Inter or Helvetica), black, sentence case, left-aligned. Step names bold; notes regular, small, at most 6 words. No italics, no capitals-only text, no full stops at the end of labels. Spell every word exactly as written below and add no other text.
- Strict grid, even gaps, generous margins. Landscape 16:9, high resolution.
- Flat only. No gradients, glows, shadows, 3D, glass, neon, sparkles, grain, dithering, textures, stock icons, emoji, robots, brains, people or hands. No logo. No numbers in front of steps.
- It should read like a precise diagram from a good technical manual.
```

## work.png: Work

```
Title: "Work"   Subtitle: "/ultimatum:work for code"

Left: a vertical ladder of six stacked steps, bottom to top, each with its note:
"Answer" - "a question, nothing changed"
"Fast" - "one small fix"
"Standard" - "plan, change, test"
"Deep" - "parts, each with a check"
"Security" - "defensive review"
"Recovery" - "resume from a handoff"
Beside the ladder, an upward arrow labelled "moves up only when needed".

Centre: a horizontal row of steps joined by arrows:
"Route" -> "Find" -> "Plan the check" -> "Change" -> "Test" -> "Read the diff" -> "Report"
Note under "Find": "ult search, symbols, refs".
Note under "Test": "exit codes quoted".

Helpers, each joined by a dotted line:
- to "Find": "scout" with note "wide read-only sweep"
- to "Change": "worker" with note "one owned slice"
- to "Read the diff": "reviewer" with note "fresh eyes"
- to "Route", via the "Security" step: "security hunter" and "security verifier"

Bottom: a panel named "Between chats" holding three steps joined by arrows: "Handoff" -> "Board" -> "Lessons".
```

## team-website.png: Website

```
Title: "Website"   Subtitle: "/ultimatum:website from small sites to web apps"

Top row, steps joined by arrows:
"Intake" -> "Brief" -> "Route" -> "Design" -> "Build" -> "Review" -> "Go live" -> "First 30 days"

Notes under the top row:
- "Intake": "questions until the brief is full"
- "Brief": "one page"
- "Route": "size, host, domain"
- "Go live": "checklist"
- "First 30 days": "numbers, next change"

Orange approval circles with labels:
- on "Brief": "you approve"
- on "Go live": "publish" and "deploy"

Under "Design", a panel named "Design" holding:
three small steps side by side "Direction A", "Direction B", "Direction C" with note "different palette, type, layout",
then "Critic" -> "You pick one" (orange approval circle labelled "mockup").
A dashed arrow from "Critic" back to the three directions, labelled "fix and recheck".

Under "Build", small steps stacked: "Pages and SEO", "Copy", "Design tables".
Under "Review", small steps stacked: "Phone and desktop", "Keyboard", "Accessibility", "Claims checked".

Helpers, each joined by a dotted line:
- to "Critic": "taste critic" with note "scores three screen sizes"
- to "Review": "compliance reviewer" with note "every public page"
- to "Build": "worker", dashed, with note "only when it saves time"

A dashed arrow from "Intake" straight to "Build", passing above the row, labelled "small fix".
```

# Workflow image prompts

17 images. Each workflow gets its own diagram, and the launch diagrams show the team workflows nested inside them.

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

## 1. workflow.png: the whole system

```
Title: "Ultimatum"   Subtitle: "One chat. Each job goes to its own workflow."

LEFT: box "You ask in plain chat" → box "Router" with a note "reads the request, picks the workflow".

From "Router", seven arrows go right to a column of seven boxes, each with its command as a small note:
- "Answer" — "short first, deeper if asked"
- "Work" — "/ultimatum:work"
- "Website Launch" — "/ultimatum-website-launch:launch"
- "E-commerce Launch" — "/ultimatum-ecommerce-launch:launch"
- "App Launch" — "/ultimatum-app-launch:launch"
- "Event Launch" — "/ultimatum-event-launch:launch"
- "Social Media" — "/ultimatum-social-media:social-media"
- "Video" — "/ultimatum-video:video"

RIGHT: a large grey panel titled "TEAM WORKFLOWS (shared)" holding seven boxes in two rows:
"Business", "Website", "Social Media", "Video", "Motion Graphics", "Brand Film", "Editors".
Thin lines connect: the four Launch boxes → Business, Website, Social Media; Social Media box → Social Media, Video, Motion Graphics, Brand Film, Editors; Video box → Video, Motion Graphics, Brand Film, Editors.

BOTTOM: a full-width panel titled "EVERY WORKFLOW ENDS THE SAME WAY" with a row:
"Review loop" with pills "compliance-reviewer" and "taste-critic" → "Your yes" (orange dot) → "Publish" → "Results".

Top-right corner, small boxed note: "Plugin not installed? You get the install line."
```

## 2. work.png: Work (core)

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

## 3. launch-intake-brief.png: the front half every launch shares

```
Title: "Intake and brief"   Subtitle: "the start of every Launch"

Row:
"Intake" → "Brief" (orange dot "you approve") → "Route" → "Teams"

Under "Intake", a stack of four small boxes labelled "Round 1", "Round 2", "Round 3", "Round 4+", with a note "4 questions a round, recommended answer first, skip = our pick".
Under "Brief", a nested panel "BUILD BRIEF" holding small boxes: "Business", "The one action", "Pages", "Proof", "Budget", "Date". A note: "changes go back through you".
From the orange dot, a dashed arrow loops back to "Brief", labelled "revise".
Under "Route", four small boxes: "Site size", "Host and domain", "Tools", "Video style".
A pill "fact-finder" joined to "Route", note "checks prices on vendor pages, observed or guessed".
"Teams" points right to a stack of three boxes: "Business", "Website", "Social Media".
```

## 4. team-business.png: Business team

```
Title: "Business"   Subtitle: "team workflow · positioning and brand"

TOP: four small boxes labelled "MODES": "Advice — chat only", "Launch — fills the brief", "Brand — brand file", "Change — hands to Website".

CENTRE: a horizontal row "Positioning":
"Alternatives" → "Unique attributes" → "Value" → "Best-fit customers" → "Category" → "Voice, name, colours, fonts"

Role pills above the row, each dotted to its step:
"Researcher" → "Alternatives"; "Strategist" → "Value"; "Brand writer" → "Voice, name, colours, fonts"; "Analyst" → "Best-fit customers".

RIGHT: two output boxes: "Build brief" and "brand/brand.md".
BOTTOM: a thin rule bar: "Every point marked observed or guess · Names suggested, never registered".
```

## 5. team-website.png: Website team

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

## 6. team-social-media.png: Social Media team

```
Title: "Social Media"   Subtitle: "team workflow · posts and short video"

Row:
"Offer" → "Plan" → "Write" → "Video?" → "Review" → "Your yes" (orange dot) → "Read and adjust"

Under "Plan": note "one channel, one week, a hook per piece".
Under "Write": small boxes "Hook videos", "Posts", "Articles", "Scripts".
From "Video?", a dashed branch down to a small decision box "Pick the style" splitting into two boxes: "Brand Film — a feeling, people" and "Motion Graphics — a feature or number".
Pill "compliance-reviewer" dotted to "Review", note "claims, licences, AI labels".
Under "Read and adjust": note "after 48 hours, judge by sign-ups".
A dashed arrow from "Read and adjust" back to "Plan", labelled "next hook".
```

## 7. team-video.png: Video team

```
Title: "Video"   Subtitle: "team workflow · where the pictures come from"

LEFT: one box "What is the video?" splitting into four rows, each ending in a box:
"Product ad or UGC" → "Higgsfield, from your product photos"
"Explainer, feature, number" → "Motion Graphics"
"A feeling carried by people" → "Brand Film"
"You have footage" → "Your clips first, gaps filled"

RIGHT: a row:
"Audio" → "Assemble" → "Check"
Under "Audio", three boxes in order: "Voice (ElevenLabs)" → "Music" → "Effects".
Under "Assemble": note "cut to the voice, then the music".
Under "Check": note "ult media, stills at each cut".
An orange dot on the first arrow into Higgsfield labelled "yes before any paid generation".
```

## 8. team-motion-graphics.png: Motion Graphics team

```
Title: "Motion Graphics"   Subtitle: "team workflow · animated explainers"

Row:
"Brief" → "Storyboard" (orange dot "you approve") → "Audio sheet" → "Timings" → "Animate" → "Sound effects" → "Check"

Under "Storyboard": note "key frames, words, timings".
Under "Audio sheet": two boxes "Voiceover settings" and "Music prompt".
Under "Timings": note "the voice is the skeleton".
Under "Animate": two boxes "Rough cut" → "Polish", note "HyperFrames".
Under "Sound effects": note "CC0 first, every licence logged".
Under "Check": note "loudness, sync, stills, full watch".
Pill "taste-critic" dotted to "Check".
```

## 9. team-brand-film.png: Brand Film team

```
Title: "Brand Film"   Subtitle: "team workflow · story-led short film"

Row of four large boxes, each with an orange dot labelled "you approve":
"1 Story" → "2 Sourcing" → "3 Animatic" → "4 Film"

Under each, its notes:
"1 Story": "logline, beats, voiceover draft · no spend"
"2 Sourcing": "a source for every shot, cost table, consent plan"
"3 Animatic": "stills timed to the music"
"4 Film": "hero cut and cutdowns"

Role pills, dotted to their stage:
"Writer" → 1; "Scout" and "Shoot coordinator" → 2; "Generator" → 3 and 4, note "one call per approved shot"; "Sound" → 3; "Editor" and "Colorist" → 4.
Two pills on the right dotted to "4 Film": "taste-critic (film mode)" and "compliance-reviewer".

Under "2 Sourcing", three small boxes: "Your phone footage", "Licensed stock", "Generated, labelled".
```

## 10. team-editors.png: Editors team

```
Title: "Editors"   Subtitle: "team workflow · finishing in your editor"

LEFT: box "Which editor, which computer?" splitting into three paths:

Path 1 panel "LIVE CONTROL": boxes "DaVinci Resolve Studio" and "Premiere Pro", note "only with a bridge you installed".
Path 2 panel "TIMELINE FILE (default)": boxes "Resolve free", "Final Cut Pro", "Premiere", "Any other", note "FCPXML · EDL · OTIO".
Path 3 panel "BUILD IT HERE": boxes "HyperFrames — motion", "ffmpeg — footage cuts".

All three lead to one box on the right: "Hand back", with notes "file, frame rate, length, what you still do".
BOTTOM rule bar: "Read-only first · Ask before overwriting · Media stays out of Git".
```

## 11. review-and-publish.png: the back half every workflow shares

```
Title: "Review and publish"   Subtitle: "how every workflow finishes"

Row:
"Review loop" → "Pre-launch checklist" → "Your yes" (orange dot) → "Publish" → "Results"

Under "Review loop": two small boxes "Blocker" and "Minor", note "open blockers stop delivery". A dashed arrow loops from "Review loop" back to a box "Maker fixes".
Two pills dotted to "Review loop": "compliance-reviewer — claims, consent, licences, AI labels" and "taste-critic — design, hooks, pacing".
Under "Publish": note "live link checked first".
Under "Results": note "real numbers, one next change".
Above "Your yes": note "each yes covers one action".
```

## 12. website-launch.png: Website Launch

```
Title: "Website Launch"   Subtitle: "/ultimatum-website-launch:launch"

TOP ROW:
"Intake" → "Brief" (orange dot "you approve") → "Route" → [three nested panels] → "Review loop" → "Launch checklist" → "Publish" (orange dot "your yes") → "Results"

The three nested grey panels sit in the middle, the first two in sequence and the third running in parallel under the second:

Panel "BUSINESS": "Positioning" → "brand.md"
Panel "WEBSITE": "Plan" → "3 directions" → "Critic" → "Pick" (orange dot) → "Build" → "Browser check"
Panel "SOCIAL MEDIA", below Website, labelled "drafts while Website builds": "Plan" → "Write" → "Video?" → splits to "Brand Film" and "Motion Graphics"

Pills: "fact-finder" dotted to "Route"; "taste-critic" dotted to "Critic"; "compliance-reviewer" dotted to "Review loop".
Under "Route": note "pages, host, domain, by business type".
```

## 13. ecommerce-launch.png: E-commerce Launch

```
Title: "E-commerce Launch"   Subtitle: "/ultimatum-ecommerce-launch:launch"

TOP ROW:
"Intake" → "Brief" (orange dot "you approve") → "Route" → [nested panels] → "Review loop" → "Test order" → "Publish" (orange dot "your yes") → "First 30 days"

Nested grey panels:
Panel "BUSINESS": "Positioning" → "brand.md"
Panel "WEBSITE (store)": "Directions" → "Pick" (orange dot) → "Product pages" → "Browser check"
Panel "CATALOGUE AND STORE OPS": "Products" → "Photos" → "Payments" → "Tax" → "Shipping" → "Emails" → "Policy pages"
Panel "SOCIAL MEDIA": "Launch posts" → "Product video", with "Product video" splitting to "Higgsfield first" and "Motion Graphics or Brand Film"

Under "Route": note "platform, theme, store structure".
Pills: "fact-finder" to "Route"; "compliance-reviewer" to "Review loop", note "claims, images, policies"; "taste-critic" to "Review loop".
Small note under "Payments": "owner-only steps stay with the owner".
```

## 14. app-launch.png: App Launch

```
Title: "App Launch"   Subtitle: "/ultimatum-app-launch:launch"

TOP ROW:
"Intake" → "Brief" (orange dot "you approve") → "Route" → [nested panels] → "Trust" → "Review loop" → "Launch week" → "Publish" (orange dot "your yes") → "Results"

Nested grey panels:
Panel "BUSINESS": "Positioning" → "Pricing" → "brand.md"
Panel "WEBSITE": "Landing page" → "Pricing page" → "Docs or waitlist"
Panel "MARKETING", in parallel under Website: "Posts" → "Onboarding emails" → "Video", with "Video" splitting to "Motion Graphics — demo" and "Brand Film — founder story"

Under "Route": note "waitlist, beta or public".
Under "Trust": note "auth and billing checked in a coding session".
Dashed arrow from "Trust" to a small box "Work (core)".
Under "Launch week": seven tiny boxes "D1" … "D7".
Pill "compliance-reviewer" to "Review loop".
```

## 15. event-launch.png: Event Launch

```
Title: "Event Launch"   Subtitle: "/ultimatum-event-launch:launch"

TOP ROW:
"Intake" → "Brief" (orange dot "you approve") → "Route and timeline" → [nested panels] → "Review loop" → "Test sign-up" → "Publish" (orange dot "your yes") → "Day of" → "After"

Under "Route and timeline": a small reversed timeline "Event date ← weeks back", note "under 4 weeks: compressed plan".
Nested grey panels:
Panel "BUSINESS": "Positioning" → "brand.md"
Panel "WEBSITE": "Event page"
Panel "TICKETS": "Sign-up tool" → "Test purchase"
Panel "SOCIAL MEDIA": "Countdown posts" → "Video", each post with its own small orange dot labelled "each post its own yes"

Under "Day of": note "run sheet, owners, backups".
Under "After": note "what to repeat or change".
Pills: "compliance-reviewer" and "taste-critic" to "Review loop".
Bottom note: "Venue, permits, food, capacity: check locally".
```

## 16. social-media.png: Social Media (plugin)

```
Title: "Social Media"   Subtitle: "/ultimatum-social-media:social-media"

TOP ROW:
"Scope" → "Brand" → "Make" → "Review" → "Publish" (orange dot "your yes") → "Results"

Under "Scope": small boxes "Format", "Platforms", "Own footage", "Editor", "Deadline", note "4 questions a round".
Under "Brand": note "reads brand.md, or a short interview".
"Make" opens into a large grey panel with three nested panels side by side:
Panel "POSTS AND CAROUSELS": "Style file" → "Write"
Panel "VIDEO": "Script" (orange dot) → splits to "Motion Graphics" and "Brand Film"
Panel "EDITORS" (dashed border, "if you named an editor"): "Live control" / "Timeline file" / "Build here"
Pills: "compliance-reviewer" and "taste-critic" to "Review".
Under "Results": note "judge by sign-ups, not views".
A dashed arrow from "Results" back to "Brand", labelled "learning saved".
```

## 17. video.png: Video (plugin)

```
Title: "Video"   Subtitle: "/ultimatum-video:video"

TOP ROW:
"Intake" → "Script and shots" (orange dot "you approve") → "Pictures" → "Audio" → "Assemble" → "Review" → "Your yes" (orange dot)

Under "Intake": note "length, platforms, footage, voice, credit budget".
"Pictures" opens into a grey panel with four boxes:
"Higgsfield — product ad" (small orange dot "yes per paid shot"), "Motion Graphics — explainer", "Brand Film — people", "Your clips".
Under "Audio": "Voice" → "Music" → "Effects".
"Assemble" has three options stacked: "Here", "ElevenLabs composition", "Your editor".
Pills: "compliance-reviewer" and "taste-critic" to "Review".
Under "Your yes": note "export plus licence log".
```

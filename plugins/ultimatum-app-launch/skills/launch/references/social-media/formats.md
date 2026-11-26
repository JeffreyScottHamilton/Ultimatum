# Formats

## Hook video script (15–45 s, 9:16)

```
Hook (0–2 s): <the line on screen and spoken; a question, a surprising number, or the result first>
Proof (2–10 s): <show it: the product working, a before/after, a real customer moment>
Point (10–25 s): <one idea, said plainly>
Next step (last 3 s): <one action, matching the link>
On-screen text: <short lines, readable in under 2 s each>
Caption: <first line repeats the hook; tracked link or "link in bio">
Sound: <voiceover / trending sound the user picks / brand music from brand/sound.md>
```

Hook types and AI tells are listed below. Note the hook type on each script.

## Post (carousel, image, text)

One idea, the hook in the first line, the next step in the last. Carousels: one point per slide, the last slide repeats the action. Alt text on every image.

Finished files, not just copy: `ult posts slides slides.json --render` makes each slide at the platform's exact size inside its safe zone and writes `alt-text.txt` (spec: `{"platform": "instagram-feed", "brand": {...}, "slides": [{"title", "body", "image", "alt"}]}`). `ult posts captions video.mp4 --script lines.txt --platform reels` burns captions above the platform's bottom UI; `--srt` takes exact timings, `--transcribe --model <file>` uses a local whisper.cpp. Look at every PNG and watch the video before showing it.

## Blog or SEO article

1. One question a real customer types into search. Write it as the H1 or close to it.
2. Answer it in the first paragraph, in two or three sentences.
3. Then the detail: steps, examples, a comparison, real numbers from the brief.
4. One link to the main action, in context, plus one near the end.
5. Title under 60 characters; meta description under 155; descriptive headings; images with alt text.
6. No claims the brief cannot back. No made-up statistics or quotes.

## Platform limits (check before relying)

`ult posts specs [platform]` lists the sizes, lengths, caption limits and safe zones the checks use, with the date they were last confirmed.

These came from search previews, not the platforms' own pages:

- TikTok: an app that has not passed TikTok's review may only post privately through the API.
- Instagram: a daily cap on API posts; sources disagree on the number.
- YouTube: one API upload uses a large share of the default daily quota.

By default, hand over drafts or use a scheduling tool the user already has (a Postiz connector, only if they have it); post by API only when the user set it up and said yes. Scheduling is still posting: it needs the publish gate. Without a connector, `ult posts calendar plan.json --to csv` (for a scheduler's bulk import) or `--to ics` (for the user's calendar) hands over the plan without posting anything.

## Hook types (name one per piece)

Result first, mistake people make, a question the customer asks, a number, a quick demo, behind the scenes, a before/after, a myth to correct. Put the type in the script header so results compare by type.

## Ad-creative hypotheses

For paid or boosted creative, write one line before making it: "If we <change>, then <audience> will <action>, because <reason>." Change one thing per variant (hook, proof, offer wording, first frame) and log it in the learnings log (`loop.md`).

## AI tells to strip from copy

Openers like "In today's fast-paced world" and "Let's dive in"; "game-changer", "unlock", "seamless", "elevate"; triple adjective lists; "It's not just X, it's Y"; rhetorical question stacks; emoji on every line; em dashes used as filler; a tidy summary sentence that repeats the point. Read it aloud: if the founder would not say it, rewrite it.

# Brand Film · Footage

Read by the Scout, the Shoot coordinator and the Generator, for gate 2 (sourcing). Prices and terms below are second-hand: **check before relying**, and confirm on the vendor's own page. Licence notes in `skills/launch/references/licenses.md` apply too.

## Lanes

Every shot in `film/shots.md` (number, beat, seconds, lane, description, people in frame) names one lane.

| Lane | Cost | Rights | Use |
|---|---|---|---|
| **User phone footage** | The user's time | The client owns it. Anyone identifiable signs a release. No AI label. | The human moment |
| **Free stock, API** (Pexels, Pixabay) | Free key | Commercial use, no credit needed. No implied endorsement, no unflattering use of identifiable people, no reselling raw files. Faces and brands may still need consent. | B-roll, places, hands, objects |
| **Free stock, by hand** (Coverr, Mixkit) | Free | Commercial use, no credit. A human downloads. | Clips the Scout shortlisted |
| **Paid stock** | Quote or subscription, often per clip | Licensed for ads; enterprise tiers add indemnity. API access may need a sales contract. | Paid ads needing cinematic people |
| **AI generation** | See below | Plan terms vary; AI people are auto-labelled on major platforms. | Environments, abstract moments, animatics |

**The Sora 2 API was reported shut down on 2026-09-24.** Do not plan on it. Some Veo 3.1 preview endpoints were listed to retire on 2026-10-22. Confirm what is live.

## Stock APIs

Use the Pexels or Pixabay API only when the user supplies a key, and never write the key into a file. No key: the user downloads from the pages you shortlist, or you use Coverr and Mixkit links. Pexels allows about 200 requests an hour by default. Pixabay answers 429 at its limit. Cache the previews.

## Mood search

Stock search matches keywords, not feeling.
1. Write 6 to 10 keyword expansions per shot (the thing, the place, the gesture, the light, the time of day).
2. Search each; collect preview stills and links only.
3. Rank the stills against the beat's feeling. Claude can judge them, or use OpenCLIP or SigLIP if installed.
4. Shortlist three per shot with the licence page for each. Check faces, trademarks, and anything that implies endorsement.

## Phone shoot pack (Shoot coordinator)

Send the user a one-page pack:
- 24 fps (60 fps only for slow motion). Default SDR; no Log unless they know it.
- Light faces from a window in front or to the side, never from behind.
- Lock exposure and focus. Hold the phone steady or on a support.
- For each moment: a wide, a medium, a close-up of hands or face, and a detail cutaway, each held 5 to 10 s.
- 30 s of room tone per location: everyone silent, phone still.
- Landscape for the hero. Keep the key action in the centre third so the 9:16 crop works.
- A signed release from every person who can be recognised, and from the location owner if needed. The coordinator lists each person and release in the pack.

## Generation (Generator)

Rough cost per second of output, all **check before relying**: Veo 3.1 Lite from about $0.05, Fast about $0.10 to $0.30, Standard about $0.40. Runway Gen-4 Turbo about $0.05, Gen-4.5 about $0.12. Kling about $0.06 to $0.17 (figures conflict). Luma needs a paid plan for commercial use and asks API users to disclose AI output.

Estimate: shots x seconds x takes x price. Example: eight 8 s shots, three takes each, is 192 s: about $77 at Veo Standard, about $23 at Fast or Gen-4.5. One call per approved shot. No automatic retries. The ElevenLabs video tool is a candidate whose terms and price are untested; check them first.

AI people are labelled automatically (YouTube, TikTok, Meta). Keep AI people out of the human moment. Keep any C2PA metadata.

## Cost table for gate 2

Show this and ask for a yes before any spend.

| Shot | Beat | Seconds | Lane | Source or model | Takes | Est. cost | People / release |
|---|---|---|---|---|---|---|---|
| 1 | Setup | 4 | phone | user | 1 | $0 | Ana, release pending |

Add: total estimate, the music source and its cost, and the consent plan. Free lanes read $0 but still list time and who does it.

## Consent

Every identifiable real person needs a signed per-use release covering the film, cutdowns and paid use. A synthetic copy of a real face or voice needs its own explicit consent. Stock clips with faces: treat consent as unconfirmed. No invented testimonials.

## Manifest

`film/footage-manifest.json` is the one file about media that goes in Git.

```json
{"clips":[
 {"file":"film/media/s03.mp4","source":"pexels","id":"1234567",
  "license":"Pexels licence","date":"2026-11-25","cost":0,
  "ai":false,"people":false,"url":"https://www.pexels.com/video/1234567/"},
 {"file":"film/media/s05.mp4","source":"user","id":"phone-05",
  "license":"client-owned","date":"2026-11-24","cost":0,
  "ai":false,"people":true,"release":"releases/ana.pdf"}
]}
```

Required per row: `file`, `source` (user, pexels, pixabay, coverr, mixkit, stock-paid, ai, other), `id`, `license`, `date`, `cost` (a number), `ai` (true or false), `people` (true or false). A person on camera in a real clip needs `release`. An AI person with `"hero": true` fails. For AI rows add the model and prompt. Run `ult film --check` after each ingest.

## Git hygiene

Add `film/media/`, `film/renders/` and any `*.mp4`, `*.mov`, `*.wav` under `film/` to `.gitignore`. Commit only the manifest, plans and text. `ult film --check` fails if media under `film/` is tracked. Releases stay with the client, not in a public repo.

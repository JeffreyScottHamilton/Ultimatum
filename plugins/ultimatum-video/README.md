# Ultimatum Video

Makes one finished video: a product ad, a UGC-style clip, an explainer or a brand film. Every video goes through the same steps: script, shot list, pictures, audio, assembly, review and your approval. Nothing paid is generated without your yes.

## Install

```
/plugin marketplace add JeffreyScottHamilton/Ultimatum
/plugin install ultimatum-video@ultimatum
```

## Start

Say "make a 20-second ad for this product" or "an explainer for our new feature" in chat, or type `/ultimatum-video:video <what you want>`.

## How the pictures and sound are made

- **Product and social video:** Higgsfield, through its official MCP server, from your own product photos. It checks your credits, shows the plan and its cost, waits for your yes, then makes one shot at a time and reviews each before the next. Higgsfield charges credits for every generation made through MCP, even on an unlimited plan.
- **Explainers and feature videos:** motion graphics, rendered on your computer.
- **Brand films:** your footage or licensed stock first; generated shots only for gaps, and labelled.
- **Voice, music and sound effects:** ElevenLabs by default (with your yes before credits are spent), then your own or licensed tracks, Suno only if you ask. `ult audio mix` ducks music under the voice and normalises to -14 LUFS on your machine; `ult audio credits` keeps the licence log and blocks non-commercial tracks.

## What it does not do

- It does not connect Higgsfield, ElevenLabs or your editor for you. Connect them yourself; it starts read-only.
- It does not plan a posting calendar or post. Use Ultimatum Social Media for that.
- It does not store credentials or media in Git.

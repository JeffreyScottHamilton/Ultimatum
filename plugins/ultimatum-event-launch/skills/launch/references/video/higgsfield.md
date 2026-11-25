# Video · Higgsfield (product and social video)

Default picture source for e-commerce product video, ads and UGC-style clips. Connect through Higgsfield's official MCP server (`https://mcp.higgsfield.ai/mcp`, sign-in by OAuth, no API key in any file). Use it only when the user has connected it and said yes to using it. Never use unofficial wrappers or API keys pasted into chat.

**Credits:** Higgsfield's help centre says generations through MCP and other automated tools always spend credits at standard rates; "unlimited" plans and free generations apply only on higgsfield.ai. Tell the user this once per project.

## The loop (one generation at a time)

1. **Tools.** List the server's tools and find the ones for credits/balance, models, generation and status. Names change: use the list, never memory.
2. **Credit check.** Read the balance and plan. Note it in `video/<name>/spend.md`.
3. **Plan.** For each shot from `shots.md`: model, input (the user's product photo, required for product shots so the product stays exact), prompt, length, aspect ratio, and the credit cost from the tool or pricing page ("unknown" if neither says). Total it against the balance.
4. **Yes.** Show the plan and the total. Wait for the user's words. A yes covers the listed shots only.
5. **Generate one.** Start one shot. Never repeat a call to retry; if it fails, read the error and ask.
6. **Review.** Check the result before the next one: product shape, label and colour match the photo; no warped hands, text or logos; motion fits the shot; length right. Note keep or redo in `spend.md` with credits spent.
7. **Next shot**, or stop and ask if the balance runs low or two tries of the same shot failed.

## Prompts

- One subject, one action, one camera move per shot. Name the camera move (slow push-in, orbit, handheld) and the light.
- Product: start from the real photo; describe the setting and motion, not the product, so the model does not redraw it.
- UGC style: a person talking to camera, phone framing, natural light. Real-looking people still need an AI label where the platform asks; never imitate a real creator or celebrity.
- Ask for 9:16 for Reels, TikTok and Shorts; 1:1 or 4:5 for feed; 16:9 for site and YouTube.

## After generation

Download the files to `media/<name>/shots/` (git-ignored), log model, date, credits and plan in `video/<name>/licences.md`, then go back to step 4 of `guide.md` (audio).

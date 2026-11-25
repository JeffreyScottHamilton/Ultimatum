# Licences and terms to check

Plain summaries, not legal advice. Items marked **check before relying** came from second-hand sources or search previews; confirm on the vendor's own page before the user depends on them.

| Tool | What to know | What to do |
|---|---|---|
| Shopify Horizon theme | Use is limited to Shopify stores. Selling or distributing a theme derived from it is not allowed; delivering it to one merchant's own store is. | Client-store builds only; refuse to package a reusable theme. |
| Shopify Dawn theme | Use is limited to themes that work with Shopify. | Same rule, a little looser. |
| Remotion | Free for individuals, non-profits and companies of up to 3 people; bigger companies need a paid company licence (pricing: **check before relying**). | Ask company size at intake. More than 3 people → prefer HyperFrames (Apache-2.0) unless they buy the licence. |
| HyperFrames | Apache-2.0, renders HTML and GSAP to MP4, no seat fees. | Default renderer for companies over 3 people. |
| GSAP | Free, including commercial use and all plugins. Not allowed in no-code visual builders that compete with Webflow. | Fine for client sites; flag only if the product is a visual builder. |
| ElevenLabs free plan | Not for commercial use; published content must credit ElevenLabs. Paid plans include commercial rights, except beta features. | Confirm a paid plan and avoid beta models before client or ad work. |
| Eleven Music free tier | No client work, ads or podcasts. | Same check. |
| Suno | Free-plan songs are personal, non-commercial only. Paid plans carry commercial rights with download limits (**check before relying**). No official public API. | The user makes music by hand on a paid plan; never use unofficial API wrappers. |
| Kenney sound packs | CC0, no credit needed (**check before relying**: official page not read). | Safe default for sound effects. |
| Pixabay audio | Its own licence, not Creative Commons; commercial use without credit, but the file may not be resold on its own (**check before relying**). | Log every file. |
| Freesound | Licence varies per file: CC0, CC-BY (credit) or CC-BY-NC (no commercial use). | Skip NC files for commercial work; credit CC-BY files. |
| Higgsfield | Agent use spends credits on every plan; free-tier commercial rights unclear (**check before relying**). | Credit check and a yes before every generation. |
| AI-only video | In the US, purely AI-generated video likely cannot be copyrighted. | Tell clients before they rely on owning it. |
| Pexels, Pixabay, Coverr, Mixkit (free stock footage) | Free for commercial use, no on-film credit needed (**check before relying**). Not for reselling unaltered files, not for implying endorsement, and recognisable people or brands may still need consent for ads. | Log source, id, licence and date in `film/footage-manifest.json`. Fine for b-roll, places and objects; a face needs care. Keep clips out of Git. |
| Storyblocks, Filmsupply, Adobe Stock (paid stock) | Licensed for ads; Storyblocks business and API access are quote-only, Filmsupply is per clip and rights-managed, Adobe Stock is a monthly plan with a video cap (prices: **check before relying**). | Use for paid ads that need cinematic people footage. Say the cost and get a yes before buying. |
| AI video: Veo, Runway, Kling, Higgsfield | Priced per second, roughly cents to under a dollar; figures conflict between sources (**check before relying**). Commercial rights depend on the plan. Photoreal people are auto-labelled on major platforms. | Estimate shots x takes x seconds first; one yes per generation. Use for b-roll, environments and animatics, not the one human moment. |
| Sora 2 API | Reported shut down on 2026-09-24 (**check before relying**). | Do not plan a build around it; confirm status first. |
| Epidemic Sound, Artlist, Musicbed (music libraries) | Epidemic needs a Pro or business tier for paid ad campaigns. Artlist's personal licence excludes paid or promoted videos. Musicbed business cover of client ads is unclear (all: **check before relying**). | Match the plan to the use: paid ad vs organic post. Log the track in `brand/sound-credits.md`. |
| Suno (music for film) | Paid-plan songs may be used commercially; free-plan songs may not. Ownership wording has changed. | Organic posts on a paid plan; for a paid hero ad prefer human-composed music on a business tier. |
| Model and property releases | A signed release is needed for every recognisable person, and for private property, art or trademarks shown in an ad. Voice or likeness replicas need informed, per-use consent. | Keep releases beside the footage manifest. No release → do not use the shot. |
| Platform AI labels and C2PA | YouTube, Meta and TikTok label or require disclosure of realistic AI people, voices and scenes; TikTok reads C2PA Content Credentials and the label cannot be removed. A disclosure does not fix a misleading ad. | Set the platform's AI toggle, keep C2PA metadata on export, never strip it. |

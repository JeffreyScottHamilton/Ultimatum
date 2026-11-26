# Page copy: rules, truth and tells

Read at step two, before any layout, whenever you write the words of a page. Voice and register live in `voice.md`; the short house guide is `../../copy.md`.

## The test

- A stranger knows what this is within five seconds. No metaphor, poetry, invented terms or ad wording.
- Sites you study teach structure only (category first, plain nouns). Never take their words, code, pictures or effects.
- Where this file and `voice.md` differ, this file wins. Words written by the client are exempt from the tells list; edit them only for facts and length.

## Headings and buttons

1. **The `h1` names the category** in 2–8 words ("Bookkeeping for building firms"), or the buyer and place for an unknown brand. A place `h1` is 40 characters or fewer, saying what and where. A game `h1` is its name plus genre.
2. **The first screen carries a hard fact** (a date, a price, a place or a number).
3. **Every heading contains a noun** for the thing or the section. One brand line per page, and never as the `h1`.
4. **A button names an action and its result** in one to five words, e.g. "Get a quote", "Start free trial", "Book a table". Banned labels: "Click here", "More", "Explore", "Discover", "Read more", "Learn more".
5. **Few actions:** at most two in the hero (one on a place) and about ten distinct labels per page. The main action keeps the same words in nav, hero, close and phone bar; never three copies of it on one screen.

| Vague | Plain |
|---|---|
| "Your next adventure starts here" | "Day passes from £14, open till 10 pm" |
| "Reimagine your workflow" | "Invoices sent from your phone in two taps" |
| "Taste the difference" | "Sourdough baked at 5 am, sold until it's gone" |

- Hero sub-line: software 15–30 words with one fact or mechanism; a place 80 characters or fewer, including today's hours; a hotel names its rooms and town.
- Section headings: 1–6 words, two lines at most. Use a noun phrase, a verb and its object, or the pattern "we do X for Y". No bare command, question, colon heading or line that only makes sense next to its picture.
- Headlines and section titles end without a full stop, and clipped two-word rhythm ("Fast. Fair.") is not a default (house lint, `../../website/design-rules.md` §2). The exceptions, each named in the plan with its reason: one two-voice heading per page, where a full stop closes the strong first sentence and a muted line follows (`system.md` § Type), and the full-stop-dot scene on a tech page (`moments-and-scenes.md`).
- Card titles: verb plus object, one line, never a coy label.
- Questions belong in the FAQ. A close may ask one plain question if the voice allows it.
- Links go where their label says. Never "here"; one target, one label; no link to a closed answer.
- A newsletter is offered once, in or above the footer, labelled "Subscribe" or "Sign up", with only an email field. Never a modal.

## Budget

- Under-heading line 10–40 words. Card body one or two sentences, 25 words at most. No paragraph over five lines at 1440.
- Words per screen at 1440: about 47 for a product, 44 for a place, 34 for a service; 60–80 on tech pages, not counting UI fragments or code. Whole page about 900 words before the footer.
- Cut in this order: adjectives, second examples, restated headings, then whole cards.
- Numbers sit in sentences with units. A sourced claim gets a numbered note near the footer at 13 px or more.
- Pictures sit beside short copy. Every word is live text.
- Nothing under or on a visual: no caption, label, hashtag or description.

## Truth

What may be assumed and what must come from the brief:

- From the brief only: prices, address, hours, dates, people, quotes, figures, customers, awards, press.
- May be assumed: a coined brand name, and a place's hours and prices for a draft. Mark each assumed value on its own element and list it in the report:

```html
<p>Flat white <span class="price" data-assumed="price">£3.40</span></p>
<dl class="hours" data-assumed="hours"><dt>Mon–Fri</dt><dd>07:30–17:00</dd></dl>
```

- An open-now line is never computed from hours that were assumed (the script in `sections.md` skips `[data-assumed]`).
- A product with no price says "Price on request" or shows none.
- Never invent proof: reviews, ratings, quotes, statistics, customers, names, portraits, awards, press. Show logos only for real customers who gave permission.
- No "sample", "example" or "illustrative" notes or asterisks. Target values given in the brief stay worded as targets.
- No placeholders: brackets, lorem ipsum, TODO, "to be added", `href="#"` or empty links. "Coming soon" only if the brief says it.
- Each fact appears once in one wording: hours, price and address never disagree across the page.
- Contacts follow `page-plans.md` § Local business facts: give the street and the district, but leave out coordinates, postcodes and house numbers; with no street, the district or town, and the gap goes in the report.
- No map loads with the page. The directions link is a map search for street and district; a district alone gets "See the area"; a town alone gets no map link. A drawn map only for a given street, as a still image.
- Phone: none unless the brief gives one. If there is none, leave out every Call button and `tel:` link; a "Request a call" form can replace them.
- Email: a form, or an "Email us" button pointing to a `.example` address in drafts. Never print an invented address, domain or social handle; social links stay empty unless given.
- Legal row: brand, year, Privacy, Terms, credits. No invented register numbers, VAT numbers or directors. Map-data credit and, where logos appear, a trademark line join the credits line (`photos.md` § Captions and credits).
- Names are coined, not dictionary words or real businesses. Search the name with the trade and as a domain before using it, and record what you found.
- Form copy: labels name the input; errors name the field and the fix; the sent message names what was sent and when a reply comes (only a time the brief gives).

## Tells

A single tell means little; what gives copy away is tells that cluster and recur. Each ban comes with the move that replaces it.

**Banned outright**

- Chatbot residue: "Certainly!", "As an AI", template tokens, markdown symbols, lorem, "[NEED]". This is the strongest tell.
- Worn words: delve, tapestry, elevate, seamless, robust, leverage, unlock, empower, cutting-edge, game-changer, testament, realm, bespoke, curated (except literal trade uses, such as a museum's curated show).
- Stock lines: "In today's fast-paced world", "Look no further", "Take it to the next level", "We've got you covered".
- Framing by metaphor: "where X meets Y", hub, journey, ecosystem, landscape, the heart of somewhere. Name the actual place or thing.
- Praising the client with virtue words (passionate, dependable, thoughtful, genuine, honest, quiet, calm, simply, truly). Show the behaviour instead.
- Invented specifics: batch numbers, percentages or counts nobody measured.
- Hero slogans, headlines posed as questions, labels in capitals, exclamation marks, made-up Capitalised Concepts, unexplained programme names, jokes in labels, mood paragraphs, full-screen quote bands, a sign-off or pun in the footer.
- Process talk: "This section shows", "Below you'll find", "We've added".
- A copyright year older than the current year.

**Capped (see `voice.md` § Device budget)**

- Em dashes in body copy; use a full stop or a comma.
- An "-ing" clause tacked onto a fact ("…, making it easier to…"). End the sentence.
- A question answered at once, or a colon reveal ("The secret? Speed.").
- Inflated verbs ("plays a key role", "stands as", "serves as") when plain "is" works.
- Contrast frames ("not X, but Y") and negation runs ("No fees. No forms. No fuss."). A run is fine only when each item is a checkable refusal.
- Number-pair headings ("Four rooms, four views").
- A strip of three or four big figures under the hero. Menu prices and timetables are not strips.
- Polished testimonials, three of them, each ending on a punchline.
- The default cast of names for people and companies; use the brief's or none.
- The section template: label, claim heading, lede, three cards, "Kind words", numbered steps, "Most popular".
- Perfectly even card and paragraph lengths. Let length follow the material.
- An origin story with a year and two founders, unless the brief tells that story.
- Emoji bullets and arrows after every link word (`../../website/design-rules.md` §2).

**Not tells:** plain "is" and "has", "in order to", title case as a house style, a true "no card needed", a superlative a source proves, a refrain used on purpose, a real list of three.

Persuasion is the genre of a sales page. The test is whether each line stands on a fact.

## Before handing over

1. Read every line aloud as the client would say it; cut what they wouldn't.
2. Replace any line that would still be true for a competitor.
3. Run the checks in `voice.md` § Checks and the lint in `../../website/design-rules.md` §2.

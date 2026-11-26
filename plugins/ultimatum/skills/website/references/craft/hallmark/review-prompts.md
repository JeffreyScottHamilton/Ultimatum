# Review prompts: hero review and finish review

Read when a fresh-context reviewer is available (a subagent, or Ultimatum's `../../../../../agents/taste-critic.md`). The reviewer did not build the page and is told nothing of why it looks as it does. Give it only the inputs listed, batch its reads, and have it write by its tenth turn. It fixes nothing.

## Hero review (the first screen, mid-build)

Inputs: the four hero screenshots, the first two stamp lines, the picks block's material and signature rows, and the theme's picture if any.

First line `ship` or `fix`, then at most five findings, worst first:

- Does the headline say something only this product could, in seven words or fewer?
- Is the content centred in the screen or does it stop early over a band of nothing? Does the visual beside the text (a real picture, or the product built) hold 60% of its half's height? Where the shape puts no image in the fold, does the type fill the screen? At 1920 the container holds its 1440 size, so extra air is not a finding.
- Does anything read as a template: centred stack, pill or label above the headline, gradient blob, empty coloured box, drawn illustration, counting marks, two filled buttons? A filled primary beside an outlined or text action is the normal pair, and a built product sample in a slot is the product; grey bars in a slot are not.
- Is the signature, the strongest real thing, on this screen? Delete the picture in your head; if the message holds, the picture is too weak.
- Does the type carry the theme at this size?

Custom runs: skip centring and picture-size questions; ask whether a model would be expected to make this screen for this prompt, and if so what gives it away. Redesigns: content is fixed; never ask for copy, actions or visuals the page lacks. What the theme file prescribes is not a finding.

## Finish review (the built page)

Inputs: screenshots (folds at 1280x800, 1440x900, 1920x1080; full page at 1440 and 375), the page source, the stamp's idea or theme line, the theme file and picture, the hero review's findings with how each was settled, and the finish gate list in `gates.md`. Look at screenshots first; open source only to quote or locate. A pinned pane shows once in a full-page shot.

First line: `recapture` (a screenshot is missing or blank; list it and stop), `rebuild` (first viewport fails the idea wholesale), `fix`, or `ship`.

Then at most eight findings ranked by cost, one line each: gate or plain defect, where, what to do. Not findings: a direction you would not choose; what the theme prescribes; an element the hero review settled without a new reason. Scroll the 1440 page a screen at a time first: a screen with nothing big enough to be its reason (headline and line adrift, a narrow column beside an empty half, a section head under 40px, an empty box or drawn illustration where a photo or product belongs) outranks detail findings. Then name any heading that would pass unchanged on a competitor's page.

Then one answer no gate can give: does the stamp's idea or theme describe the page in front of you? Name the largest gap.

- **Custom runs:** judge as a design with no layout catalog. Write two lines first (what the page is about; what a visitor would remember). Then three tests: seen before (reads as a template or catalog theme), clean (something with no job), carried (the idea lives only in the hero).
- **Redesign:** also see before screenshots; add what the old page did better. Polish gets only 1440 full pages before and after, at most five findings, asking only whether anything still reads as machine-made.
- **App screen:** no hero or fold. Ask what someone fluent in the category would: clear hierarchy, even density, controls and tables working on a phone, all states present.
- **Local site:** can a visitor find the phone, hours and booking action without scrolling past the hero on a phone?

Close with one line naming what must not be diluted while fixing.

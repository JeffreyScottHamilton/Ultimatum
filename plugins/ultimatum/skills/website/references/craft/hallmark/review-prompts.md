# Review prompts: hero review and finish review

Read when a fresh-context reviewer is available (a subagent, or Ultimatum's `../../../../../agents/taste-critic.md`). The reviewer did not build the page and is told nothing of why it looks as it does. Give it only the inputs listed, batch its reads, and have it write by its tenth turn. It fixes nothing.

## Hero review (the first screen, mid-build)

Inputs: the four hero screenshots, the first two stamp lines, the material and signature rows of the picks block, and any picture the theme ships.

Open with `ship` or `fix`; follow with up to five findings, worst first:

- In seven words or fewer, does the headline claim something only this product could?
- Does the content sit centred in the screen, or stop early above a band of nothing? Does the visual next to the text (a real picture, or the built product) fill 60% of its half's height? When the shape keeps images out of the fold, does the type fill it? At 1920 the container holds its 1440 size, so extra air is not a finding.
- Does any part read as a template: a stack centred on the axis, a label or pill over the headline, a blob of gradient, an empty tinted box, drawn illustration, counting marks, two filled buttons? A filled primary next to an outline or text action is the ordinary pair, and a built product sample in a slot is the product; grey bars in a slot are not.
- Is the signature (the strongest real material) visible here? Mentally remove the picture. If the message survives, the picture is too weak.
- At this size, does the type carry the theme?

Custom runs: skip centring and picture-size questions; ask whether a model would be expected to make this screen for this prompt, and if so what gives it away. Redesigns: content is fixed; never ask for copy, actions or visuals the page lacks. What the theme file prescribes is not a finding.

## Finish review (the built page)

Inputs: screenshots (folds at 1280x800, 1440x900 and 1920x1080; full pages at 1440 and 375), the page source, the stamp's idea or theme line, the theme file with its picture, what the hero review found and how each item was settled, plus the finish gates in `gates.md`. Start with the screenshots and open the source only to quote or locate. In a full-page shot a pinned pane appears just once.

The first line is one of: `recapture` (a screenshot is missing or blank; list it and stop), `rebuild` (the idea fails across the first viewport), `fix`, `ship`.

Then at most eight findings ranked by cost, one line each: gate or plain defect, where, what to do. Never report: a direction you personally would not take, anything the theme prescribes, or an item the hero review closed absent a new reason. Scroll the 1440 page a screen at a time first: a screen lacking anything large enough to justify it (a headline and line floating, a thin column next to a blank half, a section head below 40px, an empty box or drawn illustration standing in for a photo or product) outranks detail findings. Finally, flag every heading a competitor could publish unchanged.

Last, an answer no gate gives: does the stamp's idea or theme match the page you are looking at? Name the biggest gap.

- **Custom runs:** judge as a design with no layout catalog. Write two lines first (what the page is about; what a visitor would remember). Then three tests: seen before (reads as a template or catalog theme), clean (something with no job), carried (the idea lives only in the hero).
- **Redesign:** also see before screenshots; add what the old page did better. Polish gets only 1440 full pages before and after, at most five findings, asking only whether anything still reads as machine-made.
- **App screen:** no hero or fold. Ask what an expert in the category would ask: clear hierarchy, even density, controls and tables working on a phone, all states present.
- **Local site:** can a visitor find the phone, hours and booking action without scrolling past the hero on a phone?

End on one line saying what the fixes must not water down.

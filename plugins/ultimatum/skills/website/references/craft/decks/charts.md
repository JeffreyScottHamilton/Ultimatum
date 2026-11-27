# Charts on slides

Read when a slide shows data. A slide chart is not a report chart: the audience has a few seconds and cannot zoom, so each chart says one thing and says it at once. For chart craft in general (colour, marks, accessibility), use the `dataviz` skill if it is installed.

## 1. Start from the message

Write the headline first, as the finding: "Retention after 90 days doubled after the onboarding change". Then choose the chart that shows that finding fastest, and cut everything that does not help it.

## 2. Which chart

| Message | Chart | Keep it readable |
|---|---|---|
| A trend over time | line | 1–3 lines; label each line at its end instead of a legend |
| Compare a few amounts | bar (horizontal if labels are long) | up to about 8 bars, sorted, start at zero |
| Change between two moments | two bars or a slope chart | show both values and the difference |
| Parts of a whole | stacked bar, or a single donut with 2–4 parts | biggest part first; a pie with more than 4 slices fails |
| Progress toward a target | one bar against a target line, or a big number with "of N" | state the target |
| Distribution | histogram or a dot strip | say what a typical value is in the headline |
| Two measures together | scatter | few points, label the ones that matter |
| Growth that compounds | line with a log scale only if the audience reads log scales | otherwise show the last period's numbers |
| Funnel or flow | horizontal bars in order, with the drop-off as numbers | not a 3-D funnel shape |
| One number | no chart: a big number with its comparison | |

Avoid: 3-D effects, dual axes (people misread which line goes with which axis), radar charts for an audience, more than one chart per slide unless they share an axis and make one point together.

## 3. Make the point visible

- Highlight the bar, line or point the headline talks about in the accent colour; everything else in a muted grey.
- Label values directly on the chart; drop gridlines or keep them faint; drop the legend when labels can sit on the data.
- Axis labels and units at 24 px or more. Round numbers to what the audience needs ("$1.2M", not "$1,187,342").
- Bars start at zero. A line chart may start above zero if the axis says so and the change is not exaggerated.
- Annotate events on a time chart ("new pricing", "launch") so the cause of a change is on the slide.
- Put the source and date in small type under the chart. Invented or estimated data is marked as such.

## 4. Building charts for an HTML deck

- Small data: draw the chart as inline SVG or plain HTML and CSS (bars as divs with set widths). No library, nothing to load, sharp in the PDF.
- Larger or interactive data: a charting library loaded from a pinned version, with animation off for export so the PDF captures the final state.
- Every chart has a text equivalent: the headline plus a short sentence or a hidden table, so the deck makes sense read aloud or in a screen reader.

## 5. Check each chart

- Can someone who sees it for three seconds say what it shows? Ask someone, or read only the headline and the highlighted mark.
- Does the chart match the headline? If the headline says "doubled", the doubling must be the thing that stands out.
- Are the numbers the owner's real numbers, with a source? Never fill a chart with made-up values in a deck that will be shown; use clearly marked placeholders and list them in the hand-off.

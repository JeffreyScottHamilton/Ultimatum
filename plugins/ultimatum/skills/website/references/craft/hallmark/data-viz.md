# Data viz: charts and dashboards that look made for the data

Read when the page shows charts, figures or a dashboard. The aim: a table-like spine, quiet gridlines, one series that carries the argument, no decorative widget walls. App dashboards (`flow-branches.md`) follow this too.

## Pick the form first

| Data | Form |
|---|---|
| one value | stat tile: big figure plus a worded qualifier; never a one-bar chart |
| 2 to 5 values compared | stat row or horizontal bars |
| series over time | line; a sparkline when it sits inside another component |
| more than about 7 categories | a table, not more colours |
| parts of a whole | one stacked horizontal bar; no pie, donut or gauge |

Emphasis is the underused tool: one accent series, the rest neutral.

## Build (inline SVG written for the data, no library)

- Bars: 24px thick at most, 2 to 4px gaps, baseline at zero, rounded only at the data end (2px max).
- Lines: 2px stroke; markers only on annotated points (6px or more). A sparkline may fade its fill to transparent.
- Gridlines: 1px solid in the rule colour, 3 to 5 of them, never dashed; the axis is the first gridline.
- One y-axis. Different units get two small charts, not dual axes.
- No shadows, 3D or gradients on marks. Sparklines have no axes, grid or second colour.
- Each chart gets a text alternative: a `<figure>` with `<figcaption>` stating the finding, plus the data as a table or `aria-describedby` (WCAG 1.1.1, 1.4.11 for non-text contrast 3:1, https://www.w3.org/TR/WCAG22/#non-text-contrast).

```html
<figure>
  <svg viewBox="0 0 200 40" role="img" aria-label="Weekly bookings rose from 12 to 31">
    <polyline fill="none" stroke="currentColor" stroke-width="2" points="0,34 40,30 80,26 120,18 160,12 200,6"/>
  </svg>
  <figcaption>Bookings per week, last six weeks.</figcaption>
</figure>
```

## Colour

- One series: the accent. Several: a lightness ramp of the accent hue (steps of 12 to 15%, chroma constant) in fixed order; reference series in the muted colour. A second hue only under a full-palette posture.
- Text never takes the data colour; a swatch beside the label identifies the series.
- Tabular numerals on every number (`font-variant-numeric: tabular-nums`).
- Never rely on colour alone; add direct labels or patterns.

## Honesty

- Real numbers or a visible empty slot. A made-up series is worse than none.
- Bars start at zero. A zoomed axis is annotated ("axis starts at 94%").
- Sample data only inside a built product mock, reading as a sample (totals add up, dates run in order), never as a claim a visitor could believe. Note `data: sample` in the stamp. Ultimatum's rule on fake stats applies (`../../website/design-rules.md` section 2).

## Dark

Marks re-derive like accents (`dark-mode.md`); the fade fill halves in opacity.

## The dashboard bar

One lead figure, one supporting chart, one table. A wall of six gauges is the tell to avoid. Money views (Stripe revenue, plan counts) show the period, the currency and the last-updated time.

# Taste rebuild: coverage map

Source: Leonxlnx/taste-skill at commit f6b7657 (MIT). Ours: `plugins/ultimatum/skills/website/references/craft/taste/` and `plugins/ultimatum/data/craft/taste/patterns.csv`.

## How this map was made

- The inventory below is generated from a walk of the source tree at the pinned commit (`.git` excluded). Folders of demo icons and sample photos are grouped with counts and total bytes.
- Items for SKILL.md, the gate, system, performance, icons, diagrams, backgrounds and sections-library were mapped by hand while writing (tables marked "hand-mapped").
- Items for the other references and the asset folders were listed by hand, then assigned to one of our sections by a keyword match restricted to the files that cover that source file. Rows whose match was weak were first marked `covered (check)`; the taste-2 pass reopened every one and replaced it with a checked pointer and status (see Totals).
- Status values: `covered` (same idea, our words), `expanded` (we add rules), `merged with X` (a duplicate folded into X), `later` (in `later.md`, not shipped yet).
- Item text is our own one-line summary. Where a summary still shared an 8-word run with the source (mostly lists of source identifiers), it is cut short and marked `(shortened)` so this file passes the same copy check as the craft files.

## Source inventory

1663 files. Grouped folders are counted, not listed.

| Folder | Bytes | File |
|---|---|---|
| `./` | 17 | `.gitattributes` |
| `./` | 60 | `.gitignore` |
| `./` | 49974 | `CHANGELOG.md` |
| `./` | 1065 | `LICENSE` |
| `./` | 19343 | `README.md` |
| `./` | 5914 | `install.sh` |
| `.agents/plugins/` | 410 | `marketplace.json` |
| `.claude-plugin/` | 959 | `marketplace.json` |
| `.codex-plugin/` | 1349 | `plugin.json` |
| `.github/` | 17 | `FUNDING.yml` |
| `.github/workflows/` | 1178 | `check-skills.yml` |
| `assets/` | 48042 | `readme-tastecode-dark.webp` |
| `assets/` | 29104 | `readme-tastecode.webp` |
| `assets/` | 61650 | `taste-skill-wordmark-dark.png` |
| `assets/` | 51509 | `taste-skill-wordmark.png` |
| `assets/` | 13296 | `vercel-oss-program-badge.svg` |
| `assets/sponsors/` | 1174 | `imgly-logo.svg` |
| `assets/sponsors/` | 1924 | `interfaces-dev-icon.webp` |
| `assets/sponsors/` | 11486 | `kimi-icon.png` |
| `assets/sponsors/` | 3939 | `reactbits-icon-dark.svg` |
| `assets/sponsors/` | 3937 | `reactbits-icon-light.svg` |
| `assets/sponsors/` | 4382 | `sentdm.png` |
| `assets/sponsors/` | 21326 | `sidrune-ai.png` |
| `assets/sponsors/` | 242 | `vercel-logo.svg` |
| `examples/v2/` | 10491 | `CREDITS.md` |
| `examples/v2/` | 26692 | `coffee-questions.webp` |
| `examples/v2/` | 113142 | `coffee-roast.webp` |
| `examples/v2/` | 29172 | `coffee-storefront.webp` |
| `examples/v2/` | 173606 | `night-dates.webp` |
| `skills/taste-skill/` | 30970 | `SKILL.md` |
| `skills/taste-skill/assets/` | 34981 | `starter.html` |
| `skills/taste-skill/assets/` | 102946 | `system.css` |
| `skills/taste-skill/assets/` | 35746 | `system.js` |
| `skills/taste-skill/assets/backgrounds/` | 42506 | `backgrounds.css` |
| `skills/taste-skill/assets/backgrounds/` | 9077 | `backgrounds.js` |
| `skills/taste-skill/assets/backgrounds/` | 4957 | `check.html` |
| `skills/taste-skill/assets/backgrounds/` | 14581 | `check.mjs` |
| `skills/taste-skill/assets/backgrounds/` | 44365 | `demo.html` |
| `skills/taste-skill/assets/backgrounds/` | 20090 | `index.json` |
| `skills/taste-skill/assets/backgrounds/` | 14327 | `pick.mjs` |
| `skills/taste-skill/assets/components/` | 6569 | `_lab.html` |
| `skills/taste-skill/assets/components/` | 7806 | `base.css` |
| `skills/taste-skill/assets/components/` | 19052 | `index.html` |
| `skills/taste-skill/assets/components/` | 26553 | `shared.js` |
| `skills/taste-skill/assets/components/fx-avatar/` | 3410 | `component.css` |
| `skills/taste-skill/assets/components/fx-avatar/` | 1209 | `component.html` |
| `skills/taste-skill/assets/components/fx-avatar/` | 2756 | `component.js` |
| `skills/taste-skill/assets/components/fx-avatar/` | 870 | `meta.json` |
| `skills/taste-skill/assets/components/fx-band/` | 1416 | `component.css` |
| `skills/taste-skill/assets/components/fx-band/` | 482 | `component.html` |
| `skills/taste-skill/assets/components/fx-band/` | 2752 | `component.js` |
| `skills/taste-skill/assets/components/fx-band/` | 1122 | `meta.json` |
| `skills/taste-skill/assets/components/fx-bars/` | 3531 | `component.css` |
| `skills/taste-skill/assets/components/fx-bars/` | 2325 | `component.html` |
| `skills/taste-skill/assets/components/fx-bars/` | 2252 | `component.js` |
| `skills/taste-skill/assets/components/fx-bars/` | 1232 | `meta.json` |
| `skills/taste-skill/assets/components/fx-button/` | 1634 | `component.css` |
| `skills/taste-skill/assets/components/fx-button/` | 798 | `component.html` |
| `skills/taste-skill/assets/components/fx-button/` | 3093 | `component.js` |
| `skills/taste-skill/assets/components/fx-button/` | 1100 | `meta.json` |
| `skills/taste-skill/assets/components/fx-chart/` | 3437 | `component.css` |
| `skills/taste-skill/assets/components/fx-chart/` | 1184 | `component.html` |
| `skills/taste-skill/assets/components/fx-chart/` | 5385 | `component.js` |
| `skills/taste-skill/assets/components/fx-chart/` | 1283 | `meta.json` |
| `skills/taste-skill/assets/components/fx-dither-object/` | 452 | `component.css` |
| `skills/taste-skill/assets/components/fx-dither-object/` | 177 | `component.html` |
| `skills/taste-skill/assets/components/fx-dither-object/` | 24667 | `component.js` |
| `skills/taste-skill/assets/components/fx-dither-object/` | 2814 | `meta.json` |
| `skills/taste-skill/assets/components/fx-feature-card/` | 10957 | `component.css` |
| `skills/taste-skill/assets/components/fx-feature-card/` | 9150 | `component.html` |
| `skills/taste-skill/assets/components/fx-feature-card/` | 12381 | `component.js` |
| `skills/taste-skill/assets/components/fx-feature-card/` | 3072 | `meta.json` |
| `skills/taste-skill/assets/components/fx-globe/` | 2264 | `component.css` |
| `skills/taste-skill/assets/components/fx-globe/` | 1644 | `component.html` |
| `skills/taste-skill/assets/components/fx-globe/` | 1342 | `component.js` |
| `skills/taste-skill/assets/components/fx-globe/` | 819 | `meta.json` |
| `skills/taste-skill/assets/components/fx-headline/` | 1645 | `component.css` |
| `skills/taste-skill/assets/components/fx-headline/` | 833 | `component.html` |
| `skills/taste-skill/assets/components/fx-headline/` | 742 | `component.js` |
| `skills/taste-skill/assets/components/fx-headline/` | 964 | `meta.json` |
| `skills/taste-skill/assets/components/fx-icon-tiles/` | 1702 | `component.css` |
| `skills/taste-skill/assets/components/fx-icon-tiles/` | 2139 | `component.html` |
| `skills/taste-skill/assets/components/fx-icon-tiles/` | 1464 | `component.js` |
| `skills/taste-skill/assets/components/fx-icon-tiles/` | 922 | `meta.json` |
| `skills/taste-skill/assets/components/fx-logos/` | 2050 | `component.css` |
| `skills/taste-skill/assets/components/fx-logos/` | 12649 | `component.html` |
| `skills/taste-skill/assets/components/fx-logos/` | 1202 | `component.js` |
| `skills/taste-skill/assets/components/fx-logos/` | 1073 | `meta.json` |
| `skills/taste-skill/assets/components/fx-map/` | 25755 | `bake.mjs` |
| `skills/taste-skill/assets/components/fx-map/` | 10887 | `component.css` |
| `skills/taste-skill/assets/components/fx-map/` | 1238 | `component.html` |
| `skills/taste-skill/assets/components/fx-map/` | 14696 | `component.js` |
| `skills/taste-skill/assets/components/fx-map/` | 2626 | `meta.json` |
| `skills/taste-skill/assets/components/fx-map/` | 57014 | `sample-map.json` |
| `skills/taste-skill/assets/components/fx-photo/` | 2046 | `component.css` |
| `skills/taste-skill/assets/components/fx-photo/` | 553 | `component.html` |
| `skills/taste-skill/assets/components/fx-photo/` | 1945 | `component.js` |
| `skills/taste-skill/assets/components/fx-photo/` | 203455 | `meeting-room.jpg` |
| `skills/taste-skill/assets/components/fx-photo/` | 1818 | `meta.json` |
| `skills/taste-skill/assets/components/fx-pricing/` | 3871 | `component.css` |
| `skills/taste-skill/assets/components/fx-pricing/` | 1841 | `component.html` |
| `skills/taste-skill/assets/components/fx-pricing/` | 1539 | `component.js` |
| `skills/taste-skill/assets/components/fx-pricing/` | 971 | `meta.json` |
| `skills/taste-skill/assets/components/fx-progress/` | 3005 | `component.css` |
| `skills/taste-skill/assets/components/fx-progress/` | 2042 | `component.html` |
| `skills/taste-skill/assets/components/fx-progress/` | 4427 | `component.js` |
| `skills/taste-skill/assets/components/fx-progress/` | 1376 | `meta.json` |
| `skills/taste-skill/assets/components/fx-prompt/` | 3175 | `component.css` |
| `skills/taste-skill/assets/components/fx-prompt/` | 1349 | `component.html` |
| `skills/taste-skill/assets/components/fx-prompt/` | 1175 | `component.js` |
| `skills/taste-skill/assets/components/fx-prompt/` | 782 | `meta.json` |
| `skills/taste-skill/assets/components/fx-search/` | 2657 | `component.css` |
| `skills/taste-skill/assets/components/fx-search/` | 1434 | `component.html` |
| `skills/taste-skill/assets/components/fx-search/` | 5009 | `component.js` |
| `skills/taste-skill/assets/components/fx-search/` | 953 | `meta.json` |
| `skills/taste-skill/assets/components/fx-spotlight/` | 1868 | `component.css` |
| `skills/taste-skill/assets/components/fx-spotlight/` | 1596 | `component.html` |
| `skills/taste-skill/assets/components/fx-spotlight/` | 4127 | `component.js` |
| `skills/taste-skill/assets/components/fx-spotlight/` | 1080 | `meta.json` |
| `skills/taste-skill/assets/components/fx-stat/` | 1619 | `component.css` |
| `skills/taste-skill/assets/components/fx-stat/` | 694 | `component.html` |
| `skills/taste-skill/assets/components/fx-stat/` | 1195 | `component.js` |
| `skills/taste-skill/assets/components/fx-stat/` | 1083 | `meta.json` |
| `skills/taste-skill/assets/components/fx-tabs/` | 5102 | `component.css` |
| `skills/taste-skill/assets/components/fx-tabs/` | 2944 | `component.html` |
| `skills/taste-skill/assets/components/fx-tabs/` | 3207 | `component.js` |
| `skills/taste-skill/assets/components/fx-tabs/` | 1189 | `meta.json` |
| `skills/taste-skill/assets/diagrams/` | 11678 | `demo.html` |
| `skills/taste-skill/assets/diagrams/` | 26156 | `diagram.css` |
| `skills/taste-skill/assets/diagrams/` | 91290 | `diagram.js` |
| `skills/taste-skill/assets/diagrams/` | 11453 | `lab.html` |
| `skills/taste-skill/assets/diagrams/` | 609 | `mount.js` |
| `skills/taste-skill/assets/diagrams/` | 28505 | `presets.json` |
| `skills/taste-skill/assets/effects/` | 10038 | `README.md` |
| `skills/taste-skill/assets/effects/` | 41441 | `fx.js` |
| `skills/taste-skill/assets/effects/` | 38294 | `gallery.html` |
| `skills/taste-skill/assets/effects/` | 37570 | `index.json` |
| `skills/taste-skill/assets/effects/` | 31761 | `lab.html` |
| `skills/taste-skill/assets/effects/` | 10372 | `pick.js` |
| `skills/taste-skill/assets/effects/ascii-shade/` | 18718 | `effect.js` |
| `skills/taste-skill/assets/effects/ascii-shade/` | 372 | `meta.json` |
| `skills/taste-skill/assets/effects/aurora-curtains/` | 9384 | `effect.js` |
| `skills/taste-skill/assets/effects/aurora-curtains/` | 361 | `meta.json` |
| `skills/taste-skill/assets/effects/bayer-dither/` | 6074 | `effect.js` |
| `skills/taste-skill/assets/effects/bayer-dither/` | 311 | `meta.json` |
| `skills/taste-skill/assets/effects/caustics/` | 7451 | `effect.js` |
| `skills/taste-skill/assets/effects/caustics/` | 357 | `meta.json` |
| `skills/taste-skill/assets/effects/contour-lines/` | 8439 | `effect.js` |
| `skills/taste-skill/assets/effects/contour-lines/` | 358 | `meta.json` |
| `skills/taste-skill/assets/effects/dot-terrain/` | 9433 | `effect.js` |
| `skills/taste-skill/assets/effects/dot-terrain/` | 332 | `meta.json` |
| `skills/taste-skill/assets/effects/dotted-globe/` | 54158 | `effect.js` |
| `skills/taste-skill/assets/effects/dotted-globe/` | 546 | `meta.json` |
| `skills/taste-skill/assets/effects/duotone-grade/` | 34468 | `effect.js` |
| `skills/taste-skill/assets/effects/duotone-grade/` | 395 | `meta.json` |
| `skills/taste-skill/assets/effects/edge-glow/` | 10882 | `effect.js` |
| `skills/taste-skill/assets/effects/edge-glow/` | 427 | `meta.json` |
| `skills/taste-skill/assets/effects/film-light-leak/` | 12478 | `effect.js` |
| `skills/taste-skill/assets/effects/film-light-leak/` | 343 | `meta.json` |
| `skills/taste-skill/assets/effects/fluted-glass/` | 9891 | `effect.js` |
| `skills/taste-skill/assets/effects/fluted-glass/` | 305 | `meta.json` |
| `skills/taste-skill/assets/effects/god-rays/` | 9346 | `effect.js` |
| `skills/taste-skill/assets/effects/god-rays/` | 318 | `meta.json` |
| `skills/taste-skill/assets/effects/gradient-mesh/` | 11268 | `effect.js` |
| `skills/taste-skill/assets/effects/gradient-mesh/` | 334 | `meta.json` |
| `skills/taste-skill/assets/effects/grain-gradient/` | 8298 | `effect.js` |
| `skills/taste-skill/assets/effects/grain-gradient/` | 311 | `meta.json` |
| `skills/taste-skill/assets/effects/grid-pulse/` | 19009 | `effect.js` |
| `skills/taste-skill/assets/effects/grid-pulse/` | 343 | `meta.json` |
| `skills/taste-skill/assets/effects/halftone-screen/` | 13094 | `effect.js` |
| `skills/taste-skill/assets/effects/halftone-screen/` | 342 | `meta.json` |
| `skills/taste-skill/assets/effects/line-engraving/` | 12726 | `effect.js` |
| `skills/taste-skill/assets/effects/line-engraving/` | 343 | `meta.json` |
| `skills/taste-skill/assets/effects/orb-sphere/` | 14559 | `effect.js` |
| `skills/taste-skill/assets/effects/orb-sphere/` | 366 | `meta.json` |
| `skills/taste-skill/assets/effects/painterly-landscape/` | 13154 | `effect.js` |
| `skills/taste-skill/assets/effects/painterly-landscape/` | 364 | `meta.json` |
| `skills/taste-skill/assets/effects/prism-dispersion/` | 9795 | `effect.js` |
| `skills/taste-skill/assets/effects/prism-dispersion/` | 331 | `meta.json` |
| `skills/taste-skill/assets/effects/ridgeline/` | 19674 | `effect.js` |
| `skills/taste-skill/assets/effects/ridgeline/` | 460 | `meta.json` |
| `skills/taste-skill/assets/effects/ruled-grounds/` | 11572 | `effect.js` |
| `skills/taste-skill/assets/effects/ruled-grounds/` | 357 | `meta.json` |
| `skills/taste-skill/assets/effects/silk-folds/` | 10636 | `effect.js` |
| `skills/taste-skill/assets/effects/silk-folds/` | 348 | `meta.json` |
| `skills/taste-skill/assets/effects/soft-light-bars/` | 21593 | `effect.js` |
| `skills/taste-skill/assets/effects/soft-light-bars/` | 391 | `meta.json` |
| `skills/taste-skill/assets/effects/spotlight-cone/` | 7451 | `effect.js` |
| `skills/taste-skill/assets/effects/spotlight-cone/` | 349 | `meta.json` |
| `skills/taste-skill/assets/icons/` | 486460 | `demo.html` |
| `skills/taste-skill/assets/icons/` | 13971 | `icon.css` |
| `skills/taste-skill/assets/icons/` | 125353 | `index.json` |
| `skills/taste-skill/assets/layout/` | 16184 | `check.mjs` |
| `skills/taste-skill/assets/layout/` | 9730 | `deal.mjs` |
| `skills/taste-skill/assets/layout/` | 5868 | `demo.css` |
| `skills/taste-skill/assets/layout/` | 9773 | `fonts.html` |
| `skills/taste-skill/assets/layout/` | 16795 | `hero-centred.html` |
| `skills/taste-skill/assets/layout/` | 16062 | `hero-collage.html` |
| `skills/taste-skill/assets/layout/` | 8308 | `hero-editorial.html` |
| `skills/taste-skill/assets/layout/` | 7966 | `hero-film.html` |
| `skills/taste-skill/assets/layout/` | 7951 | `hero-photo.html` |
| `skills/taste-skill/assets/layout/` | 6890 | `hero-place.html` |
| `skills/taste-skill/assets/layout/` | 7877 | `hero-product.html` |
| `skills/taste-skill/assets/layout/` | 7971 | `hero-split.html` |
| `skills/taste-skill/assets/layout/` | 8580 | `hero-statement.html` |
| `skills/taste-skill/assets/layout/` | 14590 | `hero-triptych.html` |
| `skills/taste-skill/assets/layout/` | 10323 | `hero-word.html` |
| `skills/taste-skill/assets/layout/` | 37569 | `heroes.json` |
| `skills/taste-skill/assets/layout/` | 21651 | `layout-check.js` |
| `skills/taste-skill/assets/layout/` | 45504 | `layout.css` |
| `skills/taste-skill/assets/layout/` | 15129 | `layout.js` |
| `skills/taste-skill/assets/layout/img/` | 8365 | `credits.json` |
| `skills/taste-skill/assets/layout/img/` | 159463 | `photo-1068.jpg` |
| `skills/taste-skill/assets/layout/img/` | 219645 | `photo-1081.jpg` |
| `skills/taste-skill/assets/layout/img/` | 95992 | `photo-465.jpg` |
| `skills/taste-skill/assets/layout/img/` | 340249 | `photo-559.jpg` |
| `skills/taste-skill/assets/layout/img/` | 62206 | `photo-855.jpg` |
| `skills/taste-skill/assets/layout/img/` | 148765 | `photo-887.jpg` |
| `skills/taste-skill/assets/layout/img/` | 141810 | `photo-949.jpg` |
| `skills/taste-skill/assets/layout/img/` | 29012 | `photo-954.jpg` |
| `skills/taste-skill/assets/layout/img/` | 76590 | `photo-beans-hand.jpg` |
| `skills/taste-skill/assets/layout/img/` | 307029 | `photo-c166.jpg` |
| `skills/taste-skill/assets/layout/img/` | 438661 | `photo-c400.jpg` |
| `skills/taste-skill/assets/layout/img/` | 164902 | `photo-c7.jpg` |
| `skills/taste-skill/assets/layout/img/` | 248908 | `photo-c70.jpg` |
| `skills/taste-skill/assets/layout/img/` | 178191 | `photo-c8.jpg` |
| `skills/taste-skill/assets/layout/img/` | 388652 | `photo-c823.jpg` |
| `skills/taste-skill/assets/layout/img/` | 258281 | `photo-c96.jpg` |
| `skills/taste-skill/assets/layout/img/` | 516491 | `photo-d534.jpg` |
| `skills/taste-skill/assets/layout/img/` | 523701 | `photo-d540.jpg` |
| `skills/taste-skill/assets/layout/img/` | 257459 | `photo-d88.jpg` |
| `skills/taste-skill/assets/layout/img/` | 135132 | `photo-m61660576.jpg` |
| `skills/taste-skill/assets/layout/img/` | 191833 | `photo-m61757972.jpg` |
| `skills/taste-skill/assets/moments/` | 8326 | `gallery.html` |
| `skills/taste-skill/assets/moments/` | 21865 | `index.json` |
| `skills/taste-skill/assets/moments/` | 10768 | `lib.js` |
| `skills/taste-skill/assets/moments/` | 6101 | `moments.js` |
| `skills/taste-skill/assets/moments/_demo/` | 1326 | `credits.json` |
| `skills/taste-skill/assets/moments/_demo/` | 7011 | `demo.css` |
| `skills/taste-skill/assets/moments/_demo/` | 1870 | `in-card.html` |
| `skills/taste-skill/assets/moments/_demo/` | 10578 | `in-page-service.html` |
| `skills/taste-skill/assets/moments/_demo/` | 9847 | `in-page.html` |
| `skills/taste-skill/assets/moments/_demo/` | 102277 | `photo-1049-tall.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 152098 | `photo-1049.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 139715 | `photo-1081.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 492281 | `photo-640.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 305162 | `photo-702-tall.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 441407 | `photo-702.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 92222 | `photo-855.jpg` |
| `skills/taste-skill/assets/moments/_demo/` | 279738 | `photo-887.jpg` |
| `skills/taste-skill/assets/moments/closing-lift/` | 4357 | `demo.html` |
| `skills/taste-skill/assets/moments/closing-lift/` | 1313 | `meta.json` |
| `skills/taste-skill/assets/moments/closing-lift/` | 2378 | `moment.css` |
| `skills/taste-skill/assets/moments/closing-lift/` | 2939 | `moment.js` |
| `skills/taste-skill/assets/moments/counter-rolls/` | 5437 | `demo.html` |
| `skills/taste-skill/assets/moments/counter-rolls/` | 911 | `meta.json` |
| `skills/taste-skill/assets/moments/counter-rolls/` | 718 | `moment.css` |
| `skills/taste-skill/assets/moments/counter-rolls/` | 3400 | `moment.js` |
| `skills/taste-skill/assets/moments/cursor-spotlight/` | 4401 | `demo.html` |
| `skills/taste-skill/assets/moments/cursor-spotlight/` | 1254 | `meta.json` |
| `skills/taste-skill/assets/moments/cursor-spotlight/` | 1183 | `moment.css` |
| `skills/taste-skill/assets/moments/cursor-spotlight/` | 2286 | `moment.js` |
| `skills/taste-skill/assets/moments/giant-type-pass/` | 3651 | `demo.html` |
| `skills/taste-skill/assets/moments/giant-type-pass/` | 1057 | `meta.json` |
| `skills/taste-skill/assets/moments/giant-type-pass/` | 1571 | `moment.css` |
| `skills/taste-skill/assets/moments/giant-type-pass/` | 2089 | `moment.js` |
| `skills/taste-skill/assets/moments/headline-arrives/` | 4004 | `demo.html` |
| `skills/taste-skill/assets/moments/headline-arrives/` | 1071 | `meta.json` |
| `skills/taste-skill/assets/moments/headline-arrives/` | 1663 | `moment.css` |
| `skills/taste-skill/assets/moments/headline-arrives/` | 2699 | `moment.js` |
| `skills/taste-skill/assets/moments/iris-opens/` | 5029 | `demo.html` |
| `skills/taste-skill/assets/moments/iris-opens/` | 1293 | `meta.json` |
| `skills/taste-skill/assets/moments/iris-opens/` | 1997 | `moment.css` |
| `skills/taste-skill/assets/moments/iris-opens/` | 4691 | `moment.js` |
| `skills/taste-skill/assets/moments/letters-assemble/` | 4315 | `demo.html` |
| `skills/taste-skill/assets/moments/letters-assemble/` | 1025 | `meta.json` |
| `skills/taste-skill/assets/moments/letters-assemble/` | 1084 | `moment.css` |
| `skills/taste-skill/assets/moments/letters-assemble/` | 3019 | `moment.js` |
| `skills/taste-skill/assets/moments/line-carries-colour/` | 4487 | `demo.html` |
| `skills/taste-skill/assets/moments/line-carries-colour/` | 1382 | `meta.json` |
| `skills/taste-skill/assets/moments/line-carries-colour/` | 1683 | `moment.css` |
| `skills/taste-skill/assets/moments/line-carries-colour/` | 4048 | `moment.js` |
| `skills/taste-skill/assets/moments/lines-rise/` | 5218 | `demo.html` |
| `skills/taste-skill/assets/moments/lines-rise/` | 984 | `meta.json` |
| `skills/taste-skill/assets/moments/lines-rise/` | 1316 | `moment.css` |
| `skills/taste-skill/assets/moments/lines-rise/` | 3121 | `moment.js` |
| `skills/taste-skill/assets/moments/liquid-hover/` | 3380 | `demo.html` |
| `skills/taste-skill/assets/moments/liquid-hover/` | 1443 | `meta.json` |
| `skills/taste-skill/assets/moments/liquid-hover/` | 457 | `moment.css` |
| `skills/taste-skill/assets/moments/liquid-hover/` | 13350 | `moment.js` |
| `skills/taste-skill/assets/moments/liquid-type/` | 3099 | `demo.html` |
| `skills/taste-skill/assets/moments/liquid-type/` | 1058 | `meta.json` |
| `skills/taste-skill/assets/moments/liquid-type/` | 462 | `moment.css` |
| `skills/taste-skill/assets/moments/liquid-type/` | 4205 | `moment.js` |
| `skills/taste-skill/assets/moments/marquee-row/` | 4433 | `demo.html` |
| `skills/taste-skill/assets/moments/marquee-row/` | 865 | `meta.json` |
| `skills/taste-skill/assets/moments/marquee-row/` | 2015 | `moment.css` |
| `skills/taste-skill/assets/moments/marquee-row/` | 2459 | `moment.js` |
| `skills/taste-skill/assets/moments/photo-chapters/` | 5256 | `demo.html` |
| `skills/taste-skill/assets/moments/photo-chapters/` | 1884 | `meta.json` |
| `skills/taste-skill/assets/moments/photo-chapters/` | 6298 | `moment.css` |
| `skills/taste-skill/assets/moments/photo-chapters/` | 6202 | `moment.js` |
| `skills/taste-skill/assets/moments/picture-develops/` | 3986 | `demo-film.html` |
| `skills/taste-skill/assets/moments/picture-develops/` | 4292 | `demo.html` |
| `skills/taste-skill/assets/moments/picture-develops/` | 1412 | `meta.json` |
| `skills/taste-skill/assets/moments/picture-develops/` | 1946 | `moment.css` |
| `skills/taste-skill/assets/moments/picture-develops/` | 9433 | `moment.js` |
| `skills/taste-skill/assets/moments/pinned-chapters/` | 5545 | `demo.html` |
| `skills/taste-skill/assets/moments/pinned-chapters/` | 1279 | `meta.json` |
| `skills/taste-skill/assets/moments/pinned-chapters/` | 7029 | `moment.css` |
| `skills/taste-skill/assets/moments/pinned-chapters/` | 4338 | `moment.js` |
| `skills/taste-skill/assets/moments/window-parallax/` | 3859 | `demo.html` |
| `skills/taste-skill/assets/moments/window-parallax/` | 913 | `meta.json` |
| `skills/taste-skill/assets/moments/window-parallax/` | 591 | `moment.css` |
| `skills/taste-skill/assets/moments/window-parallax/` | 1230 | `moment.js` |
| `skills/taste-skill/assets/moments/word-highlight/` | 4605 | `demo.html` |
| `skills/taste-skill/assets/moments/word-highlight/` | 1031 | `meta.json` |
| `skills/taste-skill/assets/moments/word-highlight/` | 849 | `moment.css` |
| `skills/taste-skill/assets/moments/word-highlight/` | 2002 | `moment.js` |
| `skills/taste-skill/assets/moments/word-rotate/` | 4646 | `demo.html` |
| `skills/taste-skill/assets/moments/word-rotate/` | 948 | `meta.json` |
| `skills/taste-skill/assets/moments/word-rotate/` | 906 | `moment.css` |
| `skills/taste-skill/assets/moments/word-rotate/` | 2222 | `moment.js` |
| `skills/taste-skill/assets/motion/` | 1479 | `_hover-test.html` |
| `skills/taste-skill/assets/motion/` | 34953 | `demo.html` |
| `skills/taste-skill/assets/motion/` | 2793 | `meta.json` |
| `skills/taste-skill/assets/motion/` | 25717 | `motion.css` |
| `skills/taste-skill/assets/motion/` | 23325 | `motion.js` |
| `skills/taste-skill/assets/objects/` | 46488 | `index.html` |
| `skills/taste-skill/assets/objects/_print-core/` | 10330 | `README.md` |
| `skills/taste-skill/assets/objects/_print-core/` | 3994 | `auto.js` |
| `skills/taste-skill/assets/objects/_print-core/` | 4131 | `blank-ground.html` |
| `skills/taste-skill/assets/objects/_print-core/` | 11249 | `cards.html` |
| `skills/taste-skill/assets/objects/_print-core/` | 2929 | `demo.css` |
| `skills/taste-skill/assets/objects/_print-core/` | 4048 | `demo.js` |
| `skills/taste-skill/assets/objects/_print-core/` | 4115 | `index.json` |
| `skills/taste-skill/assets/objects/_print-core/` | 3219 | `lint-glsl.mjs` |
| `skills/taste-skill/assets/objects/_print-core/` | 4854 | `make-fallbacks.html` |
| `skills/taste-skill/assets/objects/_print-core/` | 103417 | `print3d.js` |
| `skills/taste-skill/assets/objects/_scenes/` | 9874 | `README.md` |
| `skills/taste-skill/assets/objects/_scenes/` | 4131 | `auto.js` |
| `skills/taste-skill/assets/objects/_scenes/` | 5122 | `demo.css` |
| `skills/taste-skill/assets/objects/_scenes/` | 4960 | `demo.js` |
| `skills/taste-skill/assets/objects/_scenes/` | 3740 | `index.json` |
| `skills/taste-skill/assets/objects/_scenes/` | 48885 | `kit.js` |
| `skills/taste-skill/assets/objects/_scenes/` | 4427 | `lint-glsl.mjs` |
| `skills/taste-skill/assets/objects/dither-sequence/` | 2550 | `demo.html` |
| `skills/taste-skill/assets/objects/dither-sequence/` | 4118 | `meta.json` |
| `skills/taste-skill/assets/objects/dither-sequence/` | 13345 | `object.js` |
| `skills/taste-skill/assets/objects/dot-object/` | 2425 | `demo.html` |
| `skills/taste-skill/assets/objects/dot-object/` | 3165 | `meta.json` |
| `skills/taste-skill/assets/objects/dot-object/` | 15506 | `object.js` |
| `skills/taste-skill/assets/objects/exploded-layers/` | 2017 | `demo.html` |
| `skills/taste-skill/assets/objects/exploded-layers/` | 2858 | `meta.json` |
| `skills/taste-skill/assets/objects/exploded-layers/` | 15607 | `object.js` |
| `skills/taste-skill/assets/objects/photo-dither/` | 1155 | `demo.html` |
| `skills/taste-skill/assets/objects/photo-dither/` | 4489 | `meta.json` |
| `skills/taste-skill/assets/objects/photo-dither/` | 7641 | `object.js` |
| `skills/taste-skill/assets/objects/photo-engraving/` | 1183 | `demo.html` |
| `skills/taste-skill/assets/objects/photo-engraving/` | 4273 | `meta.json` |
| `skills/taste-skill/assets/objects/photo-engraving/` | 6764 | `object.js` |
| `skills/taste-skill/assets/objects/photo-halftone/` | 1216 | `demo.html` |
| `skills/taste-skill/assets/objects/photo-halftone/` | 4405 | `meta.json` |
| `skills/taste-skill/assets/objects/photo-halftone/` | 6343 | `object.js` |
| `skills/taste-skill/assets/objects/photo-kit/` | 5263 | `README.md` |
| `skills/taste-skill/assets/objects/photo-kit/` | 4890 | `demo.css` |
| `skills/taste-skill/assets/objects/photo-kit/` | 4231 | `demo.js` |
| `skills/taste-skill/assets/objects/photo-kit/` | 59095 | `photo.js` |
| `skills/taste-skill/assets/objects/photo-kit/` | 2863 | `photos.json` |
| `skills/taste-skill/assets/objects/photo-kit/photos/` | 202086 | `concrete.jpg` |
| `skills/taste-skill/assets/objects/photo-kit/photos/` | 257459 | `lamp.jpg` |
| `skills/taste-skill/assets/objects/photo-kit/photos/` | 114947 | `platform.jpg` |
| `skills/taste-skill/assets/objects/photo-kit/photos/` | 203455 | `room.jpg` |
| `skills/taste-skill/assets/objects/print-cards/` | 392 | `demo.html` |
| `skills/taste-skill/assets/objects/print-cards/` | 36157 | `fallback-dark.png` |
| `skills/taste-skill/assets/objects/print-cards/` | 127037 | `fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/print-cards/` | 121604 | `fallback-render.png` |
| `skills/taste-skill/assets/objects/print-cards/` | 43216 | `fallback.png` |
| `skills/taste-skill/assets/objects/print-cards/` | 5621 | `meta.json` |
| `skills/taste-skill/assets/objects/print-cards/` | 5933 | `object.js` |
| `skills/taste-skill/assets/objects/print-cup/` | 393 | `demo.html` |
| `skills/taste-skill/assets/objects/print-cup/` | 98903 | `fallback-dark.png` |
| `skills/taste-skill/assets/objects/print-cup/` | 200477 | `fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/print-cup/` | 187508 | `fallback-render.png` |
| `skills/taste-skill/assets/objects/print-cup/` | 108553 | `fallback.png` |
| `skills/taste-skill/assets/objects/print-cup/` | 5518 | `meta.json` |
| `skills/taste-skill/assets/objects/print-cup/` | 6617 | `object.js` |
| `skills/taste-skill/assets/objects/print-globe/` | 389 | `demo.html` |
| `skills/taste-skill/assets/objects/print-globe/` | 101520 | `fallback-dark.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 212491 | `fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 212119 | `fallback-render-sea-dark.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 217246 | `fallback-render-sea.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 216477 | `fallback-render.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 100255 | `fallback-sea-dark.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 107585 | `fallback-sea.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 109210 | `fallback.png` |
| `skills/taste-skill/assets/objects/print-globe/` | 11096 | `land.js` |
| `skills/taste-skill/assets/objects/print-globe/` | 5886 | `meta.json` |
| `skills/taste-skill/assets/objects/print-globe/` | 9124 | `object.js` |
| `skills/taste-skill/assets/objects/print-lamp/` | 388 | `demo.html` |
| `skills/taste-skill/assets/objects/print-lamp/` | 44123 | `fallback-dark.png` |
| `skills/taste-skill/assets/objects/print-lamp/` | 137425 | `fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/print-lamp/` | 135318 | `fallback-render.png` |
| `skills/taste-skill/assets/objects/print-lamp/` | 55039 | `fallback.png` |
| `skills/taste-skill/assets/objects/print-lamp/` | 5920 | `meta.json` |
| `skills/taste-skill/assets/objects/print-lamp/` | 12073 | `object.js` |
| `skills/taste-skill/assets/objects/print-wheel/` | 392 | `demo.html` |
| `skills/taste-skill/assets/objects/print-wheel/` | 82016 | `fallback-dark.png` |
| `skills/taste-skill/assets/objects/print-wheel/` | 292781 | `fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/print-wheel/` | 295097 | `fallback-render.png` |
| `skills/taste-skill/assets/objects/print-wheel/` | 103486 | `fallback.png` |
| `skills/taste-skill/assets/objects/print-wheel/` | 5655 | `meta.json` |
| `skills/taste-skill/assets/objects/print-wheel/` | 7374 | `object.js` |
| `skills/taste-skill/assets/objects/product-render/` | 17637 | `README.md` |
| `skills/taste-skill/assets/objects/product-render/` | 7704 | `auto.js` |
| `skills/taste-skill/assets/objects/product-render/` | 90011 | `build.js` |
| `skills/taste-skill/assets/objects/product-render/` | 4629 | `demo.html` |
| `skills/taste-skill/assets/objects/product-render/` | 17822 | `make-posters.html` |
| `skills/taste-skill/assets/objects/product-render/` | 12765 | `make-posters.mjs` |
| `skills/taste-skill/assets/objects/product-render/` | 10034 | `views.html` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 59576 | `city-bike.fallback-dark.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 265301 | `city-bike.fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 267032 | `city-bike.fallback-render.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 82387 | `city-bike.fallback.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 11168 | `city-bike.json` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 56866 | `desk-lamp.fallback-dark.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 116243 | `desk-lamp.fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 115552 | `desk-lamp.fallback-render.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 54948 | `desk-lamp.fallback.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 4481 | `desk-lamp.json` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 42015 | `robot-arm.fallback-dark.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 116008 | `robot-arm.fallback-render-dark.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 109478 | `robot-arm.fallback-render.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 62050 | `robot-arm.fallback.png` |
| `skills/taste-skill/assets/objects/product-render/specs/` | 6216 | `robot-arm.json` |
| `skills/taste-skill/assets/objects/product-turntable/` | 1523 | `demo.html` |
| `skills/taste-skill/assets/objects/product-turntable/` | 9784 | `fallback-camera-dark.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 9675 | `fallback-camera-light.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 6771 | `fallback-chair-dark.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 6855 | `fallback-chair-light.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 10167 | `fallback-cup-dark.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 9701 | `fallback-cup-light.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 7736 | `fallback-speaker-dark.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 7927 | `fallback-speaker-light.png` |
| `skills/taste-skill/assets/objects/product-turntable/` | 2195 | `make-fallbacks.html` |
| `skills/taste-skill/assets/objects/product-turntable/` | 2734 | `meta.json` |
| `skills/taste-skill/assets/objects/product-turntable/` | 21045 | `object.js` |
| `skills/taste-skill/assets/objects/split-reveal/` | 2046 | `demo.html` |
| `skills/taste-skill/assets/objects/split-reveal/` | 3096 | `meta.json` |
| `skills/taste-skill/assets/objects/split-reveal/` | 12082 | `object.js` |
| `skills/taste-skill/assets/photos/` | 360290 | `photos.json` |
| `skills/taste-skill/assets/scenes/` | 22606 | `index.json` |
| `skills/taste-skill/assets/scenes/` | 20927 | `lib.js` |
| `skills/taste-skill/assets/scenes/` | 2650 | `print.js` |
| `skills/taste-skill/assets/scenes/` | 4011 | `scenes.css` |
| `skills/taste-skill/assets/scenes/` | 4293 | `scenes.js` |
| `skills/taste-skill/assets/scenes/_demo/` | 315913 | `cards.png` |
| `skills/taste-skill/assets/scenes/_demo/` | 202086 | `concrete.jpg` |
| `skills/taste-skill/assets/scenes/_demo/` | 2979 | `credits.json` |
| `skills/taste-skill/assets/scenes/_demo/` | 5566 | `demo.css` |
| `skills/taste-skill/assets/scenes/_demo/` | 383506 | `globe.png` |
| `skills/taste-skill/assets/scenes/_demo/` | 6620 | `make-object.html` |
| `skills/taste-skill/assets/scenes/_demo/` | 2179 | `make-still.html` |
| `skills/taste-skill/assets/scenes/_demo/` | 202511 | `photo-507.jpg` |
| `skills/taste-skill/assets/scenes/_demo/` | 115540 | `photo-809.jpg` |
| `skills/taste-skill/assets/scenes/_demo/` | 870090 | `photo-c391.jpg` |
| `skills/taste-skill/assets/scenes/_demo/` | 682553 | `photo-c393.jpg` |
| `skills/taste-skill/assets/scenes/_demo/` | 25332 | `shoot.mjs` |
| `skills/taste-skill/assets/scenes/descend-through-weather/` | 3936 | `demo.html` |
| `skills/taste-skill/assets/scenes/descend-through-weather/` | 2356 | `meta.json` |
| `skills/taste-skill/assets/scenes/descend-through-weather/` | 6122 | `scene.css` |
| `skills/taste-skill/assets/scenes/descend-through-weather/` | 9507 | `scene.js` |
| `skills/taste-skill/assets/scenes/dot-becomes-the-full-stop/` | 5316 | `demo.html` |
| `skills/taste-skill/assets/scenes/dot-becomes-the-full-stop/` | 1444 | `meta.json` |
| `skills/taste-skill/assets/scenes/dot-becomes-the-full-stop/` | 2630 | `scene.css` |
| `skills/taste-skill/assets/scenes/dot-becomes-the-full-stop/` | 6169 | `scene.js` |
| `skills/taste-skill/assets/scenes/fixed-hero-object/` | 5230 | `demo.html` |
| `skills/taste-skill/assets/scenes/fixed-hero-object/` | 2151 | `meta.json` |
| `skills/taste-skill/assets/scenes/fixed-hero-object/` | 6059 | `scene.css` |
| `skills/taste-skill/assets/scenes/fixed-hero-object/` | 5658 | `scene.js` |
| `skills/taste-skill/assets/scenes/fly-into-the-shape/` | 6286 | `demo.html` |
| `skills/taste-skill/assets/scenes/fly-into-the-shape/` | 1899 | `meta.json` |
| `skills/taste-skill/assets/scenes/fly-into-the-shape/` | 4385 | `scene.css` |
| `skills/taste-skill/assets/scenes/fly-into-the-shape/` | 6578 | `scene.js` |
| `skills/taste-skill/assets/scenes/letter-bar-floods-the-ground/` | 5527 | `demo.html` |
| `skills/taste-skill/assets/scenes/letter-bar-floods-the-ground/` | 1813 | `meta.json` |
| `skills/taste-skill/assets/scenes/letter-bar-floods-the-ground/` | 4252 | `scene.css` |
| `skills/taste-skill/assets/scenes/letter-bar-floods-the-ground/` | 6588 | `scene.js` |
| `skills/taste-skill/assets/scenes/letter-physics/` | 5322 | `demo.html` |
| `skills/taste-skill/assets/scenes/letter-physics/` | 1758 | `meta.json` |
| `skills/taste-skill/assets/scenes/letter-physics/` | 4184 | `scene.css` |
| `skills/taste-skill/assets/scenes/letter-physics/` | 4832 | `scene.js` |
| `skills/taste-skill/assets/scenes/object-through-giant-type/` | 4756 | `demo.html` |
| `skills/taste-skill/assets/scenes/object-through-giant-type/` | 1994 | `meta.json` |
| `skills/taste-skill/assets/scenes/object-through-giant-type/` | 3499 | `scene.css` |
| `skills/taste-skill/assets/scenes/object-through-giant-type/` | 6869 | `scene.js` |
| `skills/taste-skill/assets/scenes/parts-lock-into-the-whole/` | 8471 | `demo.html` |
| `skills/taste-skill/assets/scenes/parts-lock-into-the-whole/` | 1775 | `meta.json` |
| `skills/taste-skill/assets/scenes/parts-lock-into-the-whole/` | 4984 | `scene.css` |
| `skills/taste-skill/assets/scenes/parts-lock-into-the-whole/` | 6978 | `scene.js` |
| `skills/taste-skill/assets/scenes/powers-of-ten-pullback/` | 6050 | `demo.html` |
| `skills/taste-skill/assets/scenes/powers-of-ten-pullback/` | 1903 | `meta.json` |
| `skills/taste-skill/assets/scenes/powers-of-ten-pullback/` | 5480 | `scene.css` |
| `skills/taste-skill/assets/scenes/powers-of-ten-pullback/` | 3703 | `scene.js` |
| `skills/taste-skill/assets/scenes/product-assembles-into-its-action/` | 7582 | `demo.html` |
| `skills/taste-skill/assets/scenes/product-assembles-into-its-action/` | 1986 | `meta.json` |
| `skills/taste-skill/assets/scenes/product-assembles-into-its-action/` | 5890 | `scene.css` |
| `skills/taste-skill/assets/scenes/product-assembles-into-its-action/` | 8880 | `scene.js` |
| `skills/taste-skill/assets/scenes/shaped-window-over-fixed-world/` | 3786 | `demo.html` |
| `skills/taste-skill/assets/scenes/shaped-window-over-fixed-world/` | 2079 | `meta.json` |
| `skills/taste-skill/assets/scenes/shaped-window-over-fixed-world/` | 4960 | `scene.css` |
| `skills/taste-skill/assets/scenes/shaped-window-over-fixed-world/` | 6924 | `scene.js` |
| `skills/taste-skill/assets/ui/` | 16111 | `base.css` |
| `skills/taste-skill/assets/ui/` | 22135 | `cards.css` |
| `skills/taste-skill/assets/ui/` | 53578 | `cards.html` |
| `skills/taste-skill/assets/ui/` | 8740 | `index.html` |
| `skills/taste-skill/assets/ui/` | 31682 | `index.json` |
| `skills/taste-skill/assets/ui/` | 40405 | `ui.js` |
| `skills/taste-skill/assets/ui/_lab/` | 4078 | `build-index.mjs` |
| `skills/taste-skill/assets/ui/_lab/` | 8891 | `loops.html` |
| `skills/taste-skill/assets/ui/_lab/` | 4862 | `object-card.html` |
| `skills/taste-skill/assets/ui/_lab/` | 3186 | `selftest.html` |
| `skills/taste-skill/assets/ui/apps/` | 3074 | `fragment.css` |
| `skills/taste-skill/assets/ui/apps/` | 2397 | `fragment.html` |
| `skills/taste-skill/assets/ui/apps/` | 2032 | `fragment.js` |
| `skills/taste-skill/assets/ui/apps/` | 1683 | `meta.json` |
| `skills/taste-skill/assets/ui/calendar/` | 4494 | `fragment.css` |
| `skills/taste-skill/assets/ui/calendar/` | 3483 | `fragment.html` |
| `skills/taste-skill/assets/ui/calendar/` | 3496 | `fragment.js` |
| `skills/taste-skill/assets/ui/calendar/` | 957 | `meta.json` |
| `skills/taste-skill/assets/ui/chat/` | 4044 | `fragment.css` |
| `skills/taste-skill/assets/ui/chat/` | 5122 | `fragment.html` |
| `skills/taste-skill/assets/ui/chat/` | 2962 | `fragment.js` |
| `skills/taste-skill/assets/ui/chat/` | 1117 | `meta.json` |
| `skills/taste-skill/assets/ui/checklist/` | 2230 | `fragment.css` |
| `skills/taste-skill/assets/ui/checklist/` | 1326 | `fragment.html` |
| `skills/taste-skill/assets/ui/checklist/` | 1533 | `fragment.js` |
| `skills/taste-skill/assets/ui/checklist/` | 901 | `meta.json` |
| `skills/taste-skill/assets/ui/code/` | 2687 | `fragment.css` |
| `skills/taste-skill/assets/ui/code/` | 1606 | `fragment.html` |
| `skills/taste-skill/assets/ui/code/` | 1791 | `fragment.js` |
| `skills/taste-skill/assets/ui/code/` | 857 | `meta.json` |
| `skills/taste-skill/assets/ui/cursor/` | 2410 | `fragment.css` |
| `skills/taste-skill/assets/ui/cursor/` | 1695 | `fragment.html` |
| `skills/taste-skill/assets/ui/cursor/` | 3306 | `fragment.js` |
| `skills/taste-skill/assets/ui/cursor/` | 1189 | `meta.json` |
| `skills/taste-skill/assets/ui/diff-review/` | 14283 | `fragment.css` |
| `skills/taste-skill/assets/ui/diff-review/` | 5067 | `fragment.html` |
| `skills/taste-skill/assets/ui/diff-review/` | 2507 | `fragment.js` |
| `skills/taste-skill/assets/ui/diff-review/` | 3991 | `meta.json` |
| `skills/taste-skill/assets/ui/doc/` | 2486 | `fragment.css` |
| `skills/taste-skill/assets/ui/doc/` | 1267 | `fragment.html` |
| `skills/taste-skill/assets/ui/doc/` | 3249 | `fragment.js` |
| `skills/taste-skill/assets/ui/doc/` | 1245 | `meta.json` |
| `skills/taste-skill/assets/ui/files/` | 3973 | `fragment.css` |
| `skills/taste-skill/assets/ui/files/` | 3425 | `fragment.html` |
| `skills/taste-skill/assets/ui/files/` | 3525 | `fragment.js` |
| `skills/taste-skill/assets/ui/files/` | 1726 | `meta.json` |
| `skills/taste-skill/assets/ui/icons/` | 1004 | `asana.svg` |
| `skills/taste-skill/assets/ui/icons/` | 1894 | `calendly.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2413 | `confluence.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2225 | `docker.svg` |
| `skills/taste-skill/assets/ui/icons/` | 616 | `dropbox.svg` |
| `skills/taste-skill/assets/ui/icons/` | 836 | `figma.svg` |
| `skills/taste-skill/assets/ui/icons/` | 1554 | `git.svg` |
| `skills/taste-skill/assets/ui/icons/` | 3769 | `github.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2585 | `gitlab.svg` |
| `skills/taste-skill/assets/ui/icons/` | 1730 | `gmail.svg` |
| `skills/taste-skill/assets/ui/icons/` | 400 | `google-docs.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2105 | `google-drive.svg` |
| `skills/taste-skill/assets/ui/icons/` | 10662 | `icons-credits.json` |
| `skills/taste-skill/assets/ui/icons/` | 5311 | `intercom.svg` |
| `skills/taste-skill/assets/ui/icons/` | 1780 | `jira.svg` |
| `skills/taste-skill/assets/ui/icons/` | 15244 | `kubernetes.svg` |
| `skills/taste-skill/assets/ui/icons/` | 1681 | `linear.svg` |
| `skills/taste-skill/assets/ui/icons/` | 8036 | `mastercard.svg` |
| `skills/taste-skill/assets/ui/icons/` | 343 | `md.svg` |
| `skills/taste-skill/assets/ui/icons/` | 1662 | `messenger.svg` |
| `skills/taste-skill/assets/ui/icons/` | 3202 | `nodejs.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2878 | `notion.svg` |
| `skills/taste-skill/assets/ui/icons/` | 281 | `npm.svg` |
| `skills/taste-skill/assets/ui/icons/` | 3246 | `shopify.svg` |
| `skills/taste-skill/assets/ui/icons/` | 873 | `si-mastercard.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2671 | `slack.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2426 | `typescript.svg` |
| `skills/taste-skill/assets/ui/icons/` | 212 | `vercel.svg` |
| `skills/taste-skill/assets/ui/icons/` | 2189 | `visa.svg` |
| `skills/taste-skill/assets/ui/icons/` | 4124 | `whatsapp.svg` |
| `skills/taste-skill/assets/ui/icons/` | 640 | `zendesk.svg` |
| `skills/taste-skill/assets/ui/integrations/` | 1747 | `fragment.css` |
| `skills/taste-skill/assets/ui/integrations/` | 2417 | `fragment.html` |
| `skills/taste-skill/assets/ui/integrations/` | 2138 | `fragment.js` |
| `skills/taste-skill/assets/ui/integrations/` | 1163 | `meta.json` |
| `skills/taste-skill/assets/ui/notify/` | 1956 | `fragment.css` |
| `skills/taste-skill/assets/ui/notify/` | 1029 | `fragment.html` |
| `skills/taste-skill/assets/ui/notify/` | 2753 | `fragment.js` |
| `skills/taste-skill/assets/ui/notify/` | 1099 | `meta.json` |
| `skills/taste-skill/assets/ui/pipeline-board/` | 12457 | `fragment.css` |
| `skills/taste-skill/assets/ui/pipeline-board/` | 5136 | `fragment.html` |
| `skills/taste-skill/assets/ui/pipeline-board/` | 6544 | `fragment.js` |
| `skills/taste-skill/assets/ui/pipeline-board/` | 3249 | `meta.json` |
| `skills/taste-skill/assets/ui/search/` | 2639 | `fragment.css` |
| `skills/taste-skill/assets/ui/search/` | 1471 | `fragment.html` |
| `skills/taste-skill/assets/ui/search/` | 2730 | `fragment.js` |
| `skills/taste-skill/assets/ui/search/` | 751 | `meta.json` |
| `skills/taste-skill/assets/ui/slider/` | 3145 | `fragment.css` |
| `skills/taste-skill/assets/ui/slider/` | 1347 | `fragment.html` |
| `skills/taste-skill/assets/ui/slider/` | 2976 | `fragment.js` |
| `skills/taste-skill/assets/ui/slider/` | 1500 | `meta.json` |
| `skills/taste-skill/assets/ui/stat/` | 3589 | `fragment.css` |
| `skills/taste-skill/assets/ui/stat/` | 2151 | `fragment.html` |
| `skills/taste-skill/assets/ui/stat/` | 3640 | `fragment.js` |
| `skills/taste-skill/assets/ui/stat/` | 1154 | `meta.json` |
| `skills/taste-skill/assets/ui/terminal-run/` | 6625 | `fragment.css` |
| `skills/taste-skill/assets/ui/terminal-run/` | 3468 | `fragment.html` |
| `skills/taste-skill/assets/ui/terminal-run/` | 6320 | `fragment.js` |
| `skills/taste-skill/assets/ui/terminal-run/` | 2861 | `meta.json` |
| `skills/taste-skill/assets/ui/toggles/` | 1795 | `fragment.css` |
| `skills/taste-skill/assets/ui/toggles/` | 2113 | `fragment.html` |
| `skills/taste-skill/assets/ui/toggles/` | 1822 | `fragment.js` |
| `skills/taste-skill/assets/ui/toggles/` | 832 | `meta.json` |
| `skills/taste-skill/assets/ui/voice/` | 6113 | `fragment.css` |
| `skills/taste-skill/assets/ui/voice/` | 1518 | `fragment.html` |
| `skills/taste-skill/assets/ui/voice/` | 4797 | `fragment.js` |
| `skills/taste-skill/assets/ui/voice/` | 1510 | `meta.json` |
| `skills/taste-skill/assets/ui/window/` | 7192 | `fragment.css` |
| `skills/taste-skill/assets/ui/window/` | 4068 | `fragment.html` |
| `skills/taste-skill/assets/ui/window/` | 2632 | `fragment.js` |
| `skills/taste-skill/assets/ui/window/` | 1394 | `meta.json` |
| `skills/taste-skill/library/` | 43118 | `palettes.json` |
| `skills/taste-skill/library/` | 22998 | `type.json` |
| `skills/taste-skill/references/` | 7998 | `backgrounds.md` |
| `skills/taste-skill/references/` | 24292 | `cards.md` |
| `skills/taste-skill/references/` | 8056 | `copy-moves.md` |
| `skills/taste-skill/references/` | 9236 | `copy-registers.md` |
| `skills/taste-skill/references/` | 9612 | `copy-tells.md` |
| `skills/taste-skill/references/` | 11902 | `copy-voice.md` |
| `skills/taste-skill/references/` | 14747 | `copy.md` |
| `skills/taste-skill/references/` | 6860 | `diagrams.md` |
| `skills/taste-skill/references/` | 18582 | `effects-creative.md` |
| `skills/taste-skill/references/` | 23169 | `effects-objects.md` |
| `skills/taste-skill/references/` | 13591 | `effects-usage.md` |
| `skills/taste-skill/references/` | 13183 | `gate.md` |
| `skills/taste-skill/references/` | 6758 | `icons.md` |
| `skills/taste-skill/references/` | 23591 | `layout-v4.md` |
| `skills/taste-skill/references/` | 18173 | `moments.md` |
| `skills/taste-skill/references/` | 19242 | `motion.md` |
| `skills/taste-skill/references/` | 5707 | `perf.md` |
| `skills/taste-skill/references/` | 27704 | `photos.md` |
| `skills/taste-skill/references/` | 8705 | `scenes.md` |
| `skills/taste-skill/references/` | 66041 | `sections-library.md` |
| `skills/taste-skill/references/` | 53916 | `sections.md` |
| `skills/taste-skill/references/` | 16078 | `system.md` |
| `skills/taste-skill/scripts/` | 1015117 | `consistency.mjs` |
| `skills/taste-skill/scripts/` | 41437 | `copy-lint.mjs` |
| `skills/taste-skill/scripts/` | 33361 | `effects.mjs` |
| `skills/taste-skill/scripts/` | 87701 | `fx-gallery.template.html` |
| `skills/taste-skill/scripts/` | 22567 | `fx-lab.template.html` |
| `skills/taste-skill/scripts/` | 68364 | `gate.mjs` |
| `skills/taste-skill/scripts/` | 46035 | `icons.mjs` |
| `skills/taste-skill/scripts/` | 42632 | `moments.mjs` |
| `skills/taste-skill/scripts/` | 34716 | `perf.mjs` |
| `skills/taste-skill/scripts/` | 96474 | `photos.mjs` |
| `skills/taste-skill/scripts/` | 40467 | `shoot.mjs` |
| `skills/taste-skill/scripts/` | 32384 | `start.mjs` |
| `tests/` | 4069 | `frontmatter.mjs` |
| `tests/` | 11594 | `kit-clean.mjs` |
| `tests/` | 1796 | `text-encoding.mjs` |
| `skills/taste-skill/assets/icons/demo/` | 2748617 total | 929 files |
| `skills/taste-skill/assets/photos/img/` | 11741766 total | 66 files |

## Item map


### skills/taste-skill/SKILL.md (30970 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| S1 | Stop hook runs the source's gate script, 600 s timeout | later.md §Source tooling | later (tooling; not adopted: we never install a source hook) |
| S2 | Hook fallback writes a missing-gate notice | later.md §Source tooling | later (tooling) |
| S3 | Bar: plain-spoken company site at the level of large product companies | principles.md §The bar | covered |
| S4 | Needs Node 22+, a Chromium browser, optional ffmpeg | quality-gate.md §Tools | merged with feel-bar.md (Playwright/Chromium) |
| S5 | No caption under images; licence credits in one footer line | photos.md §Captions and credits | covered |
| S6 | Every visual draws at 1440/1024/768/390, never an empty ground | quality-gate.md §Visuals | covered |
| S7 | One section per screen; hero alone on first screen; 1-2 screens each | layout-and-heroes.md §Screens | covered |
| S8 | Exception: a photo-chapter section may run 3-4 screens | layout-and-heroes.md §Screens | covered |
| S9 | Equal left and right content edges | system.md §Grid and frame | covered |
| S10 | Hover layer: card lifts 2px, photo zooms 1.02-1.03 in frame, button press | motion.md §Hover and press | covered |
| S11 | Underlines draw; card loops 2.5-4 s, restart on hover | motion.md §Loops | covered |
| S12 | No tilt, carousels or timed tabs; hero enters once on load | motion.md §What never moves | covered |
| S13 | One dealt moment per page (two on long pages) | motion.md §Moments | covered |
| S14 | More and better real photos, grounds, heroes, fonts | principles.md §The bar | covered |
| S15 | Real full-colour icons of known products; small diagram cards | icons-and-diagrams.md §Real logos | covered |
| S16 | Scenes and shaders only for tech/AI/dev/gaming/fintech/hardware, never a local shop | grounds-and-effects.md §Who gets effects | merged with design-rules.md §3 effect caps |
| S17 | Demo addresses: street and district only | page-plans.md §Local business facts | expanded (real owner data vs demo) |
| S18 | Demo contacts use .example domains, no real-format phone | page-plans.md §Local business facts | expanded |
| S19 | Classify business kind first and declare it in markup | page-plans.md §Classify | merged with design-rules.md §3 page kinds |
| S20 | Table: brief → page type → site kind (6 kinds) | page-plans.md §Classify; data/craft/taste/patterns.csv | covered |
| S21 | A maker that opens its door or teaches is a place | page-plans.md §Classify | covered |
| S22 | Effects, scenes, loops, CSS grounds, dark pages are tech only | grounds-and-effects.md §Who gets effects | merged with design-rules.md §3 |
| S23 | Other kinds: photos, flat colour, type, real icons, one moment, hover | page-plans.md §Classify | covered |
| S24 | Place photo counts: 12-20 full, 8-12 compact, under 8 short page | page-plans.md §Place | covered |
| S25 | Place: offer and place sections differ; one type moment; text 16px | page-plans.md §Place | covered |
| S26 | Product/service: photos lead, 2+ per screen on product | page-plans.md §Product | covered |
| S27 | Product/service: no shader, grain, gradient, scene or loop | page-plans.md §Product | covered |
| S28 | Product without photos: listed stand-ins of its kind | photos.md §Stand-ins | covered |
| S29 | Product page: shown big, new picture each section, no fact twice | page-plans.md §Product | covered |
| S30 | Swatch changes the picture; each colour shown once | page-plans.md §Product | covered |
| S31 | Software shows its own UI in one app frame, not a generic dashboard | page-plans.md §Software | merged with directions.md "show the product working" |
| S32 | Hardware: its photos; never a hero of only an order form | page-plans.md §Hardware | covered |
| S33 | Game: name in h1, launch line, key art or stand-in world | page-plans.md §Game | covered |
| S34 | 60-80 words per screen outside UI | copy.md §Budget | covered |
| S35 | Tech: one effect, 1-2 moments, at most 4 live WebGL contexts | grounds-and-effects.md §Budget | covered |
| S36 | One object never carries the page | objects.md §Budget | covered |
| S37 | Client assets each get a finished-looking slot with stand-in | photos.md §Stand-ins | covered |
| S38 | Client video: real video element, play control only if file exists | later.md §Video | later (video) |
| S39 | Table: asset family by need and kind (18 rows) | data/craft/taste/patterns.csv | covered |
| S40 | Read an asset family's reference before using it | index.md | covered |
| S41 | Starter: empty folder vs existing project assets | principles.md §Stack | covered |
| S42 | Next.js builds a static export and is checked on the built page | principles.md §Stack | covered |
| S43 | Step 1: write kind, offer, buyer, main action, real material | principles.md §Order of work | merged with planner.md brief |
| S44 | Arm the finish gate with page, kind, category, primary | later.md §Source tooling | later (tooling) |
| S45 | Framework builds checked on dev URL or built page, rebuild first | quality-gate.md §Tools | covered |
| S46 | Step 2: write all copy first | principles.md §Order of work | covered |
| S47 | H1 names category and buyer; one hard fact; noun headings; verb+object buttons | copy.md §Headings and buttons | merged with copy.md (website) button wording |
| S48 | Invent nothing except a searched coined name and assumed place hours | copy.md §Truth | covered |
| S49 | Assumed facts marked in markup; drafts linted like pages | copy.md §Truth | covered |
| S50 | Step 3: plan as screens, one line per section | principles.md §Order of work | covered |
| S51 | Plan line fields: id, idea, picture, kind, screens, moment | principles.md §Order of work | covered |
| S52 | Step 4: deal, don't pick by taste; keep history so pages differ | principles.md §Deal | merged with design-rules.md §4 |
| S53 | Deal commands (hero, palette, fonts, brand, moment) | page-plans.md §Deal lists (`ult design deal`, 0.0.45; brand mark and moment still dealt by hand) | covered |
| S54 | Deal lists per kind for nav, footer, close, rhythm, buttons, mark | page-plans.md §Deal lists | covered |
| S55 | Product without photos deals photo heroes, object only for renders | page-plans.md §Product | covered |
| S56 | Game without art: setting hero; place hero fixed; product heroes limited | page-plans.md | covered |
| S57 | Take first palette unless clash; never violet | system.md §Colour | expanded (why: avoid the default AI palette) |
| S58 | Radius by kind: sharp fintech/dev, soft default, round consumer, square place | system.md §Radius | covered |
| S59 | Tech only: lit ground, CSS grounds, one effect | grounds-and-effects.md §Who gets effects | covered |
| S60 | Build: html lang and data attributes; three metas; head block | system.md §Head | covered |
| S61 | Copy only the hero markup, swap every word and picture | later.md §Source kit | later (source kit files) |
| S62 | Every section: one wrap, h2 first, 1-2 screens | system.md §Sections | covered |
| S63 | Paste UI fragments and diagrams with client labels | cards-and-ui.md §Interface fragments | covered |
| S64 | Icon scan writes every named icon locally | icons-and-diagrams.md §Serving icons | expanded (own approach, no source script) |
| S65 | Mount kit effects exactly as documented | later.md §Source kit | later (source kit) |
| S66 | Moment demo sections for place and service | motion.md §Moments | covered |
| S67 | Reuse booking form, credits line, share image | sections.md §Local business | covered |
| S68 | Run checks one browser at a time, foreground, 10 min timeout | quality-gate.md §Tools | covered |
| S69 | Serve over http on 127.0.0.1, … (shortened) | quality-gate.md §Tools | covered |
| S70 | Check block: copy lint, consistency, layout, screenshots, perf | quality-gate.md | covered |
| S71 | Shoot 1024, 820x1180, 768x1024, 390; every finding fails | quality-gate.md §Widths | expanded (adds 320 and 375) |
| S72 | Fix every copy FAIL/WARN, read aloud, re-read screenshots | quality-gate.md §Copy | covered |
| S73 | Fix rounds run the quick check at 1440 and 390 | quality-gate.md §Rounds | covered |
| S74 | Full gate run with 320 overflow walk | quality-gate.md §Widths | covered |
| S75 | Three gate rounds at most | quality-gate.md §Rounds | merged with design-rules.md §4 (3 revision rounds) |
| S76 | Never edit kit or hide things from checker; waivers with reasons | quality-gate.md §Waivers | covered |
| S77 | Client's own words waived hit by hit | quality-gate.md §Waivers | covered |
| S78 | Report: gate line, waivers, open fails, deal, voice, checks, assumed facts | quality-gate.md §Report | merged with guide.md report |
| S79 | Report lists stand-ins, demo form address, domain, client slots | quality-gate.md §Report | covered |
| S80 | Checklist first screen: what is sold, one fact, hero holds button | quality-gate.md §Checklist | covered |
| S81 | Checklist sections: 1-2 screens, nothing half empty | quality-gate.md §Checklist | covered |
| S82 | Checklist edges: on grid, no sideways scroll | quality-gate.md §Checklist | covered |
| S83 | Checklist: no captions, placeholders or demo addresses visible | quality-gate.md §Checklist | covered |
| S84 | Checklist kind fit | quality-gate.md §Checklist | covered |
| S85 | Checklist motion: controls answer, no tilt, loops 2.5-4 s, pause past 5 s | quality-gate.md §Checklist | expanded (WCAG 2.2.2) |
| S86 | Reduced motion rests everything without hiding content; 4 contexts max | motion.md §Reduced motion | expanded |
| S87 | Directions link only with a street | sections.md §Local business | covered |
| S88 | Keyboard checklist: names, alt, labels, headings, no positive tabindex, skip link | accessibility.md | expanded (WCAG 2.2) |
| S89 | Head: lang, title, description, share tags, menu expanded state | system.md §Head | covered |
| S90 | One system: one button pair, card style, radius scale, link look | system.md §One system | covered |
| S91 | Copy: noun headings, verb+object buttons, two hero actions max | copy.md §Headings and buttons | covered |
| S92 | One fact one wording; assumed facts marked; forms confirm only on real send | copy.md §Truth | covered |
| S93 | No perf FAIL rows | performance.md | covered |
| S94 | Phones 820/768/390/320: one column, 44px taps, full-width buttons | quality-gate.md §Widths | merged with design-rules.md §7 |
| S95 | Side by side with top company sites it reads professional | quality-gate.md §Eyes | covered |
| S96 | Never: fade-in on scroll cards, text parallax, scroll-jacking, blinking | motion.md §What never moves | merged with design-rules.md §2 (sections that fade in) |
| S97 | Never: stock photos passed off as the client's | photos.md §Truth | merged with design-rules.md §2 |
| S98 | Never: look-alike logos; invented reviews or figures | icons-and-diagrams.md; copy.md §Truth | merged with design-rules.md §2 |
| S99 | Never violet in the page's own design | system.md §Colour | merged with design-rules.md §2 (purple gradients) |
| S100 | Never copy a reference site's … (shortened) | principles.md §Never | covered |
| S101 | Never edit the kit to clear a check | quality-gate.md §Waivers | covered |
| S102 | Read copy, voice, system, layout and sections before the first page | index.md §Reading order | covered |

### skills/taste-skill/references/gate.md (13183 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| G1 | Finish gate blocks while fixable fails remain, counts rounds | quality-gate.md §Rounds | covered (as a manual loop; no hook) |
| G2 | Arm at step 1 with page, kind, category, action | later.md §Source tooling | later (tooling) |
| G3 | code: arm command | later.md §Source tooling | later (tooling) |
| G4 | Framework builds: dev URL or rebuilt page | quality-gate.md §Tools | covered |
| G5 | Gate opens only local pages (localhost, 127.0.0.1, *.test) | quality-gate.md §Tools | covered |
| G6 | Start/new/rounds options | later.md §Source tooling | later (tooling) |
| G7 | Deal arms the folder | later.md §Source tooling | later (tooling) |
| G8 | Build stays active while marker or rounds remain | later.md §Source tooling | later (tooling) |
| G9 | Page choice order | later.md §Source tooling | later (tooling) |
| G10 | Checks one at a time in fresh headless Chrome at 1440/390 | quality-gate.md §Tools | covered |
| G11 | Empty area: warn over 35%, fail over 50% of a section | quality-gate.md §Visuals | covered |
| G12 | Basics block: names, alt, labels, headings, Tab walk, lang, head, assumed facts | accessibility.md; quality-gate.md | merged with accessibility.md |
| G13 | Quick run omits forms, reduced motion, hover, loop pause, scroll walks | quality-gate.md §Rounds | covered |
| G14 | 390 adds collide and tap-size; 320 walk; content loads with scripts off | quality-gate.md §Widths | covered |
| G15 | Edited kit files are a finding | later.md §Source kit | later (source kit) |
| G16 | Checker-gaming code (webdriver sniffing) is a finding | quality-gate.md §Honest checks | covered |
| G17 | Headless user-agent tests and stripped aria-hidden are suspect | quality-gate.md §Honest checks | covered |
| G18 | Ported motion helper flagged suspect | later.md §Source kit | later (source kit) |
| G19 | Copy check: fails block, warns listed | quality-gate.md §Copy | covered |
| G20 | Blocking copy fails: residue, slop words, stock phrases, overused devices, cliché coined names | copy.md §Tells | covered |
| G21 | Brand-word exception; copy lint runs without a browser | copy.md §Tells | covered |
| G22 | Shared finding ids for height and neighbour checks | later.md §Source tooling | later (tooling) |
| G23 | Warns never block except hero entrance and missing moment | quality-gate.md §Severity | covered |
| G24 | code: waiver example | quality-gate.md §Waivers (own example) | covered |
| G25 | Waiver fields: check, target, reason length | quality-gate.md §Waivers | covered |
| G26 | Ambiguous waivers ignored; waived items reported | quality-gate.md §Waivers | covered |
| G27 | More than five waivers is a fail | quality-gate.md §Waivers | covered |
| G28 | A round counts only when page or waivers changed | quality-gate.md §Rounds | covered |
| G29 | Hook block allowance | later.md §Source tooling | later (tooling) |
| G30 | Rounds used up → stop and report | quality-gate.md §Rounds | covered |
| G31 | Done command closes the build | later.md §Source tooling | later (tooling) |
| G32 | Block limits per build | later.md §Source tooling | later (tooling) |
| G33 | Crashed runs stored; watchdog kills Chrome | later.md §Source tooling | later (tooling) |
| G34 | code: manual gate command | later.md §Source tooling | later (tooling) |
| G35 | Status words PASS/FAIL/OPEN/QUICK/SETUP/ERROR/OFF/DONE | quality-gate.md §Severity | covered |
| G36 | PASS finish; FAIL fix; OPEN report; QUICK not a round | quality-gate.md §Rounds | covered |
| G37 | Error: report the line, don't loop | quality-gate.md §Rounds | covered |
| G38 | code: Claude Code Stop hook JSON | later.md §Source tooling | later (tooling; not adopted) |
| G39 | code: Codex hook JSON | later.md §Source tooling | later (tooling) |
| G40 | code: Antigravity hook JSON | later.md §Source tooling | later (tooling) |
| G41 | Hook allows stop by silent exit 0 | later.md §Source tooling | later (tooling) |
| G42 | stop_hook_active doesn't end rounds | later.md §Source tooling | later (tooling) |
| G43 | Hook history entries | later.md §Source tooling | later (tooling) |
| G44 | Hook search path for the script | later.md §Source tooling | later (tooling) |
| G45 | Missing script notices | later.md §Source tooling | later (tooling) |
| G46 | Idle builds ignored; orchestrators allowed | later.md §Source tooling | later (tooling) |
| G47 | Subagents not held; run the manual check inside one | quality-gate.md §Tools | covered |

### skills/taste-skill/references/system.md (16078 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| Y1 | One system file; no second grid, scale, radius, button or card | system.md §One system | covered |
| Y2 | One button shape, radius family, card recipe, hairline, link look | system.md §One system | covered |
| Y3 | code: base reset and viewport-fit=cover | system.md §Reset (own example) | covered |
| Y4 | Without reset, measured offsets drift | system.md §Reset | covered |
| Y5 | Spacing 4-128 in ten steps; heading gap 48 (32 phone) | system.md §Spacing | covered |
| Y6 | Cards 24px apart (12 phone); one height per row; sections H or 2H | system.md §Spacing | covered |
| Y7 | code: skip link first in header targeting main | accessibility.md; system.md §Head (own example) | expanded |
| Y8 | Skip link hidden until first Tab | system.md §Head | covered |
| Y9 | html lang; hyphens auto for long words in headings | system.md §Type | covered |
| Y10 | Table: rhythm tokens (nav, pad top/bottom, gutter, heading gap, bar) | system.md §Tokens | covered |
| Y11 | Gutter 80 desktop, 24 phone; place 120 and 1200 wrap | system.md §Grid and frame | covered |
| Y12 | Bottom bar adds 64px + safe-area inset under 640 | system.md §Phone action bar | covered |
| Y13 | 12 columns, 24px gap (12 under 640); picture walls 0-2px gap | system.md §Grid and frame | covered |
| Y14 | Type tokens h1-label, body 16, small 14, label 13, stat 38/28 | system.md §Type | covered |
| Y15 | Place h2 fluid clamp 24-32 | system.md §Type (own clamp) | covered |
| Y16 | Reading text 16px+, line height 1.5-1.8, ink 7:1+ | system.md §Type | expanded (WCAG 1.4.3/1.4.12) |
| Y17 | Muted grey 4.5:1 only for labels and meta; large muted 3:1 | system.md §Colour | covered |
| Y18 | code: heading with a muted second sentence | system.md §Type (own example) | covered |
| Y19 | Hero one quieter text level; place 4.5:1; brand band 7:1 | system.md §Colour | covered |
| Y20 | Highlight by contrast only; no marker highlights; colour in a word once | system.md §Type | covered |
| Y21 | Sentence case; 13px labels at 500; no tracked caps; italic only for quotes | system.md §Type | merged with design-rules.md §2 (caps, eyebrows, italics) |
| Y22 | Curly quotes; non-breaking number+unit; 62 ch max; nothing under 13px | system.md §Type | covered |
| Y23 | One size per element kind; figures never outgrow headings; never shrink-to-fit | system.md §Type | covered |
| Y24 | Interface 90-95% neutral; warm near-black ink, never #000; hairlines 12-15% | system.md §Colour | covered |
| Y25 | Real logos full colour; fictional mark designed | icons-and-diagrams.md §Real logos | covered |
| Y26 | One accent drives primary, focus, links, brand band; under 3% elsewhere | system.md §Colour | merged with craft.md §3 |
| Y27 | Accent label 4.5:1; accent 3:1 vs ground | system.md §Colour | expanded (WCAG 1.4.11) |
| Y28 | Ground tokens main/alt/dark, brand band, tech CSS grounds | grounds-and-effects.md §Ground tokens | covered |
| Y29 | Light/evening grade chosen on load or click, never scroll | grounds-and-effects.md §Ground tokens | covered |
| Y30 | Words on photos only in hero and one closing band; no scrim; never on a place | photos.md §Text on photos | expanded (contrast measurement) |
| Y31 | Violet ban by OKLCH hue 270-330 | system.md §Colour | covered |
| Y32 | Radius scales sharp/soft/round | system.md §Radius | covered |
| Y33 | Software windows one radius 12-20; place square except controls | system.md §Radius | covered |
| Y34 | Buttons 44 high (48 place/bar), 16px label, 24px padding | system.md §Buttons | covered |
| Y35 | Two buttons per row max; full width on phone; dealt look | system.md §Buttons | covered |
| Y36 | One filled button per view; xl once; no slanted/gradient/ghost/shadow | system.md §Buttons | covered |
| Y37 | Primary may carry one drawn arrow; one style per page | system.md §Buttons | merged with design-rules.md §2 (arrow on every button) |
| Y38 | Fixed opaque nav with hairline; no blur, shrink, hide or shadow | sections.md §Navigation | covered |
| Y39 | Nav variants: plain, centre, split, tone | sections.md §Navigation | covered |
| Y40 | Logo: client SVG, dealt mark, initial or wordmark | sections.md §Navigation | covered |
| Y41 | 4-6 one-word links 15px/500; place words | sections.md §Navigation | covered |
| Y42 | Second action only as a plain word | sections.md §Navigation | covered |
| Y43 | Hover panel after 150ms; click goes to section | sections.md §Navigation | covered |
| Y44 | aria-current on one word with 2px bar | sections.md §Navigation | covered |
| Y45 | 640-1023: primary beside 44px menu button | sections.md §Navigation | covered |
| Y46 | Under 640: full-screen sheet, 56px rows; place adds street and hours | sections.md §Navigation | covered |
| Y47 | Phone action bar: one or two 48px buttons | system.md §Phone action bar | covered |
| Y48 | Bar shows after hero button scrolls off; hides when same action on screen | system.md §Phone action bar (own example) | covered |
| Y49 | Hidden bar is inert; without script stays put | system.md §Phone action bar | covered |
| Y50 | Bar after footer, no own script | system.md §Phone action bar | covered |
| Y51 | Closing footer: close row then directory and legal | sections.md §Footer | covered |
| Y52 | Footer types | sections.md §Footer | covered |
| Y53 | Legal row contents; imprint only with company details | sections.md §Footer | covered |
| Y54 | Social links only when supplied | sections.md §Footer | covered |
| Y55 | Cards per cards file; tiles for rooms, models, people | cards-and-ui.md | covered |
| Y56 | Rows for menus, prices, specs; FAQ open, no accordion | sections.md §FAQ | covered |
| Y57 | code: hours as a description list with days and time zone | sections.md §Local business (own example) | covered |
| Y58 | Script marks today and fills open-now | sections.md §Local business (own example, ran) | covered |
| Y59 | Assumed hours get no open-now; reads right without script | sections.md §Local business | covered |
| Y60 | Placeholder text and failed visuals outlined red | quality-gate.md §Visuals | covered |
| Y61 | One form recipe; named booking system replaces the form | sections.md §Local business | covered |
| Y62 | Form posts to client endpoint, else mailto stand-in; never action="#" | sections.md §Forms | covered |
| Y63 | Fields 48px, labels 14, text 16, six fields max, one column | sections.md §Forms | covered |
| Y64 | Visible label with for; placeholder is not a label | accessibility.md §Forms | merged with accessibility.md |
| Y65 | Right input types; paste allowed | accessibility.md §Forms | expanded (autocomplete tokens, 3.3.8) |
| Y66 | Errors on submit; aria-invalid, describedby, focus first error | accessibility.md §Forms | covered |
| Y67 | One status line, "Sending" after 300ms; failures keep typed text | sections.md §Forms | covered |
| Y68 | Success only after a real answer; never a modal | sections.md §Forms | covered |
| Y69 | Button names the action; sent line says when reply comes | copy.md §Headings and buttons | covered |
| Y70 | Every control named; icon buttons labelled | accessibility.md §Structure | covered |
| Y71 | Alt for content photos; decorative empty; drawn mocks role=img | accessibility.md §Structure | covered |
| Y72 | Headings step one level; no positive tabindex | accessibility.md §Structure | covered |
| Y73 | Focus ring 2px at 3:1, never animated, never under header | accessibility.md §Keyboard | expanded (WCAG 2.4.11) |
| Y74 | Menu button aria-expanded | sections.md §Navigation | covered |
| Y75 | Title pattern and one-line description | system.md §Head | merged with copy.md (website) meta titles |
| Y76 | Open Graph and Twitter card tags; share image from a screenshot | system.md §Head | covered |
| Y77 | Favicon from logo or mark | system.md §Head | covered |
| Y78 | theme-color equals the page ground | system.md §Head | covered |
| Y79 | Canonical only with the real domain | system.md §Head | covered |
| Y80 | Motion numbers live in the motion file | motion.md | covered |

### skills/taste-skill/references/perf.md (5707 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| P1 | Perf script at 1440 and 390 prints PASS/WARN/FAIL | performance.md §Measure | covered (own Playwright approach) |
| P2 | JSON output and run count | later.md §Source tooling | later (tooling) |
| P3 | Fix every fail; timing median of three loads | performance.md §Measure | covered |
| P4 | Busy host caps timing at warn | performance.md §Measure | covered |
| P5 | Lab FCP/LCP: compare pages, not field data | performance.md §Measure | covered |
| P6 | WebGL-off is a proxy; GPU compile not measured | performance.md §WebGL | covered |
| P7 | Counts and bytes are exact | performance.md §Measure | covered |
| P8 | Table: perf budgets (16 checks, warn/fail) | performance.md §Budgets | covered (own numbers from web.dev guidance) |
| P9 | Sizes in KiB | performance.md §Budgets | covered |
| P10 | 2.2x oversize limit; upscaled under 0.75x warns | performance.md §Images | covered |
| P11 | Never-mounted entry files counted | later.md §Source kit | later (source kit) |
| P12 | Every picture slot has src, width, height | performance.md §Images | covered |
| P13 | Failed visuals outlined; still-loading pictures named | quality-gate.md §Visuals | covered |
| P14 | Tech: 4 live WebGL contexts max, poster first | performance.md §WebGL | covered |
| P15 | Mount lazily with IntersectionObserver; observers don't drive motion | performance.md §WebGL | covered |
| P16 | Render budget ~1.5 MP, pixel ratio 1.5 max | performance.md §WebGL | covered |
| P17 | Noise/particles half resolution, ≤30fps, drop ratio on slow frames | performance.md §WebGL | covered |
| P18 | Every WebGL piece has a still fallback | performance.md §WebGL | covered |
| P19 | Shader lint after changes | later.md §Source tooling | later (tooling) |
| P20 | Draw static grounds once, release context | performance.md §WebGL | covered |
| P21 | Four font files max; preload two; swap; only used weights | performance.md §Fonts | merged with craft.md §2 |
| P22 | AVIF/WebP srcset at 2x; hero 2880w/780w | performance.md §Images | covered |
| P23 | Hero <400 KiB, photos <250 KiB, page images <2,400 KiB | performance.md §Budgets | covered |
| P24 | Dimensions or aspect-ratio on every image; fill while loading | performance.md §Images | merged with design-rules.md §7 |
| P25 | Lazy below fold; hero eager with fetchpriority high | performance.md §Images | covered |
| P26 | CLS under 0.1; transform and opacity only | performance.md §Layout shift | merged with libraries.md limits |
| P27 | background-position only on small spans; never animate layout | performance.md §Layout shift | covered |
| P28 | Deferred modules; no scroll listeners; no layout reads in handlers; no loader | performance.md §Scripts | covered |
| P29 | Non-tech pages: no animation library, no WebGL; 3D ~2 MB with poster | performance.md §Scripts | covered |
| P30 | Separate phone and desktop video files | later.md §Video | later (video) |
| P31 | Signal "first screen ready" to start effect mounting | performance.md §Scripts | covered |

### skills/taste-skill/references/icons.md (6758 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| I1 | Named tools show their real logo in own colours | icons-and-diagrams.md §Real logos | covered |
| I2 | Fictional client mark designed, not borrowed | icons-and-diagrams.md §Real logos | covered |
| I3 | One resolver writes local SVGs; no runtime CDN or tint | icons-and-diagrams.md §Serving icons | covered |
| I4 | Table: icon sets with source and licence (4 rows) | icons-and-diagrams.md §Icon sets | covered |
| I5 | link: gilbarbara/logos via jsDelivr | icons-and-diagrams.md §Icon sets (repo link) | covered |
| I6 | logos set ~1,500 colour brands, CC0, pinned | icons-and-diagrams.md §Icon sets | covered |
| I7 | Simple Icons for one-colour marks only when no colour mark | icons-and-diagrams.md §Icon sets | covered |
| I8 | vscode-icons (MIT) for file types | icons-and-diagrams.md §Icon sets | covered |
| I9 | Lucide (ISC) for interface glyphs | icons-and-diagrams.md §Icon sets | covered |
| I10 | Which brands come from Simple Icons | icons-and-diagrams.md §Icon sets | covered |
| I11 | Xbox and Nintendo marks absent: name in type | icons-and-diagrams.md §Trademarks | covered |
| I12 | Store row Steam/PlayStation/Epic; Office via file icons | icons-and-diagrams.md §Trademarks | covered |
| I13 | A brand-icon set dropped over unclear per-mark licences | icons-and-diagrams.md §Trademarks | covered |
| I14 | Marks are trademarks: nominative use, footer line, credits file | icons-and-diagrams.md §Trademarks | covered |
| I15 | Resolver find/apps/list commands | later.md §Source tooling | later (tooling) |
| I16 | Resolver fetch | later.md §Source tooling | later (tooling) |
| I17 | Resolver scan | later.md §Source tooling | later (tooling) |
| I18 | Resolver check | later.md §Source tooling | later (tooling) |
| I19 | Resolver measure | later.md §Source tooling | later (tooling) |
| I20 | code: import resolver in page code | later.md §Source tooling | later (tooling) |
| I21 | Written icons tagged violet/ink/paper | icons-and-diagrams.md §On dark grounds | covered |
| I22 | Logos list first, Simple Icons fallback | icons-and-diagrams.md §Icon sets | covered |
| I23 | Interface glyphs inline in text colour; mono for logo rows | icons-and-diagrams.md §Interface glyphs | covered |
| I24 | Multi-tone marks cut paper parts from silhouette | icons-and-diagrams.md §On dark grounds | covered |
| I25 | Black marks flip on dark; wordmarks wide slot | icons-and-diagrams.md §On dark grounds | covered |
| I26 | Light marks invisible on light tiles excluded | icons-and-diagrams.md §On dark grounds | covered |
| I27 | Violet-heavy marks flagged | icons-and-diagrams.md §On dark grounds | covered |
| I28 | Examples of violet-heavy brand marks | icons-and-diagrams.md §On dark grounds | covered |
| I29 | Marks under half violet drawn as is | icons-and-diagrams.md §On dark grounds | covered |
| I30 | Icon layout classes (tile, row, chip, stack, mosaic, file) | icons-and-diagrams.md §Layouts | covered |
| I31 | Icon sizes 16-56; icons never animate | icons-and-diagrams.md §Layouts | covered |
| I32 | Demo page of icon layouts | kit/icons/index.html (later.md §Shipped kit) | covered |
| I33 | Shape classes by aspect ratio | icons-and-diagrams.md §Layouts | covered |
| I34 | Tile fill 70% width / 68% height | icons-and-diagrams.md §Layouts | covered |
| I35 | File cards and integration grids at 20-40px | icons-and-diagrams.md §Layouts | covered |

### skills/taste-skill/references/diagrams.md (6860 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| D1 | Diagram engine draws node-and-line visuals from JSON | icons-and-diagrams.md §Diagrams | covered (own SVG approach) |
| D2 | 27 preset specs tagged by page kind | icons-and-diagrams.md §Diagram layouts | covered |
| D3 | Demo and builder pages | kit/diagrams/index.html, a generated gallery (later.md §Shipped kit); no builder page yet | covered |
| D4 | Diagram shows connection; UI fragment shows what users see | icons-and-diagrams.md §Diagrams | covered |
| D5 | One per section, two per page (tech); one still on product/service; none on place | icons-and-diagrams.md §Diagrams | covered |
| D6 | Game diagrams show a system, never replace pictures | icons-and-diagrams.md §Diagrams | covered |
| D7 | Table: 9 diagram layouts (hub, ring, tree, lanes, fan-in, sync, timeline, grid, free) | data/craft/taste/patterns.csv; icons-and-diagrams.md | covered |
| D8 | Hub draws mind map or radial web | icons-and-diagrams.md §Diagram layouts | covered |
| D9 | Filter presets by kind; pulses for tech | icons-and-diagrams.md §Diagram motion | covered |
| D10 | code: mount markup | icons-and-diagrams.md §Diagrams (own SVG example, ran) | covered |
| D11 | Rename preset labels to the client's | icons-and-diagrams.md §Labels | covered |
| D12 | code: spec in a JSON script tag | later.md §Source kit | later (source kit) |
| D13 | Bad spec logs error and draws what it can | icons-and-diagrams.md §Diagrams | covered |
| D14 | Builder tool | later.md §Source kit | later (source kit) |
| D15 | No CDN or runtime icon calls | icons-and-diagrams.md §Serving icons | covered |
| D16 | Icon scan covers diagram icons | later.md §Source tooling | later (tooling) |
| D17 | Violet, black and wordmark handling in diagrams | icons-and-diagrams.md §On dark grounds | covered |
| D18 | Icon folder override attribute | later.md §Source kit | later (source kit) |
| D19 | Pulse: spokes start 0.24-0.5 s apart in a 3.2 s cycle | icons-and-diagrams.md §Diagram motion | covered |
| D20 | Cycle 2.5-4 s; two loops never share a screen | motion.md §Loops | covered |
| D21 | Pulse restarts on pointer enter or focus | icons-and-diagrams.md §Diagram motion | covered |
| D22 | Pulses only on screen; phone and reduced motion hold still | icons-and-diagrams.md §Diagram motion | covered |
| D23 | Still attributes; looping diagram gets a pause control | icons-and-diagrams.md §Diagram motion | expanded (WCAG 2.2.2) |
| D24 | Light pulse as a comet with glow; hairline lines | icons-and-diagrams.md §Diagram motion | covered |
| D25 | Card never moves; nothing starts on scroll; core is an ink tile | icons-and-diagrams.md §Diagram motion | covered |
| D26 | Default grounds per layout | icons-and-diagrams.md §Diagram layouts | covered |
| D27 | Non-tech: no ground, no pulse | icons-and-diagrams.md §Diagrams | covered |
| D28 | Size steps (band, card) | icons-and-diagrams.md §Diagram layouts | covered |
| D29 | Line shapes: straight, curve, elbow, swirl | icons-and-diagrams.md §Diagram layouts | covered |
| D30 | Labels plain, 1-3 words | icons-and-diagrams.md §Labels | covered |
| D31 | Numbers look real; no jargon; core named as the product names it | icons-and-diagrams.md §Labels | merged with design-rules.md §2 (no fake stats) |
| D32 | Up to 8 spokes and 12 nodes; crowded → list | icons-and-diagrams.md §Labels | covered |
| D33 | No caption; title says what it shows; alt for screen readers | icons-and-diagrams.md §Labels | covered |
| D34 | Tool marks own colours; core without icon is a named pill | icons-and-diagrams.md §Labels | covered |

### skills/taste-skill/references/backgrounds.md (7998 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| B1 | Three ground tokens only | grounds-and-effects.md §Ground tokens | covered |
| B2 | 1-3 colours down the page, same at 390 | grounds-and-effects.md §Ground tokens | covered |
| B3 | Main ground: white or light client tint (L 0.80-0.97, low chroma) | grounds-and-effects.md §Ground tokens | covered |
| B4 | Main ground covers 55%+ of height (60% software/product) | grounds-and-effects.md §Ground tokens | covered |
| B5 | Main ground by trade | grounds-and-effects.md §Ground tokens | merged with design-rules.md §2 (cream by default) |
| B6 | Alt ground: same hue, 0.06-0.15 darker, not below 0.70 | grounds-and-effects.md §Ground tokens | covered |
| B7 | Alt ground for panels and one band | grounds-and-effects.md §Ground tokens | covered |
| B8 | Dark ground L ≤0.05; never charcoal or violet | grounds-and-effects.md §Ground tokens | covered |
| B9 | One dark body section; dark page tech only | grounds-and-effects.md §Ground tokens | covered |
| B10 | Brand band once in the second half on product and place | grounds-and-effects.md §Brand band | covered |
| B11 | Place brand band lightness/saturation; text 7:1; inverted button | grounds-and-effects.md §Brand band | covered |
| B12 | Grounds change at section edges; no rules between sections | grounds-and-effects.md §Ground tokens | merged with design-rules.md §2 (dividers) |
| B13 | No inset coloured box as a fake ground | grounds-and-effects.md §Ground tokens | covered |
| B14 | Non-tech kinds stay flat: no gradient, grain, glass, shadow | grounds-and-effects.md §Who gets effects | merged with design-rules.md §2 |
| B15 | Don't run the ground picker for non-tech | later.md §Source tooling | later (tooling) |
| B16 | Hardware dealt as tech | grounds-and-effects.md §Who gets effects | covered |
| B17 | Sixteen CSS grounds library | grounds-and-effects.md §Named grounds | covered |
| B18 | Grounds as section classes; stage, paper, top glow scopes | grounds-and-effects.md §Named grounds | covered |
| B19 | Section grounds keep ink 7:1, muted 4.5:1 | grounds-and-effects.md §Named grounds | covered |
| B20 | Ground metadata: mood, roles, pairs, avoids | data/craft/taste/patterns.csv | covered |
| B21 | Soft grounds: mist, halo, ruled, dots, arcs, liquid | grounds-and-effects.md §Named grounds | covered |
| B22 | Hard grounds: grain, dusk, band, field, photo, horizon, deep | grounds-and-effects.md §Named grounds | covered |
| B23 | code: ground picker command | later.md §Source tooling | later (tooling) |
| B24 | Hardware picker flags | later.md §Source tooling | later (tooling) |
| B25 | Rhythm bands: dark, lit, surface | grounds-and-effects.md §Rhythm | covered |
| B26 | Two dealt grounds max beyond tokens; one loud | grounds-and-effects.md §Rhythm | covered |
| B27 | Never two strong grounds as neighbours | grounds-and-effects.md §Rhythm | covered |
| B28 | Grain/texture and moving grounds count as the one effect | grounds-and-effects.md §Budget | covered |
| B29 | Moving ground runs on a clock with pause; still under reduced motion | grounds-and-effects.md §Budget | expanded (WCAG 2.2.2) |
| B30 | Lit ground tech only, behind UI and closing bands | grounds-and-effects.md §Named grounds | covered |
| B31 | Words on photo on its calm part; hero or one closing band | photos.md §Text on photos | covered |
| B32 | Tuning properties; tints lean to accent, never violet | grounds-and-effects.md §Named grounds | covered |
| B33 | Grounds never change height; soft fade over 120px | grounds-and-effects.md §Rhythm | covered |
| B34 | Code grounds mix tokens in OKLCH, chroma <0.12 | grounds-and-effects.md §Building gradients (own example, ran) | covered |
| B35 | Build gradients light first: 4-6 stops one hue, grain 4-10% | grounds-and-effects.md §Building gradients | covered |
| B36 | Dark gradients dithered; two-stop linear never decoration; seams are hard stops | grounds-and-effects.md §Building gradients | merged with design-rules.md §2 (gradients) |
| B37 | Grain only inside the one effect, never animated or over text | grounds-and-effects.md §Building gradients | covered |
| B38 | Lit studio sweep recipe | grounds-and-effects.md §Recipes | covered |
| B39 | Corner glow recipe | grounds-and-effects.md §Recipes | covered |
| B40 | Painterly field recipe | grounds-and-effects.md §Recipes | covered |
| B41 | Spotlight floor recipe | grounds-and-effects.md §Recipes | covered |
| B42 | Product-colour wash cross-fades on click, not scroll | grounds-and-effects.md §Recipes | covered |
| B43 | Woven tile and ordered dither, once per page | grounds-and-effects.md §Recipes | covered |
| B44 | Grid marks on one dark technical band | grounds-and-effects.md §Recipes | covered |
| B45 | Hairline ledger rules, never between sections | grounds-and-effects.md §Recipes | covered |

### skills/taste-skill/references/sections-library.md (66041 bytes) (hand-mapped)

| # | Source item | Our file § | Status |
|---|---|---|---|
| L1 | Frame: 1440 wrap 1280 at x80, 24px gutter, h1 72/h2 48; 390 wrap 342 at x24 | system.md §Grid and frame | covered |
| L2 | One split pair per page, text left visual right, phone stacks text first | sections.md §Rules for every section | covered |
| L3 | Cards at most two boxes deep; UI cards open or flush | cards-and-ui.md §Depth | merged with design-rules.md §2 (cards in cards) |
| L4 | Card widths per breakpoint, never under 304px | cards-and-ui.md §Widths | covered |
| L5 | One effect per page plus one still card ground | grounds-and-effects.md §Budget | merged with design-rules.md §3 effect caps |
| L6 | Product/service/place frames hold photos on flat colour | photos.md §Where photos lead | covered |
| L7 | UI fragments rewritten to client names, true size, never scaled | cards-and-ui.md §Interface fragments | covered |
| L8 | Fragment minimum widths per slot (324px, 256px) | cards-and-ui.md §Widths | covered |
| L9 | Fragment edges 24px clear or cut 24px+ with fade, checked at 4 widths | cards-and-ui.md §Interface fragments | covered |
| L10 | Phone cards inset fragments 16px | cards-and-ui.md §Widths | covered |
| L11 | One loop per card group with pause; two loops never share a screen | motion.md §Loops | expanded (WCAG 2.2.2) |
| L12 | Only system classes; page CSS only inside visuals | system.md §Tokens first | covered |
| L13 | Photos lead main sections of product/place/service pages, one look, one credit | photos.md §Where photos lead | covered |
| L14 | Example names invented; proof and figures only from the brief | copy.md §Truth | merged with design-rules.md §2 (numbers nobody can back up) |
| L15 | Logo SVG, one button look, nav primary, links to #ids | sections.md §Navigation | covered |
| L16 | nav-mega: grouped feature columns, short grey lines, one picture card | sections.md §Navigation | covered |
| L17 | nav-cards: 2-4 picture cards; place uses 3 photo cards with price | sections.md §Navigation | covered |
| L18 | nav-centre: centred links, 4-5 words, never wrap at 1024 | sections.md §Navigation | covered |
| L19 | nav-split: place/shop, logo centred, menu word opens photo cards | sections.md §Navigation | covered |
| L20 | Nav panel opens after 150ms hover, fade + 6px drop; Esc, aria-expanded | sections.md §Navigation | expanded (keyboard, focus return) |
| L21 | Hero h1 2-8 words; sub-line 15-30 words with a hard fact; place shows today's hours | sections.md §Hero copy | covered |
| L22 | Hero primary verb+object repeated in nav, close, phone bar | sections.md §Hero copy | merged with copy.md (ours) button wording |
| L23 | Hero picture by kind | layout-and-heroes.md §Picking a hero | covered |
| L24 | App store links as text, not badges | sections.md §Hero copy | covered |
| L25 | Window heroes: at most two fragments, never tilted/scaled | layout-and-heroes.md §Window heroes | covered |
| L26 | Phone device frame hero 280x570 | kit/ui/phone.html (later.md §Shipped kit) | covered |
| L27 | Dimension drawing SVG at true mm scale beside specs | icons-and-diagrams.md §Dimension drawing | covered |
| L28 | logo-row: up to 6 real logos, one still row | sections.md §Proof | covered |
| L29 | quote-stat: named quote ≤40 words with portrait beside a stat | sections.md §Proof | covered |
| L30 | customer-proof-row: three customer cards with stat | sections.md §Proof | covered |
| L31 | product-statement: paragraph with grey second half, cut-out photo, three facts | sections.md §Features | covered |
| L32 | features-2x2: four cards each with a panel | sections.md §Features | covered |
| L33 | bento: one wide + one narrow then three small, one panel height | sections.md §Features | covered |
| L34 | split-text-left: text with three facts beside overlapping frames | sections.md §Features | covered |
| L35 | tabs-tour: 3-6 click tabs drive one fixed-height frame | sections.md §Features | expanded (ARIA tabs pattern) |
| L36 | chapter: one feature area, wide frame, four names | sections.md §Features | covered |
| L37 | app-frame: list pane beside open pane, loop only on open pane | sections.md §App screens | covered |
| L38 | app-frame pane pairings table (code review, support, docs, CI, booking) | data/craft/taste/patterns.csv | covered |
| L39 | code: app-frame markup | sections.md §App screens (own example) | covered |
| L40 | code: app-frame grid ratios per breakpoint, list hidden under 640 | sections.md §App screens (own example) | covered |
| L41 | steps: three numbered cards, no arrows, never chained | sections.md §Features | merged with design-rules.md §2 (three-step boxes) |
| L42 | photo-band: full-width photo, short h2 on calm side, no scrim box | photos.md §Text on photos | expanded (contrast check) |
| L43 | photo-pair: two photos one ratio, no captions | photos.md §Layouts | covered |
| L44 | line-up: model tiles with photo, name, from-price | sections.md §Products and services | covered |
| L45 | rooms-list: room tiles with photo, seasonal price, book action | sections.md §Products and services | covered |
| L46 | services-list: rows with name, line, price from, beside a photo; no icon cards | sections.md §Products and services | covered |
| L47 | peek-list: rows swap a photo on hover/focus/tap | sections.md §Products and services | covered |
| L48 | people-row: four portrait tiles, real team only | sections.md §Proof | covered |
| L49 | integrations-grid: real tool icons; 72px tiles for 9+ | sections.md §Features | covered |
| L50 | calendar-frame: real-month calendar fixed height beside text | cards-and-ui.md §Calendar | covered |
| L51 | Calendar data: lead-in days, real days, today only in current month | cards-and-ui.md §Calendar (own example) | covered |
| L52 | timeline-rail: four dated moments, newest in accent | sections.md §Proof | covered |
| L53 | menu-in-type: price list as type beside a photo; no PDF menus | sections.md §Local business | covered |
| L54 | visit-map: address, hours with time zone, map or shopfront | sections.md §Local business | expanded (open-now logic, schema) |
| L55 | booking-form: six visible-label fields, never a modal | sections.md §Local business | expanded (WCAG 3.3, autocomplete) |
| L56 | client-slots: stand-ins with searchable file comments, never grey boxes | photos.md §Stand-ins | covered |
| L57 | Trailer video frame 16:9 with real play control | later.md | later (video) |
| L58 | Trailer play disc centring | later.md | later (video) |
| L59 | Screenshot strip: 3-5 uncaptioned 16:9 captures | sections.md §Features | covered |
| L60 | CAD/render frame and exploded frame on light ground | objects.md §Client renders | covered |
| L61 | Key-art slot with stand-in and file comment | photos.md §Stand-ins | covered |
| L62 | pricing-three: middle featured, monthly/yearly switch, subgrid rows | sections.md §Pricing | expanded (switch as radio group) |
| L63 | pricing-two: free and paid | sections.md §Pricing | covered |
| L64 | comparison-table: role=table, 48px rows, no sideways scroll | sections.md §Pricing | covered |
| L65 | faq: 5-8 open answers, short questions and answers | sections.md §FAQ | covered |
| L66 | close-type: big h2 with full-width xl button | sections.md §Close | covered |
| L67 | close-photo: action row above client photo | sections.md §Close | covered |
| L68 | close-word: client name across the wrap | sections.md §Close | covered |
| L69 | footer-columns: quiet, link columns mirror nav, legal row | sections.md §Footer | covered |
| L70 | footer-dark: the one dark band at the end | sections.md §Footer | covered |
| L71 | footer-visit: large address, directions, hours | sections.md §Footer | covered |
| L72 | footer-statement: inset slab combining close and footer | sections.md §Footer | covered |
| L73 | Page plan: neighbours never share a layout, calm after two visual, card layout max twice | page-plans.md §Rhythm | covered |
| L74 | Software plan example | page-plans.md §Software | covered |
| L75 | Product plan example | page-plans.md §Product | covered |
| L76 | Product without photos: stand-ins, 3D only on request | page-plans.md §Product | covered |
| L77 | Gaming plan example | page-plans.md §Game | covered |
| L78 | Gaming without art | page-plans.md §Game | covered |
| L79 | Place plan example | page-plans.md §Place | covered |
| L80 | Service plan example | page-plans.md §Service | covered |
| L81 | (no URLs; OpenStreetMap named) | sections.md §Local business (OSM link) | expanded |
| L82 | Tooling: photos.mjs, icons.mjs, deal.mjs, make-posters.mjs, starter.html | later.md | later (source tooling) |

### skills/taste-skill/references/copy.md (14747 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| CP1 | [rule] Say what it is in words a stranger gets in five seconds; no metaphor, poetry, invented terms or ad wording. | copy.md §The test | covered |
| CP2 | [rule] Studied sites are description only: copy their plain category-first style, never their words, code, pictures or effect. | copy.md §The test | covered |
| CP3 | [pattern] Copy layer is four files read at step 2: copy-voice, copy-registers, copy-moves, copy-tells. | copy.md §The test | merged with voice.md |
| CP4 | [later] copy-lint: `node … (shortened) | later.md §Source tooling | later |
| CP5 | [rule] Where files differ, copy.md wins. | copy.md §The test | covered |
| CP6 | [rule] Rule 1: h1 names the category (2-8 words), or buyer/place for an unknown brand; place h1 at most 40 characters; game = name plus genre. | copy.md §Headings and buttons | covered |
| CP7 | [rule] Rule 2: first screen holds one hard fact: number, place, price or date. | copy.md §Headings and buttons | covered |
| CP8 | [rule] Rule 3: every heading has a noun for a thing or section; one brand line per page, never the h1. | copy.md §Headings and buttons | covered |
| CP9 | [rule] Rule 4: buttons are a verb plus the visitor's gain, 1-5 words; banned labels: Learn more, Read more, Discover, Explore, More, Click here. | copy.md §Headings and buttons | covered |
| CP10 | [rule] Rule 5: max 2 hero … (shortened) | copy.md §Headings and buttons | covered |
| CP11 | [table] Plain versions: columns Vague / Plain; 4 rows (e.g. "Come climb" becomes a day pass with price). | copy.md §Headings and buttons | covered |
| CP12 | [rule] Hero sub-line: software 15-30 words; place 80 characters at most with today's hours; hotel names rooms and town. | copy.md §Headings and buttons | covered |
| CP13 | [rule] Section headings 1-6 words, two … (shortened) | copy.md §Headings and buttons | covered |
| CP14 | [rule] At most one two-fragment heading per page. | copy.md §Headings and buttons | covered |
| CP15 | [rule] Card titles: verb plus object, one line, no coy label. | copy.md §Headings and buttons | covered |
| CP16 | [rule] Grey second half of a … (shortened) | copy.md §Headings and buttons | covered |
| CP17 | [rule] Under-heading line 10-40 words; card body 1-2 sentences, 25 words max; no paragraph over five lines at 1440. | copy.md §Budget | covered |
| CP18 | [rule] Words per screen: product 47, place 44, service 34; page about 900 words max excluding footer. | copy.md §Budget | covered |
| CP19 | [rule] Tech word budget: 60-80 words per screen at 1440, excluding mocks and code; cut order given. | copy.md §Budget | covered |
| CP20 | [rule] Numbers sit in sentences with units; a sourced claim gets a numbered footnote near footer, 13px or larger. | copy.md §Budget | covered |
| CP21 | [rule] Pictures sit beside short copy; all words are live text. | copy.md §Budget | covered |
| CP22 | [rule] Form labels name the input; errors name the field; sent line names what was sent. | copy.md §Truth | covered |
| CP23 | [rule] Self-check: read each line aloud; then copy-voice section 6 and copy-lint. | copy.md §Before handing over | covered |
| CP24 | [rule] Prices, address, hours and dates … (shortened) | copy.md §Truth | covered |
| CP25 | [rule] Each assumed value carries `data-assumed` … (shortened) | copy.md §Truth | covered |
| CP26 | [code] Two markup examples: a price span and an hours `<dl>`, both with `data-assumed`. | copy.md §Truth | covered |
| CP27 | [rule] No invented proof: reviews, ratings, quotes, statistics, customers, names, portraits, awards, press; logos only for permitted real customers. | copy.md §Truth | covered |
| CP28 | [rule] No "sample", "examples", "illustrative" tags, notes or asterisks; brief-given target values stay worded inside the brief. | copy.md §Truth | covered |
| CP29 | [rule] No placeholders: brackets, lorem ipsum, TODO, "to be added", `#` or empty hrefs; "Coming soon" only if the brief says so. | copy.md §Truth | covered |
| CP30 | [rule] No caption, label or description … (shortened) | copy.md §Budget | covered |
| CP31 | [rule] Footer credits: one line naming sources only, 110 characters max, pasted exactly as photos.mjs prints it; never per-photo credit links. | copy.md §Truth | covered |
| CP32 | [rule] Map-data credit joins it; a logo-showing page adds a trademark line. | copy.md §Truth | covered |
| CP33 | [later] photos.mjs credits prints the credits line and list (tooling, named here). | later.md §Source tooling | later |
| CP34 | [rule] Each fact once: one value and wording for hours, price, address. | copy.md §Truth | covered |
| CP35 | [rule] Address: street and district only; … (shortened) | copy.md §Truth | covered |
| CP36 | [rule] Brief with no street: district … (shortened) | copy.md §Truth | covered |
| CP37 | [rule] Maps: no map loads with the page; directions link is an OpenStreetMap search by street and district; no street gives "See the area"; town only gives no map link. | copy.md §Truth | covered |
| CP38 | [link] https://www.openstreetmap.org/search?query=<street>+<district> (directions link template) | copy.md §Truth | covered |
| CP39 | [rule] A map is drawn only … (shortened) | copy.md §Truth | covered |
| CP40 | [rule] Phone: none unless the brief … (shortened) | copy.md §Truth | covered |
| CP41 | [rule] No imprint or company details (register number, VAT, managing director, court); legal row holds brand, year, Privacy, Terms, credits. | copy.md §Truth | covered |
| CP42 | [rule] Email: a form or an "Email us" button with a `.example` mailto; never print an email, domain or social handle; socials empty unless given. | copy.md §Truth | covered |
| CP43 | [rule] Names are coined, not dictionary words or existing businesses; search name plus trade and domain; record results in names.json. | copy.md §Truth | covered |
| CP44 | [later] copy-lint FAILs a coined name in title or h1, WARNs it elsewhere. | later.md §Source kit | later |
| CP45 | [rule] Links go where their label says; never "here"; one target, one label; no link to a closed answer. | copy.md §Headings and buttons | covered |
| CP46 | [rule] Newsletter: asked once, in or above footer, "Subscribe" or "Sign up", email field only, never a modal. | copy.md §Headings and buttons | covered |
| CP47 | [rule] Banned: metaphors and "where X … (shortened) | copy.md §Tells | covered |
| CP48 | [rule] Banned also: filler words, virtue words about the client, footer sign-off or pun, the model's default voice. | copy.md §Tells | covered |
| CP49 | [later] copy-lint FAILs old slop words, stock phrases, residue and over-budget devices; WARNs the countable rest. | later.md §Source tooling | later |
| CP50 | [later] Rival's-name check and read-aloud test catch what lint cannot. | later.md §Source kit | later |

### skills/taste-skill/references/copy-moves.md (8056 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| CM1 | [rule] Moves distilled from pre-2021 professional sites; examples are invented; learn the move, not the line. | voice.md §Copy moves | covered |
| CM2 | [rule] The copy.md rules (h1 category, heading nouns, verb buttons, nothing invented) hold throughout. | copy.md §Headings and buttons | covered |
| CM3 | [rule] Hero is 2-9 words, one clause, no stacked adjectives. | voice.md §Copy moves | covered |
| CM4 | [table] Hero forms: columns Form / Example / When; 8 rows (category and buyer, place, twist, customer, scope, year, superlative, name and genre). | voice.md §Copy moves | covered |
| CM5 | [rule] Greeting, mood, question, imperative, enemy, idiom and product news never take the h1; they fit sub-line, section opener, close or brand line. | voice.md §Copy moves | covered |
| CM6 | [pattern] Reader-state sub-line example (inbox sorted before opening). | voice.md §Copy moves | covered |
| CM7 | [pattern] Enemy-as-habit sub-line example (booking forms asking for too much). | voice.md §Copy moves | covered |
| CM8 | [pattern] Plain product-news line example (new model, same price). | voice.md §Copy moves | covered |
| CM9 | [rule] Software sub-line 15-30 words, one fact or mechanism; place sub-line 80 characters with hours. | copy.md §Headings and buttons | covered |
| CM10 | [rule] Default heading: name of the part plus a claim line under it. | copy.md §Tells | covered |
| CM11 | [pattern] Verb-and-thing heading for reader actions (send invoices from the van). | voice.md §Copy moves | covered |
| CM12 | [pattern] Plain claim with its noun heading (pays staff on the same day). | copy.md §Headings and buttons | covered |
| CM13 | [pattern] Figure-from-brief heading (routes count, reset schedule). | voice.md §Copy moves | covered |
| CM14 | [rule] Questions only in the FAQ; a close may ask once plainly if the register allows. | voice.md §Copy moves | covered |
| CM15 | [rule] About story opens on a … (shortened) | voice.md §Copy moves | covered |
| CM16 | [rule] About uses anecdotes, timelines or questions, never value pillars. | voice.md §Copy moves | covered |
| CM17 | [rule] Failure and luck belong in the story when the brief has them. | voice.md §Copy moves | covered |
| CM18 | [rule] Founders shown as people; only brief-given names. | voice.md §Copy moves | covered |
| CM19 | [rule] Values written as behaviours with numbers, not adjectives. | voice.md §Copy moves | covered |
| CM20 | [rule] About ends in a modest present tense. | voice.md §Copy moves | covered |
| CM21 | [rule] Say how to reach them: form, street, hours. | voice.md §Copy moves | covered |
| CM22 | [rule] Portfolio about: what the person does, work with dates, one belief line, availability date. | voice.md §Copy moves | covered |
| CM23 | [pattern] Features as mechanism in verb-led steps. | voice.md §Copy moves | covered |
| CM24 | [pattern] Outcome first, feature second as its proof. | voice.md §Copy moves | covered |
| CM25 | [pattern] A specific moment instead of a use case. | voice.md §Copy moves | covered |
| CM26 | [rule] Examples use real values (times, sizes, amounts), never "customisable". | voice.md §Copy moves | covered |
| CM27 | [rule] UI fragments carry client's own data (cards.md); tech UI carries most words. | voice.md §Copy moves | covered |
| CM28 | [rule] Names of rooms, plans and models used the same way every time. | voice.md §Copy moves | covered |
| CM29 | [rule] Card length varies with material known. | voice.md §Voice card | covered |
| CM30 | [rule] Proof only from the brief: verbatim quotes with name and role, sourced figures, permitted logos. | voice.md §Copy moves | covered |
| CM31 | [rule] Let others say superlatives, with attribution. | voice.md §Copy moves | covered |
| CM32 | [rule] Quotes stay rough and as written. | voice.md §Copy moves | covered |
| CM33 | [pattern] A rule instead of a claim proves craft (a brazing example). | voice.md §Copy moves | covered |
| CM34 | [rule] No proof is fine for craft, luxury and small places. | voice.md §Registers | covered |
| CM35 | [rule] Prices, FAQ and booking drop to plain facts. | voice.md §Voice card | covered |
| CM36 | [pattern] Perks priced literally (late checkout fee, hire per day). | voice.md §Copy moves | covered |
| CM37 | [rule] Risk reversal beside the button … (shortened) | voice.md §Copy moves | covered |
| CM38 | [pattern] Admit limits in the FAQ. | voice.md §Copy moves | covered |
| CM39 | [pattern] Answer the buyer's real objection flatly (data export). | voice.md §Copy moves | covered |
| CM40 | [rule] Button is verb plus real object. | copy.md §Headings and buttons | covered |
| CM41 | [rule] Button wording literal even when the register plays. | voice.md §Copy moves | covered |
| CM42 | [pattern] Low-pressure browse exit for browsers ("See the rooms first" style). | voice.md §Copy moves | covered |
| CM43 | [rule] Close restates the hero promise with one fact and the main action verbatim. | copy.md §Headings and buttons | covered |
| CM44 | [rule] Microcopy written whenever it exists; form rules still hold. | voice.md §Copy moves | covered |
| CM45 | [pattern] Form error sample: closed day, choose another. | voice.md §Copy moves | covered |
| CM46 | [pattern] Sent-message sample naming the request and reply time from the brief. | copy.md §Truth | covered |
| CM47 | [pattern] Empty-state sample (first item lands here). | voice.md §Copy moves | covered |
| CM48 | [pattern] 404 sample pointing to menu and hours. | voice.md §Copy moves | covered |
| CM49 | [pattern] Newsletter confirmation sample with the mailing rhythm from the brief. | voice.md §Copy moves | covered |
| CM50 | [pattern] Field-hint sample, only for what the brief promises. | voice.md §Copy moves | covered |
| CM51 | [rule] Footer: facts only (legal row, street, district, place hours); no sign-off or name pun. | voice.md §Copy moves | covered |
| CM52 | [rule] Odd human numbers beat round big ones, when the brief gives them. | voice.md §Copy moves | covered |
| CM53 | [rule] Every number sits in a sentence beside its claim. | voice.md §Copy moves | covered |
| CM54 | [rule] Humour points at ourselves, lives in asides or microcopy, absent from serious purchases. | voice.md §Copy moves | covered |
| CM55 | [pattern] Rhythm used once per page: short scene sentences, list ending on a surprise. | voice.md §Copy moves | covered |

### skills/taste-skill/references/copy-registers.md (9236 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| CR1 | [rule] Registers are pre-2021 voices; choose one per client, borrow one move from another; they never bend copy.md rules. | voice.md §Copy moves | covered |
| CR2 | [rule] No register is the default; … (shortened) | voice.md §Voice card | covered |
| CR3 | [rule] Register 0 (model default: warm, wry, literary, anti-big-company) is to be avoided unless asked for. | voice.md §Registers | covered |
| CR4 | [pattern] Register 1 Facts only: sample and moves (plain declaratives, names, dates, counts). | voice.md §Copy moves | covered |
| CR5 | [rule] Register 1 fits professional services, B2B, clubs; fails when facts are weak. | voice.md §Registers | covered |
| CR6 | [pattern] Register 2 Technical and dry: sample and moves (label plus figure, real commands, enemy as a category). | voice.md §Registers | covered |
| CR7 | [rule] Register 2 fits dev tools and APIs; fails as spec dump or abstractions. | voice.md §Registers | covered |
| CR8 | [pattern] Register 3 Founder's letter: sample and moves (first person, named enemy, refrain, sign-off in text). | voice.md §Registers | covered |
| CR9 | [rule] Register 3 fits stance-led products; fails when the stance is put on. | voice.md §Registers | covered |
| CR10 | [pattern] Register 4 Self-aware playful: sample and moves (straight face, joke in sub-line, hype words banned even as jokes). | voice.md §Registers | covered |
| CR11 | [rule] Register 4 fits drinks, snacks, studios; fails with jokes aimed at customers or on money/health purchases. | voice.md §Registers | covered |
| CR12 | [pattern] Register 5 Literary formal: sample and moves (raised vocabulary, "clients", sensory lists, plain price). | voice.md §Registers | covered |
| CR13 | [rule] Register 5 fits skincare and design objects; fails when ornate without exactness. | voice.md §Registers | covered |
| CR14 | [pattern] Register 6 Proper nouns and restraint: sample and moves (places, history, verbs like overlook; the word "luxury" never appears). | voice.md §Registers | covered |
| CR15 | [rule] Register 6 fits luxury hotels, heritage, galleries; fails with no real place or history. | voice.md §Registers | covered |
| CR16 | [pattern] Register 7 Sensory second person present: sample and moves (literal sensory facts, one absence, odd numbers). | voice.md §Registers | covered |
| CR17 | [rule] Register 7 fits cafes, fitness, spas; fails when every section turns sensory. | voice.md §Registers | covered |
| CR18 | [pattern] Register 8 Historical scene: sample and moves (dated opening, named streets and people). | voice.md §Registers | covered |
| CR19 | [rule] Register 8 fits restaurants and family firms; fails when history is generic. | voice.md §Registers | covered |
| CR20 | [pattern] Register 9 Plain-spoken activist: sample and moves (one measurable mission, admits harm, proof in numbers). | voice.md §Registers | covered |
| CR21 | [rule] Register 9 fits mission brands and non-profits; fails with abstract-noun missions. | voice.md §Registers | covered |
| CR22 | [pattern] Register 10 Refusal and narrowness: sample and moves (positioned by what it won't do, honest scarcity). | voice.md §Registers | covered |
| CR23 | [rule] Register 10 fits makers and specialists; fails when the refusal is invented. | voice.md §Registers | covered |
| CR24 | [pattern] Register 11 Product as hero: sample and moves (product is subject, a spec follows each turn of phrase). | voice.md §Registers | covered |
| CR25 | [rule] Register 11 fits hardware and single-feature apps; fails when a wordplay has no fact under it. | voice.md §Registers | covered |
| CR26 | [pattern] Register 12 Hurried conversational: sample and moves (talks to one busy person, bracketed asides, self-deprecation). | voice.md §Registers | covered |
| CR27 | [rule] Register 12 fits studios, freelancers, D2C founders; fails when chummy or jokes replace information. | voice.md §Registers | covered |
| CR28 | [table] Trade to voice: columns Trade / Try first / Avoid; 18 rows (cafe through wedding); avoid column gives banned phrases like "boutique", "magic", "passion". | voice.md §Registers | covered |

### skills/taste-skill/references/copy-tells.md (9612 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| CT1 | [rule] Models pick safe, common phrasing; specifics must come from the input, and every ban needs a positive move beside it. | copy.md §Truth | covered |
| CT2 | [rule] One tell proves little; clusters … (shortened) | copy.md §Tells | covered |
| CT3 | [rule] Old-generation ban words (about 50, e.g. delve, tapestry, elevate, seamless, robust); literal trade uses stay; client's own brand name gets one WARN. | copy.md §Tells | covered |
| CT4 | [later] Ban words are copy-slop-word; brand-name check is copy-brand-word. | scripts/ultlib/copylint.py worn-word rule; no brand-name check yet (later.md §Source tooling) | covered |
| CT5 | [rule] Stock lines to avoid (e.g. "In today's fast-paced world", "Look no further", "Let that sink in"); id copy-stock-phrase. | copy.md §Tells | covered |
| CT6 | [rule] Residue is the strongest tell: chatbot lines, template tokens, lorem, markdown, [NEED] (copy-residue). | copy.md §Tells | covered |
| CT7 | [pattern] The -ing rider tacked onto a fact (copy-ing-rider). | copy.md §Tells | covered |
| CT8 | [pattern] Question answered at once and the colon reveal (copy-reveal). | copy.md §Tells | covered |
| CT9 | [pattern] "serves as", "stands as", "plays … (shortened) | copy.md §Tells | covered |
| CT10 | [rule] Em dashes are a tell (copy-em-dash). | copy.md §Tells | covered |
| CT11 | [rule] Exclamation marks in body copy (copy-exclaim). | copy.md §Tells | covered |
| CT12 | [rule] Emoji bullets and arrows after link words. | copy.md §Tells | covered |
| CT13 | [pattern] Dead metaphors: landscape, ecosystem, journey, … (shortened) | copy.md §Tells | covered |
| CT14 | [pattern] House voice: warm, wry, literary for every client (the meta tell). | copy.md §Tells | covered |
| CT15 | [rule] Invented specifics such as batch numbers or percentages nobody measured (ban). | copy.md §Tells | covered |
| CT16 | [pattern] Strip of three or four figures under hero or story (copy-stat-strip); menu prices and timetables are not strips. | copy.md §Tells | covered |
| CT17 | [rule] Two-fragment "X. Y." heading, cap 1 (copy-two-fragment). | voice.md §Device budget | covered |
| CT18 | [rule] Number-pair headings like "Four X, four Y", cap 0-1 (copy-number-pair). | copy.md §Headings and buttons | covered |
| CT19 | [rule] Contrast frames and their substitutes, cap 2 together (copy-contrast). | voice.md §Device budget | covered |
| CT20 | [rule] Negation runs, cap 1, only when each item is a checkable refusal (copy-negation). | copy.md §Tells | covered |
| CT21 | [rule] Virtue words about ourselves are … (shortened) | copy.md §Tells | covered |
| CT22 | [pattern] Dry closer on paragraphs (joke at end). | voice.md §Device budget | covered |
| CT23 | [rule] Footer sign-off line (copy-footer-signoff); footer holds the legal row only. | voice.md §Device budget | covered |
| CT24 | [pattern] Name's metaphor run into the … (shortened) | copy.md §Tells | covered |
| CT25 | [pattern] Origin-story template with year and two founders; use brief's real story or none. | copy.md §Tells | covered |
| CT26 | [rule] Polished testimonials, three each with punchline (copy-quotes); none unless brief gives them. | copy.md §Tells | covered |
| CT27 | [rule] Default cast names for people and companies to avoid (copy-cast, copy-cast-company). | copy.md §Tells | covered |
| CT28 | [pattern] Section template: eyebrow, claim heading, lede, three cards, "Kind words", numbered steps, "Most popular" (copy-numbered, copy-eyebrows). | copy.md §Tells | covered |
| CT29 | [rule] Response-time promise: one, from the brief, same wording (copy-response-time). | voice.md §Device budget | covered |
| CT30 | [rule] "Since [year]" once where it matters (copy-since). | voice.md §Device budget | covered |
| CT31 | [rule] Proof figures like "3x faster" must carry brief units and sources (copy-proof-figure). | copy.md §Truth | covered |
| CT32 | [rule] Perfect evenness of card and paragraph lengths is a tell (copy-rhythm). | copy.md §Tells | covered |
| CT33 | [rule] Microcopy left unwritten under a hand-tuned hero. | voice.md §Copy moves | covered |
| CT34 | [pattern] Process talk: "This section shows", "Below, you'll find", "We've added" (copy-reveal). | copy.md §Tells | covered |
| CT35 | [rule] A copyright year older than this year (copy-stale-year). | copy.md §Tells | covered |
| CT36 | [table] Over-correction: columns Rule applied / Habit it breeds / Counter; 10 rows (e.g. no em dashes breeds comma splices). | voice.md §Over-correction | covered |
| CT37 | [rule] Not tells: plain "is"/"has", "in order to", title case house style, a true "no card needed", a provable superlative, purposeful refrain, a real list of three. | copy.md §Tells | covered |
| CT38 | [rule] Client-written copy is exempt; copy-lint waivers via gate.md (cross-reference). | copy.md §The test | covered |
| CT39 | [rule] Persuasion is the genre on … (shortened) | copy.md §Tells | covered |
| CT40 | [later] Bracketed ids are copy-lint.mjs ids (scripts/copy-lint.mjs named at the top). | later.md §Source tooling | later |

### skills/taste-skill/references/copy-voice.md (11902 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| CV1 | [rule] Copy-voice decides what words say and how they sound; read at step 2, checked at step 6 by copy-tells and copy-lint. | voice.md §Copy moves | covered |
| CV2 | [pattern] Why model copy reads as model copy: one voice for every client, same devices every section, sincerity said not shown, invented detail with recurring names. | voice.md §Why model copy reads as model copy | covered |
| CV3 | [rule] Professional copy differs in five ways: true details, each device used once, own voice, real risks, uneven pages. | voice.md §Why model copy reads as model copy | covered |
| CV4 | [rule] The fix is facts and … (shortened) | voice.md §Why model copy reads as model copy | covered |
| CV5 | [table] Fact sheet: columns Field / What it holds / Where it goes; 11 rows (what it is, for whom, today's alternative, true difference, customer words, numbers, people, odd details, a limit, an enemy, the offer). | voice.md §Fact sheet | covered |
| CV6 | [rule] Nothing invented beyond copy.md's allowances; an empty field shrinks or removes its section; no [NEED] or "coming soon". | voice.md §Fact sheet | covered |
| CV7 | [rule] Thin brief is not a … (shortened) | voice.md §Fact sheet | covered |
| CV8 | [rule] Limits and enemies come from the brief or trade facts; an invented flaw is still invented. | voice.md §Fact sheet | covered |
| CV9 | [rule] Default voice is out unless … (shortened) | voice.md §Voice card | covered |
| CV10 | [rule] Pick one register by buyer, price and character; write the voice card on the plan, not the page. | voice.md §Voice card | covered |
| CV11 | [code] Voice card template: seven labelled lines (Voice, Pairs, Person, Sentences, Humour, House words, Never). | voice.md §Voice card | covered |
| CV12 | [rule] A writing sample or old site from the client overrides the register menu. | voice.md §Voice card | covered |
| CV13 | [pattern] Nine-trades test: picture the voice on nine other trades; push further if it fits any. | voice.md §Voice card | covered |
| CV14 | [rule] Voice holds, tone moves: hero and story carry voice; prices, FAQ, booking and forms stay plain. | voice.md §Voice card | covered |
| CV15 | [rule] Register never bends copy.md's rules. | voice.md §Why model copy reads as model copy | covered |
| CV16 | [pattern] Reader's question order: what is it, is it for me, why believe, how it works, cost, what if it fails, what now. | voice.md §Order and length | covered |
| CV17 | [rule] Opening depends on reader knowledge: unaware, knows problem, comparing, knows client. | voice.md §Order and length | covered |
| CV18 | [rule] A section exists only with true material; five real sections beat eight padded ones. | voice.md §Order and length | covered |
| CV19 | [rule] Counts follow the content (four features, one quote, two plans). | voice.md §Order and length | covered |
| CV20 | [pattern] Organising idea (a menu as the page, timetable, founder's letter, one object) may break the template once. | voice.md §Order and length | covered |
| CV21 | [rule] Do not use the default skeleton in every section; vary lists, tables, letters, paragraphs. | voice.md §Order and length | covered |
| CV22 | [rule] Draft: facts replace adjectives; proper nouns over categories; mechanism in verb steps; customer's pain in their words. | voice.md §Copy moves | covered |
| CV23 | [rule] Draft: one admission per page; proof beside its claim; numbers with units; risk reversal only when given. | voice.md §Copy moves | covered |
| CV24 | [rule] Draft: microcopy carries voice; sentence length follows meaning; repeat the product name. | voice.md §Voice card | covered |
| CV25 | [table] Device budget: columns Device / Budget / Note; 15 rows (two-fragment heading, number-pair, negation run, contrast, dry closer, brand pun, footer sign-off, strip of figures, virtue words, lists of three, step numbers, eye | voice.md §Device budget | covered |
| CV26 | [later] copy-lint WARNs over budget and FAILs at twice budget plus one (scripts/copy-lint.mjs named). | scripts/ultlib/copylint.py: a warning above the per-page cap, a failure at 2 × cap + 1 | covered |
| CV27 | [rule] Check 1: run copy-lint; fix FAILs; fix or justify WARNs. | voice.md §Checks | covered |
| CV28 | [rule] Check 2: rival-name test; a line that still fits a rival is rewritten from the fact sheet. | voice.md §Fact sheet | covered |
| CV29 | [rule] Check 3: sameness across pages; lint several pages together and compare headings. | voice.md §Checks | covered |
| CV30 | [rule] Check 4: read aloud as the client; cut anything they would not say. | copy.md §Before handing over | covered |
| CV31 | [rule] Check 5: look for the over-correction habit that replaced the removed one. | voice.md §Checks | covered |
| CV32 | [pattern] Check 6: fresh-reader subagent given page text only; never iterate to beat an AI detector. | voice.md §Checks | covered |
| CV33 | [rule] Report carries the one-line voice card, every assumed value, and what the client must supply. | voice.md §Checks | covered |

### skills/taste-skill/references/cards.md (24292 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| CD1 | [pattern] Method: cards measured from a reference recording (x.ai Grok Bot 2x2 and Figma tile wall) and 41 company sites. | none (source's method note: how its cards were measured; no rule to carry) | later |
| CD2 | [link] assets/ui/cards.html: nine layouts, light and dark (showcase). | cards-and-ui.md §Interface fragments | covered |
| CD3 | [link] assets/ui/index.html: every fragment on its own. | sections.md §Rules for every section | covered |
| CD4 | [link] assets/ui/cards.css and assets/ui/base.css: card, panel, placement and fragment styles. | cards-and-ui.md §The card | covered |
| CD5 | [link] assets/ui/ui.js: motion script; assets/ui/_lab/object-card.html: object-instead-of-photo card. | cards-and-ui.md §The card | covered |
| CD6 | [later] scripts/icons.mjs: `fetch` or `scan --colour` downloads brand colour icon files (cited at line 101). | later.md §Source kit | later |
| CD7 | [rule] The card is barely there: … (shortened) | cards-and-ui.md §The card | covered |
| CD8 | [rule] Panel holds a real lit picture, never a flat gradient or line or dot pattern. | cards-and-ui.md §The card | covered |
| CD9 | [rule] UI at true size, cut … (shortened) | cards-and-ui.md §Interface fragments | covered |
| CD10 | [rule] One thing moves per card group; cards never move alone; linked cards lift 2px. | cards-and-ui.md §The card | covered |
| CD11 | [rule] Edges, radii and titles line up across a row. | cards-and-ui.md §The card | covered |
| CD12 | [rule] Card fill: --card, light white … (shortened) | cards-and-ui.md §The card | covered |
| CD13 | [rule] Border 1px at 8-14% ink; dark top highlight 5-7%; no blur shadow at rest; hover shadow only on linked cards; never tilted. | cards-and-ui.md §The card | covered |
| CD14 | [rule] Grid rows: … (shortened) | sections.md §App screens | covered |
| CD15 | [rule] Radius --r-lg (20; 18 on … (shortened) | cards-and-ui.md §The card | covered |
| CD16 | [rule] Title one line at 20/18 weight 500; body 16/24 in ink at 84%, max 46ch; muted small text only for labels. | cards-and-ui.md §The card | covered |
| CD17 | [rule] `.card--row` holds lines at two from 1024px. | cards-and-ui.md §The card | covered |
| CD18 | [rule] 32px from last line to panel edge; one --p-h per group. | cards-and-ui.md §The card | covered |
| CD19 | [code] Phone media query sets a panel height (`#features .panel` at max-width 639px) to fit four two-line tiles in two screens. | sections.md §Features | covered |
| CD20 | [rule] Two levels only: card > panel > fragment; never a patterned panel with a white card inside, never card-in-card text, never glass. | cards-and-ui.md §Depth | covered |
| CD21 | [rule] Default panel: side edges on text column, runs off bottom, lower 60-65% of card (--p-h 264-340px). | cards-and-ui.md §Depth | covered |
| CD22 | [rule] `.panel--inset`: 8px margin, radius 20-8=12 (never under 6), one ratio (4:3 or 16:10) per row. | cards-and-ui.md §Depth | covered |
| CD23 | [rule] `.panel--flush`: runs to card sides and bottom (image band). | cards-and-ui.md §Depth | covered |
| CD24 | [rule] `.panel--top`: on top with 8px margin for tall cards. | cards-and-ui.md §Depth | covered |
| CD25 | [rule] `.panel--device`: status row on the card, ground as screen, radius 12 (x.ai Computer card). | cards-and-ui.md §The card | covered |
| CD26 | [rule] A 1px inner edge over ground and fragments; vignette variables --vx, --vy, --calm-k (0% on lit ground). | cards-and-ui.md §Depth | covered |
| CD27 | [rule] Fragment shows the product's own subject as its users see it; never a generic dashboard or chat. | cards-and-ui.md §Interface fragments | covered |
| CD28 | [pattern] Subject examples: diff-review, invoices, booking calendar, pipeline-board, terminal-run. | cards-and-ui.md §Calendar | covered |
| CD29 | [rule] The product itself is shown once, large, in an app-frame (sections-library.md); small centred fragments read as fragments. | cards-and-ui.md §Interface fragments | covered |
| CD30 | [rule] Live HTML at true size: … (shortened) | cards-and-ui.md §Interface fragments | covered |
| CD31 | [table] Fragment minimum widths: columns Fragment / Min width px; 16 rows (chat 140 through window 456). | cards-and-ui.md §Widths | covered |
| CD32 | [rule] A phone mock runs past … (shortened) | cards-and-ui.md §Widths | covered |
| CD33 | [rule] Fragment surface white on light, #1c1d20 on dark (--frag); 1px border at 12%; radius 12; shadow only inside panel. | cards-and-ui.md §Interface fragments | covered |
| CD34 | [rule] Primary button is ink; the … (shortened) | cards-and-ui.md §Interface fragments | covered |
| CD35 | [rule] Real brand icons in own colours on a light tile; assets/icons files; `data-icon` attribute; no CDN for icons; one treatment per set. | cards-and-ui.md §Interface fragments | covered |
| CD36 | [later] icons.mjs `fetch` or `scan --colour` fetches the colour file (named in the icon rule). | later.md §Source kit | later |
| CD37 | [rule] Glyph marks only; wordmarks are illegible at tile size. | cards-and-ui.md §Interface fragments | covered |
| CD38 | [rule] Placements: `.at-corner` 28-40px from top-left, … (shortened) | cards-and-ui.md §Placements | covered |
| CD39 | [rule] `.at-over` puts a cursor dialog over a window only; `.at-center` only for a small control (about 250x130). | cards-and-ui.md §Placements | covered |
| CD40 | [rule] `.fit` with `--fit-max` keeps true width; `.wide` plus `--w` for a fluid grid cut by the right edge; `.to-edge` reaches 72px past bottom. | cards-and-ui.md §Placements | covered |
| CD41 | [rule] diff-review: `.at-corner.fit`, --fit-max 480px (up to 760), cut at bottom with stage--fade-b, top 250px holds the comment and Apply; phone panel 340px or more. | cards-and-ui.md §Placements | covered |
| CD42 | [rule] terminal-run: `.at-rise.fit`, … (shortened) | cards-and-ui.md §Interface fragments | covered |
| CD43 | [rule] pipeline-board: `.at-rise.fit` … (shortened) | cards-and-ui.md §Placements | covered |
| CD44 | [rule] Vary placements across a group: … (shortened) | cards-and-ui.md §Placements | covered |
| CD45 | [rule] Every edge keeps 24px of … (shortened) | cards-and-ui.md §Interface fragments | covered |
| CD46 | [rule] Fades (stage--fade-b, … (shortened) | cards-and-ui.md §Interface fragments | covered |
| CD47 | [rule] A fade never covers the point: the thing the card is about stays above 100% minus --fade-h. | cards-and-ui.md §The card | covered |
| CD48 | [rule] Measure at 1440, 1024, 768 and 390. | cards-and-ui.md §Interface fragments | covered |
| CD49 | [rule] Shader grounds only on tech pages, one per card group, from the page's effect family (effects-usage.md); product pages use a photo or diagram on a flat panel. | cards-and-ui.md §Grounds | covered |
| CD50 | [rule] One ground id per group; … (shortened) | cards-and-ui.md §Grounds | covered |
| CD51 | [rule] Soft fields behind UI: painterly-landscape, … (shortened) | cards-and-ui.md §Grounds | covered |
| CD52 | [rule] Banned behind UI: grid-pulse, ruled-grounds, … (shortened) | cards-and-ui.md §Grounds | covered |
| CD53 | [table] Palettes: columns Name / Colours / Notes; 4 rows (painting, sand, sky, sage; sky silk-folds takes #7f9fbd with tone 1). | sections.md §Navigation | covered |
| CD54 | [code] Painting palette parameters: blur 1, … (shortened) | effect-parts.md §Feature-card panels | merged with effect-parts.md |
| CD55 | [rule] Panels that hold UI get a lit palette 3:1 or more against the dark card, or a step darker than white UI on light. | cards-and-ui.md §Grounds | covered |
| CD56 | [rule] At most one painted panel per card group; the rest use sand, sky or sage. | cards-and-ui.md §The card | covered |
| CD57 | [rule] Accent never violet or lavender. | cards-and-ui.md §Grounds | covered |
| CD58 | [rule] Hold grounds still: speed 0 or drift 0, grainMotion 0 on grain-gradient; calmY near 1 where a fade meets it. | cards-and-ui.md §Grounds | covered |
| CD59 | [rule] A ground shows something behind something; decorative strips under stats are not allowed. | cards-and-ui.md §Grounds | covered |
| CD60 | [rule] Laptop GPU budget: `ui.grounds(document, fx)` bakes each still ground at up to 2 device pixels, one at a time, then frees its WebGL context. | cards-and-ui.md §Grounds | covered |
| CD61 | [rule] `data-fx-live` marks a driven ground: … (shortened) | cards-and-ui.md §Grounds | covered |
| CD62 | [rule] Live contexts allowed: page hero effect, driven ground, voice orb (dark only), hover light, object; never two of them; fx caps 3 live, page cap 4 (perf.md). | cards-and-ui.md §Grounds | covered |
| CD63 | [rule] Object or raymarch canvas mounts … (shortened) | cards-and-ui.md §Grounds | covered |
| CD64 | [rule] Loops are for tech pages: `data-ui-loop` on the one loop per group; all others hold their finished picture. | cards-and-ui.md §Loops | covered |
| CD65 | [rule] system.js marks others `data-ui-still`; under 640px every fragment except voice is still. | cards-and-ui.md §Loops | covered |
| CD66 | [rule] Without system.js: `ui.loadAll` and `ui.startAll` do the same, whenever a page has any `data-ui-loop`. | cards-and-ui.md §Loops | covered |
| CD67 | [rule] The group loop is the … (shortened) | cards-and-ui.md §Loops | covered |
| CD68 | [rule] Below the hero, two loops … (shortened) | cards-and-ui.md §Loops | covered |
| CD69 | [rule] Pause button: a 32px disc in the card beside the title (44px kept clear), or 12px in from bottom-right of a panel; keyboard focus plays a held cycle once. | cards-and-ui.md §Loops | covered |
| CD70 | [rule] Motion over 5 s needs `ui.pausable(panel, ctrl)` with pause() and resume(). | cards-and-ui.md §Loops | covered |
| CD71 | [rule] Loops start on the finished … (shortened) | cards-and-ui.md §Loops | covered |
| CD72 | [rule] Files status line uses data-reading on the root; a cut tile hides its name rather than half a word. | cards-and-ui.md §Loops | covered |
| CD73 | [rule] Cadence: one 2.5-4 s cycle, restarting on pointer or focus; a card with all held fragments plays its top one while hovered. | cards-and-ui.md §Loops | covered |
| CD74 | [rule] `ui.restart(el)` restarts fragments; each fragment fires a bubbling `ui-cycle` event. | cards-and-ui.md §Interface fragments | covered |
| CD75 | [rule] Fragment text comes from the … (shortened) | cards-and-ui.md §Loops | covered |
| CD76 | [pattern] Control drives ground: slider with drive param grain; compact option for `.at-center`. | cards-and-ui.md §Grounds | covered |
| CD77 | [pattern] stat with window true cuts … (shortened) | cards-and-ui.md §Grounds | covered |
| CD78 | [pattern] `.knock` puts a still canvas under white numbers with mix-blend-mode darken (lighten on light). | cards-and-ui.md §Grounds | covered |
| CD79 | [pattern] Voice orb: orb-sphere on dark; a CSS pearl with clouds and specks on light; never a dark glass ball. | cards-and-ui.md §Grounds | covered |
| CD80 | [pattern] Real object (tech only): an assets/objects item as the whole picture of a `.panel--top`, from effects-objects.md; turns, never tilts. | cards-and-ui.md §Grounds | covered |
| CD81 | [pattern] Featured plan lit border: data-glow edge-glow with data-glow-params fill 1, one light lap of about 4.6 s on hover or focus. | cards-and-ui.md §The card | covered |
| CD82 | [rule] Never: a big fragment dead centre, a dialog alone, three box levels, a pattern behind a list, a fade over the point, a dark ground behind dark UI. | cards-and-ui.md §Never | covered |
| CD83 | [rule] Never: accent on every chip, … (shortened) | cards-and-ui.md §Never | covered |
| CD84 | [rule] Never: cards moving with scroll, one WebGL context per panel, a "sample" or "example" note, a placeholder such as Example Street 1, small grey 15px card text. | cards-and-ui.md §Interface fragments | covered |

### skills/taste-skill/references/photos.md (27704 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| PH1 | [rule] A place is its photographs: 2-3 per screen, the client's own; software leads with real interface; games lead with own art, never library frames. | photos.md §Where photos lead | covered |
| PH2 | [rule] A physical product must show photographs (client's, else stand-ins); a photo never stands where an effect or empty box would. | photos.md §Where photos lead | covered |
| PH3 | [rule] Source order: 1 client's own, … (shortened) | photos.md §Sources, in order | covered |
| PH4 | [rule] data-source values: client, commissioned, phone, … (shortened) | photos.md §Sources, in order | covered |
| PH5 | [rule] Library (Wikimedia Commons, Unsplash) fills detail slots only (hands, tools, materials, process); never hero, room, shopfront, product, person; max one in three pictures. | photos.md §Sources, in order | covered |
| PH6 | [later] `pick` deals frames and prints the cap; `--draft-lead` lifts it (scripts/photos.mjs). | later.md §Source tooling | later |
| PH7 | [later] `fetch` prints data-source library-057; frames vetted at 100% for softness, grade, brands and faces; rating below 7 never dealt; weak frames kept but never dealt. | later.md §Source kit | later |
| PH8 | [table] Per-trade library caps: columns Trade … (shortened) | photos.md §Sources, in order | covered |
| PH9 | [rule] The rest of the page is client's own photos, the object, real UI or type. | photos.md §Where photos lead | covered |
| PH10 | [later] Live search: `photos.mjs search` asks … (shortened) | later.md §Source tooling | later |
| PH11 | [rule] Nothing is an acceptable fallback: real UI or type; a product render only if the brief asks for 3D. | photos.md §Where photos lead | covered |
| PH12 | [rule] With no client photos, say so in the report: half-day local shoot, then a phone shoot, then products on one backdrop. | photos.md §Stand-ins | covered |
| PH13 | [rule] Shot list: shopfront, room from the door, counter or bench, three products, hands at work, one detail, each guest room; 1x lens, window light, no flash. | photos.md §Stand-ins | covered |
| PH14 | [later] Draft path: `pick --draft-lead --pictures 12` with section words repeated until 8 or more frames (cafe 8-12, guesthouse 9). | later.md §Source tooling | later |
| PH15 | [rule] Draft pages stay whole place pages leading with a photograph; the hero is the lead pick returns. | photos.md §Where photos lead | covered |
| PH16 | [rule] A place whose trade leads with land passes `--place "<region>"`; the statement hero is used only when no frame fits. | photos.md §Stand-ins | covered |
| PH17 | [rule] Every library frame is listed … (shortened) | photos.md §Sources, in order | covered |
| PH18 | [rule] Under eight frames after pick … (shortened) | photos.md §Stand-ins | covered |
| PH19 | [rule] No drawn box, grid or effect substitutes for a photograph. | photos.md §Where photos lead | covered |
| PH20 | [rule] Two exceptions (draft hero, land around a place) are named in the report. | photos.md §Stand-ins | covered |
| PH21 | [rule] Product without photos (PH-04): no library frame, no mood stock, the product still shown (brief's picture, else stand-ins). | photos.md §Truth | covered |
| PH22 | [rule] Stand-ins show the same kind … (shortened) | photos.md §Stand-ins | covered |
| PH23 | [rule] Report lists the shots to take: product on plain backdrop, three angles, parts, product in use. | photos.md §Stand-ins | covered |
| PH24 | [later] `pick --product-without-photos` prints the search to run. | later.md §Source kit | later |
| PH25 | [later] Live search filter: JPEG 1600px … (shortened) | later.md §Source kit | later |
| PH26 | [table] Trade search words: columns Trade / Search words; 9 rows (yoga, pottery, studio, bike, hotel, wedding, restaurant, workshop, bakery/cafe/florist/salon). | photos.md §Stand-ins | covered |
| PH27 | [rule] Product searches its own words; a game its setting; others two or three words; `--count`, `--min 1200`, `--orientation portrait`. | photos.md §Stand-ins | covered |
| PH28 | [rule] Every search result is a candidate, viewed at full size; keep only if sharp, no readable business name, no staff face, no landmark, one grade. | photos.md §Stand-ins | covered |
| PH29 | [rule] Write new alt text for each stand-in; list it in the report; its credit goes in the footer line. | photos.md §Stand-ins | covered |
| PH30 | [later] Command block: list, list --places, pick, pick draft, pick with own-land and place, search trade, search words, fetch, credits --write. | later.md §Source kit | later |
| PH31 | [later] Pick prints a fetch with … (shortened) | later.md §Source kit | later |
| PH32 | [later] `--trade` values list (cafe, bakery, … (shortened) | later.md §Source tooling | later |
| PH33 | [later] Workshops name their craft; no craft named means nothing is dealt. | later.md §Source kit | later |
| PH34 | [later] `--sections` takes plain words; dealt nothing: hero (unless draft), menu, visit, contact, booking, closing; land words only with own-land. | later.md §Source kit | later |
| PH35 | [later] `--pictures N` caps library frames at N/3, default 12. | later.md §Source kit | later |
| PH36 | [later] Filter: rated 7 or more; … (shortened) | later.md §Source kit | later |
| PH37 | [rule] Land is only the client's own, except a draft stand-in for a region named by --place or --brief. | photos.md §Stand-ins | covered |
| PH38 | [later] Place matching: whole-name match ("Senjavegen" is not Senja); --place accepts several names separated by semicolons; --setting only narrows. | later.md §Source tooling | later |
| PH39 | [rule] moodOnly frames never serve as the client's room, counter or product, nor for trades with premises. | photos.md §Sources, in order | covered |
| PH40 | [later] --draft-lead permits only sharp landscapes as leads; --own-land adds land sections; --detail-only is a no-op. | later.md §Source kit | later |
| PH41 | [later] Flags --commons-only, --tone light/dark, --mono, --shop. | later.md §Source kit | later |
| PH42 | [later] Place pick prints words under the photo on the ground; product and service get band and calm-side hints. | later.md §Source tooling | later |
| PH43 | [later] Variety via --history and TASTE_SKILL_RECENT (shared recent-frame file across folders); soft frames never lead. | later.md §Source tooling | later |
| PH44 | [later] Section word subjects: hands, writing, notebook, paper; detail, texture, surface, linen, material; breakfast; rooms. | later.md §Source kit | later |
| PH45 | [table] Library frame counts: columns Trade / Frames; 16 rows (cafe 19 through wine 0; bakery 4, hotel 9, bike 6, workshop 5, studio 5, books 5, office 3, bar 0, outdoors 0). | photos.md §Stand-ins | covered |
| PH46 | [later] Trades with three or fewer frames are marked `thin` by list. | later.md §Source kit | later |
| PH47 | [rule] Place pages use 4:5, 4:3 … (shortened) | photos.md §Layouts | covered |
| PH48 | [rule] Container lines: x 120-1320 on … (shortened) | layout-and-heroes.md §Grid | covered |
| PH49 | [rule] One visual world: one light, … (shortened) | photos.md §Layouts | covered |
| PH50 | [rule] Product page shows the product whole in at most three sections. | photos.md §Layouts | covered |
| PH51 | [rule] Hero: plain full-colour; place hero … (shortened) | photos.md §Layouts | covered |
| PH52 | [rule] Rooms: one detail per room … (shortened) | photos.md §Layouts | covered |
| PH53 | [rule] Photo bands: product one or … (shortened) | photos.md §Layouts | covered |
| PH54 | [pattern] Place compositions: bleed, pair, trio, … (shortened) | photos.md §Layouts | covered |
| PH55 | [rule] Text on photographs: never on … (shortened) | photos.md §Text on photos | covered |
| PH56 | [rule] At 768 a 3:2 lead … (shortened) | photos.md §Text on photos | covered |
| PH57 | [rule] Full-bleed photos carrying words need a 390 crop with the subject inside the middle 342 px. | photos.md §Text on photos | covered |
| PH58 | [rule] Cut-outs only for the client's own product (transparent WebP, data-subject product); supplier images only in a product grid; illustration only if owned. | photos.md §Layouts | covered |
| PH59 | [later] Library files are WebP, 1200 wide, some 1600, 1800, 2144, 2400; caps: hero 400 KB, other 250 KB; perf.mjs FAILs above 2,400 KiB (named). | later.md §Source kit | later |
| PH60 | [rule] No 2x hero at 1440 in the library; replace with the client's own. | photos.md §Sources, in order | covered |
| PH61 | [later] `--hero` sets sizes 100vw, fetchpriority high, eager, plus a 780x975 phone crop in a picture source at max-width 639px; data-phone-fill kept. | later.md §Source kit | later |
| PH62 | [rule] A client hero photo gets … (shortened) | photos.md §Serving | covered |
| PH63 | [pattern] Other images: loading lazy, decoding … (shortened) | photos.md §Serving | covered |
| PH64 | [later] `--big` adds the largest file within 250 KB to a band; `--lqip` adds a 24px colour placeholder. | later.md §Video | later |
| PH65 | [rule] Nav and tab photos drop lazy loading; object-position follows focus; a wide frame keeps --ratio 66.7%. | photos.md §Serving | covered |
| PH66 | [rule] A photograph is visible from first paint: never inside an opacity-0 reveal or a developing mask; check four widths for blank frames. | photos.md §Serving | covered |
| PH67 | [rule] No print, dither, duotone, grain, filter or blend mode on any photograph. | photos.md §Treatment | covered |
| PH68 | [rule] Hover: a linked photo zooms 1.03 (1.02-1.03) over 600 ms inside its mask; no tilt, rotation or Ken Burns; place photos never change opacity. | photos.md §Treatment | covered |
| PH69 | [rule] Place photos have square corners and no border or shadow; product uses one radius; software windows 12-20 px. | photos.md §Treatment | covered |
| PH70 | [rule] Credits: one line in the legal row; no caption under pictures; a place name goes in alt text. | photos.md §Captions and credits | covered |
| PH71 | [later] `credits --out . --write` makes credits.html; --href points the line; --text for reports; "Photographs via Unsplash and Wikimedia Commons" at most 110 characters; list shows photographer, licence, source, adapted flag. | later.md §Source kit | later |
| PH72 | [rule] Public-domain frames are listed with the Public Domain Mark page and the photographer named. | photos.md §Captions and credits | covered |
| PH73 | [rule] Every word is live text, … (shortened) | photos.md §Text on photos | covered |
| PH74 | [rule] Never another business's identifiable room, … (shortened) | photos.md §Stand-ins | covered |
| PH75 | [rule] Never a face as staff, guest or customer; never another place's coast or landmark; never a lone house on a hotel page. | photos.md §Truth | covered |
| PH76 | [rule] Never trade stock: latte art … (shortened) | photos.md §Truth | covered |
| PH77 | [rule] Never mood stock, animals, vehicles, recognisable viewpoints, AI images, composites, Street View, gradients or shaders standing in for photos. | photos.md §Truth | covered |
| PH78 | [rule] Never repeat library frames across builds; use --history and TASTE_SKILL_RECENT. | photos.md §Stand-ins | covered |
| PH79 | [rule] Never use a live search result without viewing it full size, or leave it out of the report. | photos.md §Truth | covered |

### skills/taste-skill/references/sections.md (53916 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| SC1 | [rule] Write the plan first: line … (shortened) | sections.md §Rules for every section | covered |
| SC2 | [rule] Every section shows real material (photo, portrait, real icons, client UI, diagram card, or tech-only effect). | sections.md §Rules for every section | covered |
| SC3 | [rule] Picture-less sections are allowed only for a price list, FAQ, specs table, booking form, or dealt statement moment, each once. | sections.md §Rules for every section | covered |
| SC4 | [rule] Two picture-less sections never sit side by side; the short-page no-photo case is the sole exception. | sections.md §Rules for every section | covered |
| SC5 | [rule] A quote needs a face beside it or it merges into the section above. | sections.md §Rules for every section | covered |
| SC6 | [rule] A picture takes at least … (shortened) | sections.md §Rules for every section | covered |
| SC7 | [rule] One object never carries the page: the whole object leads the hero plus at most two sections; three object plan lines at most. | layout-and-heroes.md §Picking a hero | covered |
| SC8 | [rule] Testing evidence: a robot arm … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| SC9 | [rule] Other picture sections use a visual kind from the table, none more than twice; a recolour or crop of the whole still counts as the object. | sections.md §Rules for every section | covered |
| SC10 | [rule] A use photograph counts as … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC11 | [table] Kind-by-visual table; columns "Kind", "the … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| SC12 | [rule] Client-supplied assets (trailer, key art, in-engine shots, CAD renders, exploded model, motion video) each get a finished-looking designed slot. | later.md §Video | later |
| SC13 | [rule] A client slot holds a stand-in photograph at the file's final ratio, named in a comment; never an empty, grey, broken or "file missing" frame. | place-pages.md §Photographs | covered |
| SC14 | [later] Trailer or motion-video frame slot: … (shortened) | later.md §Video | later |
| SC15 | [technique] Screenshot strip slot: three to … (shortened) | place-pages.md §Photographs | covered |
| SC16 | [technique] CAD or render frame and exploded-frame slots; key art fills the hero stage; the report lists each slot, its file and stand-in. | layout-and-heroes.md §Picking a hero | covered |
| SC17 | [rule] One idea per section, one h2, and at most one action besides the main one (a pair allowed only in the hero or product compare-plus-buy). | sections.md §Rules for every section | covered |
| SC18 | [rule] The main action has identical wording in nav, hero, close or booking, and phone bar, and is a filled button nowhere else. | sections.md §Rules for every section | covered |
| SC19 | [rule] Short blocks (quote, logo row, … (shortened) | sections.md §Rules for every section | covered |
| SC20 | [rule] An FAQ whose answers open to 495px or more becomes its own section. | sections.md §FAQ | covered |
| SC21 | [rule] Card layouts (2x2, bento, three … (shortened) | sections.md §Rules for every section | covered |
| SC22 | [rule] On software, product and service, … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| SC23 | [rule] Repeat the section scaffold (heading, padding, ground logic) so the reader learns it once. | sections.md §Rules for every section | covered |
| SC24 | [rule] Proof appears only as small exact objects from the brief: named quote with face, footnoted figure, press line, rating line, permitted logos. | sections.md §Proof | covered |
| SC25 | [rule] Banned: big stat-number rows, filler stat strips, check-icon lists and customer-logo walls. | sections.md §Proof | covered |
| SC26 | [rule] Two boxes deep at most; … (shortened) | cards-and-ui.md §Depth | covered |
| SC27 | [rule] Every nav word, button and footer link targets an #id on the page; the logo targets #top. | sections.md §Rules for every section | covered |
| SC28 | [rule] The main action goes to the form or order section id, to #visit for directions, or to a mailto on .example when no form exists. | place-pages.md §Visit | covered |
| SC29 | [rule] Never link #contact from outside the footer; Privacy, Terms and Imprint get small pages or are omitted; never /contact, /[page] or a bare #. | sections.md §Footer | covered |
| SC30 | [rule] At 390 keep the desktop … (shortened) | sections.md §Rules for every section | covered |
| SC31 | [rule] At 768 and 820 re-plan … (shortened) | layout-and-heroes.md §Screens | covered |
| SC32 | [rule] Write the tablet screen count … (shortened) | sections.md §Rules for every section | covered |
| SC33 | [code] Shell one-liner that randomly picks one entry per option list (nav, footer, close, rhythm, buttons, mark) from pipe-separated arguments. | place-pages.md §Close and footer | covered |
| SC34 | [rule] Hero and pairing come from deal.mjs and start.mjs, never from the one-liner; a place takes the place hero. | layout-and-heroes.md §Place hero | covered |
| SC35 | [rule] Write dealt results on plan … (shortened) | layout-and-heroes.md §Screens | covered |
| SC36 | [rule] Re-deal a part only when … (shortened) | page-plans.md §Deal lists | covered |
| SC37 | [rule] With no photograph: nav-cards becomes nav-split (no panel) or nav-centre; close-photo becomes close-word without the name. | sections.md §Close | covered |
| SC38 | [rule] With no photograph: media-band becomes space (games keep it as a setting photo) and a place hero becomes the statement hero on .ground-brand. | layout-and-heroes.md §Picking a hero | covered |
| SC39 | [technique] Nav options: nav-mega (link columns, one picture card), nav-cards (three or four cards), nav-centre, nav-split; nav--tone is tech only. | sections.md §Navigation | covered |
| SC40 | [technique] Footer options: footer-columns, footer-dark, footer-statement (tech only, lit ground), footer-visit (places or services with a door). | sections.md §Footer | covered |
| SC41 | [technique] Close options: close-type (h2, a line, full-width big button), close-photo (head row then photograph), close-word (h2, button, name set across the wrap). | sections.md §Close | covered |
| SC42 | [technique] dark-band: one inverse-ground section at mid-page or later, holding the strongest visual. | page-plans.md §Rhythm | covered |
| SC43 | [technique] media-band: one full-width photograph layer … (shortened) | layout-and-heroes.md §Place hero | covered |
| SC44 | [technique] surface-pairs: one surface band of … (shortened) | sections.md §Rules for every section | covered |
| SC45 | [technique] Buttons set on the html data-buttons attribute: solid, pill, tonal, arrow, block. | page-plans.md §Deal lists | covered |
| SC46 | [technique] A mark sits beside the name in nav and footer; a client's own logo replaces it. | sections.md §Navigation | covered |
| SC47 | [rule] Optional parts go in brackets, listed in page order; tell it as a story (say, show, prove, explore); tabs only on software and only on click. | place-pages.md §Order by trade | covered |
| SC48 | [pattern] Software plan: nav, hero, optional docked logo row, app-frame, two or three feature sections, integrations diagram, proof, pricing or comparison, FAQ, footer.closing. | sections.md §Rules for every section | covered |
| SC49 | [pattern] app-frame: the product big in one app window across the wrap, its list beside the open item. | sections.md §App screens | covered |
| SC50 | [rule] Software pictures: the client's live HTML screens, else assets/ui fragments rewritten to the product's own subject; diagram cards; real tool icons. | cards-and-ui.md §Interface fragments | covered |
| SC51 | [rule] Software integrations: fanin-warehouse or hub-tools … (shortened) | sections.md §Features | covered |
| SC52 | [rule] Software proof: quote-stat or customer-proof-row … (shortened) | sections.md §Proof | covered |
| SC53 | [rule] Software options: nav-mega, nav-cards or nav-centre; footer-dark, footer-statement or footer-columns; close-type or close-word; rhythm dark-band, surface-pairs or space; buttons solid, pill, tonal or arrow. | page-plans.md §Deal lists | covered |
| SC54 | [rule] Software never: stock people at … (shortened) | sections.md §App screens | covered |
| SC55 | [pattern] Gaming plan: nav, named hero, trailer frame, full-bleed world sections, screenshot strip of three to five cards, system diagram, platforms, press, FAQ, footer with action. | sections.md §Rules for every section | covered |
| SC56 | [rule] Testing: a game page that … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC57 | [rule] Gaming hero names the game … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC58 | [rule] The lead or a line under the hero carries the brief's launch date or status; with no date use a status such as "Coming to PC", never an invented date. | layout-and-heroes.md §Picking a hero | covered |
| SC59 | [rule] When key art is supplied, key art and in-engine shots run full bleed in hero and world sections under one grade, dealt with --has film,photo. | layout-and-heroes.md §Picking a hero | covered |
| SC60 | [rule] The world and the crew … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC61 | [technique] No-art path: the hero is … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC62 | [technique] No-art path details: three to five frames of one light, nothing readable on them, dealt with --has setting; the game name set large or on a dark empty area (data-box="none"). | layout-and-heroes.md §Screens | covered |
| SC63 | [rule] The widest setting frame runs full bleed as a media-band or dark-band world section under an h2; other frames fill trailer and screenshot slots, each named. | layout-and-heroes.md §Picking a hero | covered |
| SC64 | [rule] One shader effect may sit behind words in its own section, never on the photographs; a rendered hero object only when the brief asks for 3D. | layout-and-heroes.md §Picking a hero | covered |
| SC65 | [rule] Every stand-in frame is listed in the report with the art that should replace it. | sections.md §Rules for every section | covered |
| SC66 | [rule] Platforms: real Steam, PlayStation and … (shortened) | sections.md §Features | covered |
| SC67 | [rule] Gaming options: nav-mega, nav-centre or nav-cards; footer-dark or footer-statement; close-word or close-type; rhythm dark-band, media-band or space; buttons solid, pill or block. | page-plans.md §Deal lists | covered |
| SC68 | [rule] Gaming never: a hero that … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC69 | [rule] Gaming never: UI fragments, dashboards or SaaS widgets (no UI kit on gaming), stock players at screens, or drawn SVG or empty panels in place of the world. | sections.md §App screens | covered |
| SC70 | [pattern] Product plan: nav, hero, range … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC71 | [rule] Product: the whole product appears in three sections at most; every main section shows the product's world. | sections.md §Rules for every section | covered |
| SC72 | [rule] Product prices: "from" prices on … (shortened) | sections.md §Rules for every section | covered |
| SC73 | [rule] Technical products may take the … (shortened) | sections.md §Products and services | covered |
| SC74 | [rule] Product rule 1, Big: in … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| SC75 | [technique] Product hero stage: a render … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| SC76 | [rule] Never a mid-size product inside … (shortened) | cards-and-ui.md §The card | covered |
| SC77 | [rule] A product photograph runs edge … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| SC78 | [rule] Product rule 2: the whole … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC79 | [rule] Never show one view twice: … (shortened) | sections.md §Rules for every section | covered |
| SC80 | [rule] Product rule 3: every promise … (shortened) | layout-and-heroes.md §Screens | covered |
| SC81 | [rule] Product rule 4: each picture section takes a composition from bleed, pair, trio, strip or tall-small; neighbours differ; the order section comes last. | sections.md §Rules for every section | covered |
| SC82 | [technique] Product bleed: the product at … (shortened) | page-plans.md §Product | covered |
| SC83 | [technique] Product pair: two views at one ratio, side by side. | page-plans.md §Product | covered |
| SC84 | [technique] Product trio: the whole product, a part, and a detail. | page-plans.md §Product | covered |
| SC85 | [technique] Product strip: four close-ups of … (shortened) | page-plans.md §Product | covered |
| SC86 | [technique] Product tall-small: the product in use shown tall, a detail small beside it. | sections.md §Rules for every section | covered |
| SC87 | [technique] Product split: text beside one … (shortened) | sections.md §Rules for every section | covered |
| SC88 | [rule] One section stands on a … (shortened) | page-plans.md §Rhythm | covered |
| SC89 | [rule] Product rule 5: colour swatches swap the product picture; render swatches carry data-product-swatch and value attributes; photographs swap src and alt per colour. | place-pages.md §Photographs | covered |
| SC90 | [rule] Every colour offered must be shown at least once on the page; an offered colour never shown is a fault. | sections.md §Rules for every section | covered |
| SC91 | [rule] Product rule 6: no fact twice; the stat strip takes the three selling figures (load, range, price) and spec rows take the rest. | layout-and-heroes.md §Screens | covered |
| SC92 | [rule] Product rule 7: buttons step and press via the motion layer, with no page CSS on .btn transform or transition; a linked card lifts 2px and its picture zooms 1.03. | cards-and-ui.md §The card | covered |
| SC93 | [rule] Without photographs the product is still shown; a brief-supplied cut-out, CAD view or render goes on the hero stage. | layout-and-heroes.md §Picking a hero | covered |
| SC94 | [technique] Stand-in search: photos.mjs pick --product-without-photos … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC95 | [rule] Stand-in frames: no maker's name, … (shortened) | cards-and-ui.md §Interface fragments | covered |
| SC96 | [later] Product stand-in hero: deal.mjs --type … (shortened) | later.md §Source tooling | later |
| SC97 | [rule] A colour the stand-ins cannot … (shortened) | place-pages.md §Order by trade | covered |
| SC98 | [rule] Hardware without photos: stand-ins of … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| SC99 | [rule] A render only when the … (shortened) | objects.md §Who gets an object | covered |
| SC100 | [later] Render path: product-render helper from … (shortened) | later.md §Source kit | later |
| SC101 | [rule] Renders stay still by default, … (shortened) | cards-and-ui.md §Grounds | covered |
| SC102 | [rule] Product never: photographs of something else, app screens the product lacks, logo rows, tabs, or copy apologising for missing material. | sections.md §App screens | covered |
| SC103 | [rule] Product never: a mid-size product in a grey panel, the whole product in more than three sections, a repeated view, or a repeated fact. | sections.md §Rules for every section | covered |
| SC104 | [pattern] Service plan: nav, hero, services list (with price from when given), work grid of three to six photos or photo-pair, steps, people row, proof quote, pricing, FAQ, booking form with address, footer.closing. | sections.md §Rules for every section | covered |
| SC105 | [rule] Service pictures: photographs of the work, team and rooms, one or two per screen; real icons only for tools a studio really uses. | sections.md §Rules for every section | covered |
| SC106 | [rule] Service options: nav-mega, nav-split or nav-centre; footer-visit, footer-dark or footer-columns; close-type or close-photo; rhythm surface-pairs, dark-band or space; buttons solid, tonal, block or arrow. | page-plans.md §Deal lists | covered |
| SC107 | [rule] Service never: product UI the … (shortened) | sections.md §Proof | covered |
| SC108 | [rule] Place kind: cafes, bars, bakeries, restaurants, guesthouses, shops, bookshops, florists, bike shops, local studios; the door decides, so a maker who teaches or sells online still counts as a place. | layout-and-heroes.md §Place hero | covered |
| SC109 | [rule] Place markup: html data-type="place", meta … (shortened) | place-pages.md §What a place page is | covered |
| SC110 | [rule] Named places to study for … (shortened) | sections.md §Hero copy | covered |
| SC111 | [rule] Never on a place: effects, WebGL, canvas, CSS gradients, grain, glass, print, scenes, loops, counters, UI fragments or diagrams. | place-pages.md §What a place page is | covered |
| SC112 | [rule] Never on a place: feature … (shortened) | place-pages.md §What a place page is | covered |
| SC113 | [rule] Never on a place: unbriefed ratings, reviews, figures or quotes; words on photographs; rounded or filtered photos; see-through or blurred nav. | place-pages.md §What a place page is | covered |
| SC114 | [rule] Never on a place: outline, … (shortened) | place-pages.md §What a place page is | covered |
| SC115 | [rule] Length counts: the nav is … (shortened) | sections.md §Footer | covered |
| SC116 | [pattern] Full place page: 12 to 20 photographs, at most six screens: hero, visit, offer, place, orders or booking, footer.closing; over six screens drop the place, never the booking. | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC117 | [pattern] Compact place page: 8 to 12 photographs over four or five screens: hero, visit, offer, optional place, footer.closing. | layout-and-heroes.md §Screens | covered |
| SC118 | [pattern] Short place page: under 8 … (shortened) | place-pages.md §Short page | covered |
| SC119 | [later] Draft path with no client photos: photos.mjs pick --trade with --sections and --draft-lead, repeating section words for rows until eight or more frames. | later.md §Source tooling | later |
| SC120 | [rule] The hero is a photograph whenever any frame fits; a remote place passes its region via --place so its landscape leads; statement hero only without any frame. | place-pages.md §Photographs | covered |
| SC121 | [rule] Page length follows the count, not the trade: under eight frames including the client's is the short page; eight to twelve compact; twelve or more full. | place-pages.md §Photographs | covered |
| SC122 | [rule] Photographs per section, all distinct: … (shortened) | place-pages.md §Photographs | covered |
| SC123 | [rule] The three length names (full, … (shortened) | place-pages.md §Photographs | covered |
| SC124 | [code] Shell one-liner dealing place parts: nav, footer, rhythm, buttons, mark, offer and place compositions, type moment and rooms layout. | place-pages.md §Type moment | covered |
| SC125 | [rule] After dealing, re-deal the place composition while it equals the offer's; rhythm is surface-pairs, space or colour-band (close on the brand ground). | place-pages.md §Short page | covered |
| SC126 | [technique] Never two sections built round … (shortened) | place-pages.md §Photographs | covered |
| SC127 | [table] Five-compositions table for place; columns "id", "at 1440", "at 390"; five rows (bleed, pair, trio, strip, tall-small). | place-pages.md §Compositions | covered |
| SC128 | [pattern] Place bleed: a head row, … (shortened) | place-pages.md §Compositions | covered |
| SC129 | [pattern] Place pair: two photographs on span-6 at one ratio (4:3 588x441 or 4:5 588x735), tops level; at 390 stacked, 342 wide, 24 apart. | place-pages.md §Compositions | covered |
| SC130 | [pattern] Place trio: span-5 4:5 (486x607), … (shortened) | place-pages.md §Compositions | covered |
| SC131 | [pattern] Place strip: four 1:1 details … (shortened) | place-pages.md §Compositions | covered |
| SC132 | [pattern] Place tall-small: a 4:5 tall … (shortened) | place-pages.md §Compositions | covered |
| SC133 | [technique] Offer composition: strip runs under menu groups; pair or tall-small take the photograph slot beside groups narrowed to span-6. | place-pages.md §Compositions | covered |
| SC134 | [pattern] Place wall: head row, then … (shortened) | place-pages.md §Compositions | covered |
| SC135 | [pattern] Place story: 6/6 with text … (shortened) | place-pages.md §Compositions | covered |
| SC136 | [pattern] Type moment "address": street and district set large under the visit h2; no invented street; display clamp from 48px to 104px. | place-pages.md §Type moment | covered |
| SC137 | [pattern] Type moment "name": makes the close close-word; the photograph then goes to the place composition; footer name capped at 12vw. | place-pages.md §Type moment | covered |
| SC138 | [rule] Type moment: one a page; … (shortened) | place-pages.md §Type moment | covered |
| SC139 | [rule] Hover: linked photographs zoom 1.03 and their cards lift 2px; head-row links carry an arrow; nav words draw underlines; each section after the hero holds one such link. | place-pages.md §Actions and motion | covered |
| SC140 | [rule] One main action a screen: transactions appear in the nav and hero, booking or close, and phone bar; Get directions never repeats beyond hero, phone bar and desktop nav. | sections.md §Rules for every section | covered |
| SC141 | [rule] The nav word "Visit" points … (shortened) | place-pages.md §Close and footer | covered |
| SC142 | [rule] List text at 16/24 minimum (menu rows, descriptions, room facts, hours); 13px only for group labels. | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC143 | [rule] Credits: one footer line links to the credits list, never one link per photograph. | sections.md §Footer | covered |
| SC144 | [pattern] Place hero copy: h1 of 40 characters at most (what and where), sub-line of 80 characters at most with one fact, one main button. | place-pages.md §Hero | covered |
| SC145 | [pattern] Visit section: always screen two after the hero, data-place="visit" and id="visit", a panel on --g-alt on span-6, a 1:1 or 4:3 shopfront or room photo 6/6, panel left. | place-pages.md §Visit | covered |
| SC146 | [rule] Visit panel: h2 "Visit" top-left, open-now line at its right only with brief-given hours; address at 20/30 linked to the map; tel link only when given; week's hours in tabular figures. | place-pages.md §Visit | covered |
| SC147 | [rule] Visit secondary button: "Get directions" … (shortened) | place-pages.md §Visit | covered |
| SC148 | [rule] Visit extra rows: at most two 44px rows (access, delivery area, check-in and check-out, repair turnaround, or "By appointment"). | place-pages.md §Visit | covered |
| SC149 | [rule] Visit at 390: panel first … (shortened) | place-pages.md §Visit | covered |
| SC150 | [rule] With the address moment, the h2 and street run across the wrap above the split and the photo becomes 4:3. | place-pages.md §Visit | covered |
| SC151 | [pattern] Map: only when a street … (shortened) | place-pages.md §Visit | covered |
| SC152 | [pattern] Offer head row: h2 of … (shortened) | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC153 | [pattern] Menu group: 13px weight-500 label with 12px air and no rule; rows with 1px closing rules; name 16/24/500 left, tabular price right, optional 16/24 muted description. | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC154 | [rule] Menu row limits: 44px rows (64 with description); six rows with descriptions or eight without; the rest behind the head-row link; paired groups hold equal row counts. | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC155 | [rule] Menu is always text with prices visible; never an image, PDF, tabs or accordion; at 390 one column with photographs after the first group. | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC156 | [pattern] Rooms section: h2 "Rooms and prices", side line of breakfast and check-in and check-out times; each room has a 4:3 photo, name, facts, price-from and "Book this room". | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC157 | [pattern] Rooms row layout: three on … (shortened) | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC158 | [pattern] Rooms side layout: head as … (shortened) | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC159 | [pattern] Goods grid: four linked cards … (shortened) | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC160 | [rule] Goods at 390: two-up at … (shortened) | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC161 | [pattern] Orders section: three kinds on … (shortened) | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC162 | [rule] A florist's events order states what to send: date, venue, guests and budget. | place-pages.md §Offer: menus, rooms, goods, orders | covered |
| SC163 | [pattern] Booking section: head row ("Book … (shortened) | place-pages.md §Booking | covered |
| SC164 | [rule] Booking form: text fields instead of type=date on non-English pages; no photo, texture or glass under the form; a briefed booking system replaces the form. | place-pages.md §Booking | covered |
| SC165 | [pattern] Close (close-photo): h2 of eight words at most, one line such as opening hours, the main action, and a 1:1 photo never used above with no words on it. | place-pages.md §Close and footer | covered |
| SC166 | [rule] Close on colour-band: sits on the brand ground with every word at 7:1 and the button inverted. | place-pages.md §Close and footer | covered |
| SC167 | [pattern] Footer-visit: address at 32/40 on … (shortened) | place-pages.md §Close and footer | covered |
| SC168 | [pattern] Footer-columns: Visit, Contact as given, nav words, delivery or check-in or newsletter, and the legal row. | place-pages.md §Close and footer | covered |
| SC169 | [pattern] Phone bar (nav.actionbar, required): order … (shortened) | place-pages.md §Actions and motion | covered |
| SC170 | [pattern] Notice line: one 14px line … (shortened) | place-pages.md §Hero | covered |
| SC171 | [rule] Splits are 6/6, text left, … (shortened) | layout-and-heroes.md §Grid | covered |
| SC172 | [pattern] Cafe order: menu as text … (shortened) | place-pages.md §Order by trade | covered |
| SC173 | [pattern] Bakery order: goods with prices; one order card per kind; process as strip or trio on one screen; several shops as a ruled list with streets; under eight frames is the short page. | place-pages.md §Order by trade | covered |
| SC174 | [pattern] Guesthouse order: hero shows the … (shortened) | place-pages.md §Order by trade | covered |
| SC175 | [pattern] Shop or bookshop order: new-in goods with Add; categories as plain text; one story row; footer with each shop's address, hours and newsletter; four to six nav categories. | place-pages.md §Order by trade | covered |
| SC176 | [pattern] Bike shop order: visit and … (shortened) | place-pages.md §Order by trade | covered |
| SC177 | [pattern] Florist order: notice line with … (shortened) | place-pages.md §Order by trade | covered |
| SC178 | [later] Palette dealt by trade: start.mjs … (shortened) | later.md §Source tooling | later |
| SC179 | [later] Client colours replace the deal via start.mjs brand with --bg, --ink and --accent; colours are quoted because a bare # starts a shell comment. | later.md §Source tooling | later |
| SC180 | [rule] Accent: the palette's one accent … (shortened) | place-pages.md §Colour and type by trade | covered |
| SC181 | [rule] Grounds: one surface band at most plus one brand band; no dark section except the brand band (the nav may take dark ink); flat colour only. | place-pages.md §Colour and type by trade | covered |
| SC182 | [rule] Type pairing by trade: display 400, text 400 and 500; serif head with plain sans for bakery, restaurant or guesthouse; one sans in two weights for shops; soft sans for cafe or yoga. | place-pages.md §Colour and type by trade | covered |
| SC183 | [rule] Motion on place: hover layer … (shortened) | place-pages.md §Actions and motion | covered |
| SC184 | [rule] On load the place hero … (shortened) | layout-and-heroes.md §Place hero | covered |
| SC185 | [pattern] Short page structure: hero, one … (shortened) | place-pages.md §Short page | covered |
| SC186 | [rule] Short page section is open … (shortened) | place-pages.md §Short page | covered |
| SC187 | [pattern] Short page with photo: groups … (shortened) | place-pages.md §Short page | covered |
| SC188 | [rule] Short page menu names fit one line beside their price on span-3 (about 24 characters) with equal row counts; longer names get shortened. | place-pages.md §Short page | covered |
| SC189 | [rule] Short page under 640px: --hm 2 with the photo after the groups at 16:9 via a page CSS rule; at 1:1 the section runs 119px long. | place-pages.md §Short page | covered |
| SC190 | [rule] Short page nav: three or four words, each pointing at a group id (#tableware, #classes, #visit); a section with no scroll-marked word leaves aria-current off. | place-pages.md §Short page | covered |
| SC191 | [rule] Short page re-dealt without pictures: nav-split with no panel, close-word without the name; choose the brand band or the wide footer name, not both. | place-pages.md §Short page | covered |
| SC192 | [pattern] Short page moment with photo: picture-develops on the figure (needs half the wrap or more), dealt via moments.mjs; re-deal with photo-chapters excluded. | place-pages.md §Short page | covered |
| SC193 | [pattern] Short page moment without photo: one statement section of 12 to 40 words with word-highlight, making the page four screens, 3,600px at 1440. | place-pages.md §Short page | covered |
| SC194 | [rule] Short page drops: no place … (shortened) | place-pages.md §Short page | covered |
| SC195 | [rule] Short page tablet (640 to 1023) stays one screen at 600 to 830px content; keep three groups and three visit columns across via a page CSS rule using repeat(3). | place-pages.md §Short page | covered |
| SC196 | [rule] Short page tablet with photo: --h 2 read as two screens (h2 and full-width photo, then groups and visit columns); this rule replaces the earlier tablet rule. | place-pages.md §Short page | covered |
| SC197 | [rule] Place with no photographs: no … (shortened) | place-pages.md §Photographs | covered |
| SC198 | [rule] A place with no photos … (shortened) | place-pages.md §Photographs | covered |
| SC199 | [technique] UI fragments: paste assets/ui/<name>/fragment.html into … (shortened) | cards-and-ui.md §Interface fragments | covered |
| SC200 | [later] Kit icon samples are rewritten as the client's tools with data-icon attributes; icons.mjs scan --colour fetches them. | later.md §Source kit | later |
| SC201 | [rule] data-ui-load shows the kit's sample … (shortened) | cards-and-ui.md §Interface fragments | covered |
| SC202 | [pattern] Diagram cards: only when the … (shortened) | place-pages.md §What a place page is | covered |
| SC203 | [rule] Real icons: every tool, app … (shortened) | sections.md §Rules for every section | covered |
| SC204 | [pattern] Shader grounds: tech only, the … (shortened) | cards-and-ui.md §Grounds | covered |
| SC205 | [later] Photographs: the client's first, else … (shortened) | later.md §Video | later |
| SC206 | [link] No URLs appear in this … (shortened) | none (the source file has no links) | covered |

### skills/taste-skill/references/layout-v4.md (23591 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| LY1 | [technique] Role of the file: the layout spec for every page; system.css holds tokens, section box, grid and hero frame; assets/layout holds heroes, deal and check tools. | system.md §Grid and frame | covered |
| LY2 | [technique] Link order: system.css first, then … (shortened) | place-pages.md §Actions and motion | covered |
| LY3 | [rule] Reference recordings of figma.com and … (shortened) | layout-and-heroes.md §Screens | covered |
| LY4 | [rule] Study of 327 sites at … (shortened) | layout-and-heroes.md §Screens | covered |
| LY5 | [rule] A section shows alone more … (shortened) | layout-and-heroes.md §Screens | covered |
| LY6 | [rule] The look comes from heights … (shortened) | layout-and-heroes.md §Screens | covered |
| LY7 | [rule] Judge tile: the shot is … (shortened) | layout-and-heroes.md §Screens | covered |
| LY8 | [rule] Shell: body renders only header.nav, … (shortened) | layout-and-heroes.md §Screens | covered |
| LY9 | [rule] Section box: height calc(var(--h,1) x … (shortened) | layout-and-heroes.md §Screens | covered |
| LY10 | [code] Section markup example: a section with id and inline --h 2 style, its .wrap holding the h2 first, then the content. | layout-and-heroes.md §Screens | covered |
| LY11 | [table] Content windows at 1440x900; columns "c at 1440x900" and "Screens"; six rows from under 360 up to over 1,608 with the action for each band. | layout-and-heroes.md §Screens | covered |
| LY12 | [rule] Phone (390, --padt 96): one … (shortened) | layout-and-heroes.md §Screens | covered |
| LY13 | [rule] Tablet 640 to 1023 (judges shoot 768x1024 and 820x1180): an oversize box pushes later sections off the grid, so stacked content is judged at 768x1024. | layout-and-heroes.md §Screens | covered |
| LY14 | [table] Tablet table; columns "c at … (shortened) | layout-and-heroes.md §Screens | covered |
| LY15 | [later] consistency.mjs with … (shortened) | later.md §Source kit | later |
| LY16 | [rule] The system's 48px tablet gutter … (shortened) | system.md §Tokens | covered |
| LY17 | [pattern] Two-screen group (.g2, or .g2m … (shortened) | layout-and-heroes.md §Screens | covered |
| LY18 | [rule] A total of 708 to … (shortened) | layout-and-heroes.md §Screens | covered |
| LY19 | [rule] Content is top-aligned: the h2 comes first at --padt (120; 96 on phone) below the section top; never centred vertically; never a second h2. | layout-and-heroes.md §Screens | covered |
| LY20 | [rule] Fill 0.55 or more; the … (shortened) | layout-and-heroes.md §Screens | covered |
| LY21 | [rule] Separation by ground change or … (shortened) | layout-and-heroes.md §Screens | covered |
| LY22 | [pattern] footer.closing is one screen: .wrap holds two children, row 1 the dealt close, row 2 links and legal row; .g2m allowed on phone; no separate closing band. | layout-and-heroes.md §Screens | covered |
| LY23 | [rule] No scroll tricks: no scroll-snap, … (shortened) | layout-and-heroes.md §Screens | covered |
| LY24 | [rule] photo-chapters moment: (hold plus one) … (shortened) | layout-and-heroes.md §Screens | covered |
| LY25 | [rule] Hero is exactly the first … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY26 | [rule] Hero content ends by y … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY27 | [rule] Hero structure: .wrap > .hero-text holds optional notice line, h1, p.hero__lead, at most two buttons, and the picture; no caption, second float card or third button style. | layout-and-heroes.md §Picking a hero | covered |
| LY28 | [rule] The h1 starts at y 120 (96 phone), runs three lines at most at every width, never below h2 size (28 to 60px on phone); a notice line sits 16px above it at 14px, 4.5:1. | layout-and-heroes.md §Picking a hero | covered |
| LY29 | [rule] The picture ends inside the hero: beside words in a split, behind them as a layer, or above or below only if the hero ends by H minus 24; a frame under words ends by y 836. | layout-and-heroes.md §Picking a hero | covered |
| LY30 | [rule] At 768 and 820 the … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY31 | [rule] Hero stacking details: .at-over pieces hide below 1024; the main piece gets a .fit width; bleeds use .frame--photo cover or a .stage--fade-b fade of 96px or more; test at 820x1180 and 768x1024. | layout-and-heroes.md §Picking a hero | covered |
| LY32 | [rule] Docked strip (software and product only): at most 96px, still, one row under content (logos with permission, rating line, or three facts); hidden on phone unless it ends by H minus 24 minus bar; service and place dock no | layout-and-heroes.md §Picking a hero | covered |
| LY33 | [rule] Phone hero: text first; a … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY34 | [rule] Allowed hero types: full-bleed still photo, product on a stage, inset frame, or statement followed by work; tech may use a film or 3D hero; elsewhere film is a still that plays on click. | layout-and-heroes.md §Hero catalogue | covered |
| LY35 | [rule] Never a slider or crossfade … (shortened) | layout-and-heroes.md §Screens | covered |
| LY36 | [rule] Hero pictures are the work … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY37 | [later] Hero dealer: node deal.mjs with … (shortened) | later.md §Source tooling | later |
| LY38 | [rule] Heroes are dealt by kind … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY39 | [rule] Games: --kind gaming with --has … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY40 | [rule] Product or hardware stand-ins pass … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY41 | [rule] A product page is dealt … (shortened) | layout-and-heroes.md §Picking a hero | covered |
| LY42 | [rule] Copy only the section element from hero-<id>.html demo files; their nav, other sections, footer and photographer credit line stay behind; hero-place's latte close-up is a demo only. | system.md §Phone action bar | covered |
| LY43 | [pattern] split hero: text span-5; picture … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY44 | [pattern] photo hero: full-bleed photo layer; … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY45 | [pattern] product hero: h1 across columns 1 to 7 on two lines, lead and buttons on columns 9 to 12; the product large on the ground across the wrap, edge to edge down to the fold, with its stage 24px above it. | layout-and-heroes.md §Hero catalogue | covered |
| LY46 | [pattern] editorial hero: headline is the … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY47 | [pattern] collage hero: text span-5; a … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY48 | [pattern] word hero: oversized h1 at … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY49 | [pattern] film hero: a cinema frame … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY50 | [pattern] statement hero: one calm 56px two-line sentence over the page ground with lead, buttons and four facts; phone 34px on three lines; no motion. | layout-and-heroes.md §Hero catalogue | covered |
| LY51 | [pattern] triptych hero: h1 at 52 … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY52 | [pattern] centred hero: pill, centred 72px … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY53 | [rule] Every hero is one screen … (shortened) | layout-and-heroes.md §Hero catalogue | covered |
| LY54 | [rule] Hero fails for: picture out to one viewport edge, hero taller than screen, visual above text on phone, words over a busy picture, second float card, slogan, or caption under the picture. | layout-and-heroes.md §Hero catalogue | covered |
| LY55 | [rule] Place hero: never dealt; one … (shortened) | layout-and-heroes.md §Place hero | covered |
| LY56 | [pattern] Place hero at 1440: .hero.hero--photo … (shortened) | layout-and-heroes.md §Place hero | covered |
| LY57 | [pattern] Shop or bookshop letterbox option: 1200 x 504 inside the column, 24px under the header (--photo 528px). | layout-and-heroes.md §Place hero | covered |
| LY58 | [rule] Place hero at 640 to 1023: photo at most 56vw tall, words stacked beneath it, hero ends by H minus 24. | layout-and-heroes.md §Place hero | covered |
| LY59 | [rule] Place hero at 390: photo at least 390x292 (grows with data-phone-fill to 390x488 at most); --hgap 24; h1 32/37 on three lines at most; sub-line 18/28; one 342x48 button; stack ends at H minus 24. | layout-and-heroes.md §Place hero | covered |
| LY60 | [rule] Place hero photo must be real and of this place in daylight (room from the door, counter, shopfront with customers, workshop, best room); never mood shots, scenery, cut-outs or hazy files. | layout-and-heroes.md §Place hero | covered |
| LY61 | [rule] The visit block is always screen two, never inside the first screen. | place-pages.md §Visit | covered |
| LY62 | [rule] One .wrap for header, sections … (shortened) | layout-and-heroes.md §Grid | covered |
| LY63 | [technique] 12-column grid with 24px gutter … (shortened) | layout-and-heroes.md §Grid | covered |
| LY64 | [technique] Place grid at 1200: starts … (shortened) | layout-and-heroes.md §Grid | covered |
| LY65 | [rule] Blocks start on the left … (shortened) | layout-and-heroes.md §Grid | covered |
| LY66 | [rule] Two text lines: the left … (shortened) | layout-and-heroes.md §Grid | covered |
| LY67 | [rule] Splits: text left, visual right, top-aligned, never mirrored or alternating; the h2 sits above the grid on the left line; filled columns pad 48px; phone text then visual, both 342 wide. | layout-and-heroes.md §Grid | covered |
| LY68 | [rule] Pictures span the viewport as … (shortened) | layout-and-heroes.md §Grid | covered |
| LY69 | [rule] Bleed is for layers only: … (shortened) | layout-and-heroes.md §Grid | covered |
| LY70 | [rule] Nothing crosses a section edge, … (shortened) | layout-and-heroes.md §Grid | covered |
| LY71 | [rule] 1024 to 1279: span-4 cards with panels go two-up; 640 to 1023: splits stack text first and panel cards take the full row; nothing scrolls sideways; no swipe rows. | layout-and-heroes.md §Grid | covered |
| LY72 | [later] Type dealing: start.mjs deal --page <kind> gives three Google pairings (take the first); start.mjs css writes the tokens; --axis for word or editorial heroes; start.mjs types lists every pairing with its link. | later.md §Source tooling | later |
| LY73 | [rule] One family, or a display … (shortened) | layout-and-heroes.md §Type sizes | covered |
| LY74 | [rule] Banned faces and looks: Inter, … (shortened) | system.md §One system | covered |
| LY75 | [rule] Weights: display at --display-weight (400 … (shortened) | layout-and-heroes.md §Type sizes | covered |
| LY76 | [rule] Never 700 or 800 (the letters moment excepted); no light weight under 20px; a static face such as Instrument Serif sets the nav tile in the display weight. | layout-and-heroes.md §Type sizes | covered |
| LY77 | [rule] Desktop and phone sizes: h1 … (shortened) | system.md §Type | covered |
| LY78 | [rule] Place sizes: h1 48/53 and … (shortened) | layout-and-heroes.md §Type sizes | covered |
| LY79 | [rule] Each size level is at … (shortened) | system.md §Type | covered |
| LY80 | [rule] Display text of 40px or … (shortened) | layout-and-heroes.md §Type sizes | covered |
| LY81 | [later] check.mjs run: headless Chrome via layout-check against index.html with a profile directory and sizes 1440x900, 1024x768, 820x1180, 768x1024, 390x844; --json and --shots options. | later.md §Source kit | later |
| LY82 | [table] Check findings table; columns "Finding" and "Means"; eight rows (hero-fold; hero-maxchars and hero-lines; screen-short and screen-height; sparse; neighbour and neighbour-ground; edge-left, edge-right, spill, bleed-one-si | layout-and-heroes.md §Checks | covered |
| LY83 | [rule] Run without --no-stress; every finding … (shortened) | layout-and-heroes.md §Checks | covered |
| LY84 | [later] In-page use: evaluate the layout-check … (shortened) | later.md §Source kit | later |
| LY85 | [link] No URLs appear in this file; Google Fonts is named but no link is given. | none (the source file has no links) | covered |

### skills/taste-skill/references/motion.md (19242 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| MO1 | [rule] Every page loads the motion layer: html data-motion, motion.css after ui/cards.css, motion.js as a module after system.js. Never removed or overridden. | moments-and-scenes.md §Moments | covered |
| MO2 | [rule] Missing or invisible hover layers count as faults. Since 2.5.1, a page without its hero entrance or dealt moment also counts as a fault. | motion.md §Where motion is allowed | covered |
| MO3 | [rule] Markup contract: linked card is .card holding its link (never .m-nolift); linked photo uses a.m-zoom around img; buttons .btn; running-text links .link. | motion.md §Hover and press | covered |
| MO4 | [rule] Motion moves in exactly three places: hero entrance once, one dealt moment per section, and the hover/press layer. Nothing else moves. | motion.md §Where motion is allowed | covered |
| MO5 | [rule] Tech/gaming/software pages may add card-visual loops, one timed hero or data-visual loop, one count, and the dealt effect. Other kinds get none of these. | motion.md §Where motion is allowed | covered |
| MO6 | [rule] Product render stays a still … (shortened) | motion.md §Where motion is allowed | covered |
| MO7 | [rule] Scrolling moves only the dealt … (shortened) | motion.md §Scroll | covered |
| MO8 | [rule] A moment may pin its … (shortened) | motion.md §Scroll | covered |
| MO9 | [rule] Each motion needs a one-line purpose in the plan; a motion with no purpose is cut. | motion.md §Where motion is allowed | covered |
| MO10 | [rule] Content is readable at rest, … (shortened) | motion.md §Where motion is allowed | covered |
| MO11 | [rule] Timing tokens: --m-in 150ms, --m-out 120ms, --m-press 90ms, --m-panel 200ms, --m-close 120ms, --m-slide 240ms. | motion.md §Tokens | covered |
| MO12 | [rule] Image tokens: --m-image 600ms in, --m-image-out 400ms. Cycle token --m-cycle is 3.2s. | motion.md §Tokens | covered |
| MO13 | [rule] Tech loop tokens: --m-roll 700ms, … (shortened) | motion.md §Tokens | covered |
| MO14 | [rule] UI … (shortened) | moments-and-scenes.md §Moments | covered |
| MO15 | [rule] Entrances … (shortened) | moments-and-scenes.md §Moments | covered |
| MO16 | [rule] --m-ease-io … (shortened) | motion.md §Tokens | covered |
| MO17 | [rule] No curve overshoots or bounces. | motion.md §Tokens | covered |
| MO18 | [rule] Motion layer animates only transform, scale and opacity. Hovers may also change colour. Width, height, top, left, margin and padding never animate. | motion.md §Tokens | covered |
| MO19 | [rule] Dealt moments may additionally animate clip-path (wipe), filter (photo developing), text colour, and on tech only background-position; each is named in meta.json. | moments-and-scenes.md §Moments | covered |
| MO20 | [rule] Distances: card lift 2px; photo … (shortened) | motion.md §Hover and press | covered |
| MO21 | [table] Button: fill steps 14% toward ink (outline gains faint fill and stronger border); box steps up 1px; press sinks to 1px below rest. Times 150ms in, 120ms out, 90ms press. Fine pointer only. | motion.md §Hover and press | covered |
| MO22 | [rule] Text-link secondary of the arrow … (shortened) | motion.md §Hover and press | covered |
| MO23 | [rule] Page CSS must never set a .btn's transform or transition. | motion.md §Hover and press | covered |
| MO24 | [table] Arrow (svg.m-arrow): moves 3px right … (shortened) | motion.md §Hover and press | covered |
| MO25 | [table] Link: running text and .link … (shortened) | motion.md §Hover and press | covered |
| MO26 | [table] Nav words rest bare, darken, … (shortened) | motion.md §Hover and press | covered |
| MO27 | [technique] Nav panel: opens after 150ms of hover intent, fades in with a 6px drop as one surface, closes in 120ms. Open panels swap at once. Chevron turns 180 degrees on tech, flips instantly elsewhere. | motion.md §Hover and press | covered |
| MO28 | [technique] Current page: a 2px bar under the nav word with aria-current="page"; no motion. | motion.md §Hover and press | covered |
| MO29 | [technique] Software tabs (click only): one indicator slides by transform in 240ms, starts scaled to the old tab and settles to scale 1. Panel swap at most 200ms; every panel fixed height. Other kinds have no tabs. | motion.md §Hover and press | covered |
| MO30 | [table] Card with link: lifts 2px, border darkens one step, optional soft shadow (blur 24px, 10% ink max, hover only); 180ms in, 120ms out. | motion.md §Hover and press | covered |
| MO31 | [rule] Card without a link: no motion; marked .m-nolift. | motion.md §Where motion is allowed | covered |
| MO32 | [table] Photo in linked card or … (shortened) | motion.md §Hover and press | covered |
| MO33 | [rule] Focus: 2px ring in the … (shortened) | motion.md §Hover and press | covered |
| MO34 | [table] Field: action border plus a 3px soft ring; 140ms. | motion.md §Hover and press | covered |
| MO35 | [technique] Switch (.m-switch) and check (.m-check) … (shortened) | motion.md §Hover and press | covered |
| MO36 | [technique] Copy button (tech): glyph swaps … (shortened) | motion.md §Hover and press | covered |
| MO37 | [rule] FAQs show every answer open; no accordion; height, max-height and padding never animate. | motion.md §Hover and press | covered |
| MO38 | [rule] Hooks: [data-m-loop], data-ui-loop, data-m-count (tech … (shortened) | motion.md §Hero entrance | covered |
| MO39 | [rule] Hover effects apply only to … (shortened) | motion.md §Hover and press | covered |
| MO40 | [rule] Every hover control also works … (shortened) | motion.md §Hover and press | covered |
| MO41 | [rule] Banned hover effects: rotate, skew, glow, shine sweep, chip glide. | motion.md §Hover and press | covered |
| MO42 | [technique] Hero entrance: h1 lines rise out of word masks, 700ms each, lines 80ms apart, at most 240ms from first to last line. | motion.md §Hero entrance | covered |
| MO43 | [technique] After the h1, the lead, buttons and facts fade up 12px, 520ms each, 60ms apart, starting once the last line is half up. | motion.md §Hero entrance | covered |
| MO44 | [rule] A line above the h1 (notice, pill) enters together with the first h1 line. | motion.md §Hero entrance | covered |
| MO45 | [technique] Hero picture never fades: photo … (shortened) | motion.md §Hero entrance | covered |
| MO46 | [rule] Whole hero entrance lasts about 1.1s, ease-out, transform/scale/opacity only, once per visit, never on scroll. | motion.md §Hero entrance | covered |
| MO47 | [rule] An h1 that layout.js reworks … (shortened) | moments-and-scenes.md §Moments | covered |
| MO48 | [code] Head snippet: adds m-enter class so words wait for motion.js, and m-enter-done after a 700ms fallback timer. Prevents text flash. | motion.md §Hero entrance | covered |
| MO49 | [code] Hero section markup: section with data-enter and aria-labelledby, marking the entrance target. | motion.md §Hero entrance | covered |
| MO50 | [rule] Optional attributes: data-enter-media on the … (shortened) | motion.md §Hero entrance | covered |
| MO51 | [technique] motion.js enter(): lends the h1 word masks during the entrance, then returns its nodes; sets .is-entering then .is-entered. | motion.md §Hero entrance | covered |
| MO52 | [rule] Words hide only while html.m-enter … (shortened) | motion.md §Hero entrance | covered |
| MO53 | [rule] Headless screenshots see the hero at rest unless html has data-motion="live". | motion.md §Hero entrance | covered |
| MO54 | [rule] Never a loader, gate, delay before reading, or second entrance. headline-arrives is retired. | motion.md §Hero entrance | covered |
| MO55 | [rule] Tech card loops: one cycle 2.5 to 4s (3.2s default), repeating; seeded on its finished picture; a ui.js fragment rests 600ms before its first cycle. | motion.md §Loops | covered |
| MO56 | [rule] Last 10 to 15% of … (shortened) | motion.md §Loops | covered |
| MO57 | [technique] Pointer or focus entering a card restarts its loop from the top, not within the first 800ms. A paused loop stays paused. Cards and windows never zoom, tilt or pan. | motion.md §Loops | covered |
| MO58 | [rule] One subject per cycle; one change every 1 to 2s, each change 300ms or less. Several subjects advance one per cycle. A label never shows two words. | motion.md §Loops | covered |
| MO59 | [rule] One fragment loop per card … (shortened) | motion.md §Loops | covered |
| MO60 | [rule] A small diagram's pulse is its own loop on the same cycle and restart/pause rules. Below the hero, never two loops on one screen; use data-ui-still or data-dg-still to hold a pulsing diagram. | motion.md §Loops | covered |
| MO61 | [rule] Page-own CSS loops sit in [data-m-loop], keyframes on var(--m-cycle), --m-still gives the finished frame, and a 48px --m-safe band is kept clear for the pause button. | motion.md §Loops | covered |
| MO62 | [rule] Life signs only inside the … (shortened) | motion.md §Loops | covered |
| MO63 | [rule] Card story kinds, each in a fixed-height box: prompt types 12 to 20 chars/s and holds; answer streams about one bubble a second; notification enters at top and oldest fades; checklist ticks about once a second; calendar  | motion.md §Loops | covered |
| MO64 | [rule] Speaker or avatar front item … (shortened) | motion.md §Loops | covered |
| MO65 | [rule] Ideas listed as not placed and therefore unused: stepping slot strip, before/after divider, path-following items, growing dock tab, pointer-linked mascot, comet on hero strand. | motion.md §Hero entrance | covered |
| MO66 | [rule] Tech budget: one timed loop per page (hero or data-visual frame, any form); plus at most one effect; a live hero effect forbids any other timed loop. Card loops, diagram pulses and dealt moments sit outside this count. | motion.md §Loops | covered |
| MO67 | [rule] One count per page (data-m-count or counter-rolls, never both): 1000ms on load, 1.2s at most, final figure in HTML; never a year, price or phone number; live counters change only last 1 to 3 digits. | motion.md §Loops | covered |
| MO68 | [rule] On tech, one load-once motion … (shortened) | motion.md §Where motion is allowed | covered |
| MO69 | [rule] Pause: anything moving 5s after being seen gets one 32px solid round button, 12px from bottom-right; shown on hover/focus or always; never over copy or on a still. ui.pausable(panel, ctrl) for custom movers. | moments-and-scenes.md §Moments | covered |
| MO70 | [rule] Timed loops start on load, never start/stop/resume on scroll; IntersectionObserver only mounts lazily. Canvases may skip off-screen drawing on a load-based clock. Hidden tabs may pause all. | motion.md §Loops | covered |
| MO71 | [rule] Outside the dealt moment's section … (shortened) | motion.md §Scroll | covered |
| MO72 | [rule] Scroll moments sit in data-moment sections (tech big scenes use data-big-scene with hold 1), 1H or 2H, pinned only with position: sticky. photo-chapters runs 3H or 4H live. | moments-and-scenes.md §Big scenes | covered |
| MO73 | [rule] Scroll moments scrub to the scrollbar (reversing upward) and show a finished state at both ends. Enter moments (picture-develops) run once, 1.6 to 1.8s. | motion.md §Scroll | covered |
| MO74 | [rule] Moment text stays visible without … (shortened) | moments-and-scenes.md §Moments | covered |
| MO75 | [rule] Phones run the light moments … (shortened) | moments-and-scenes.md §Moments | covered |
| MO76 | [rule] Moments never move cards, photos, pricing, FAQs, quotes or the footer. | moments-and-scenes.md §Moments | covered |
| MO77 | [technique] Allowed scroll drivers: native animation-timeline; … (shortened) | motion.md §Scroll | covered |
| MO78 | [rule] No smooth-scroll library (Lenis, Locomotive, … (shortened) | motion.md §Scroll | covered |
| MO79 | [technique] Header and phone bar look … (shortened) | motion.md §Scroll | covered |
| MO80 | [rule] Reduced motion: colours still change; menus fade; presses show a deeper tone; tab indicator and switch knob jump; underline appears without travel (transition-property limited to opacity and colours in motion.css). | motion.md §Reduced motion | covered |
| MO81 | [rule] Reduced motion: hero stands as … (shortened) | motion.md §Reduced motion | covered |
| MO82 | [rule] Phones (no hover, touch): card loops and effects hold a poster or finished frame; heavy canvases become stills; no hover states or pointer simulation; hero still enters; phone-light moments still run. | motion.md §Reduced motion | covered |
| MO83 | [rule] Never list: card reveals/tilts/flips/glows or follows the pointer; magnetic buttons; carousels, auto-advancing sliders, timed tabs, rotating notices, logo marquees. | motion.md §What never moves | covered |
| MO84 | [rule] Never list: random blinking, twinkle, glitter, flicker, hue cycling or scrambled text; every change must show a state, a step or real data. | motion.md §What never moves | covered |
| MO85 | [rule] Never list: a loop that … (shortened) | motion.md §Loops | covered |
| MO86 | [rule] Never list: hover slower than its token; overshooting ease; delay before a button reacts; animated focus ring; second underline or indicator style; animated width, height or margin. | motion.md §What never moves | covered |
| MO87 | [technique] Demo file assets/motion/demo.html shows every interaction (a check-by-eye artefact, not a script). | moments-and-scenes.md §Big scenes | covered |

### skills/taste-skill/references/moments.md (18173 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| MM1 | [rule] A moment is the award-style part of a page: one place, or two, that a visitor remembers, in its own section. Hero entrance and hover layer are the only other motion. | moments-and-scenes.md §Moments | covered |
| MM2 | [rule] Each moment is a folder assets/moments/<id>/ holding moment.js, moment.css, meta.json and demo.html; index.json, gallery.html and moments.js sit beside them. | moments-and-scenes.md §Moments | covered |
| MM3 | [rule] Eighteen folders: five retired (headline-arrives, … (shortened) | moments-and-scenes.md §Moments | covered |
| MM4 | [rule] Moment count: one on a … (shortened) | moments-and-scenes.md §Moments | covered |
| MM5 | [rule] Place with under 8 photographs … (shortened) | moments-and-scenes.md §Moments | covered |
| MM6 | [table] Place pool: photo-chapters, picture-develops (film), word-highlight. Look: photographs and type. | moments-and-scenes.md §Moments | covered |
| MM7 | [table] Product pool: photo-chapters, pinned-chapters, picture-develops … (shortened) | moments-and-scenes.md §Moments | covered |
| MM8 | [table] Service pool (firm, clinic, agency, trade): same four moments as product; look: photographs and type. | moments-and-scenes.md §Moments | covered |
| MM9 | [table] Software, gaming, tech: the eleven moments that list those kinds, which is every dealt moment except photo-chapters and picture-develops. | moments-and-scenes.md §Moments | covered |
| MM10 | [rule] Calm kinds get photo- or type-led moments because they move only in their own section, cost no WebGL, and read as calm. | moments-and-scenes.md §Moments | covered |
| MM11 | [rule] Excluded on place, product and service: liquid-hover, liquid-type, cursor-spotlight, iris-opens, line-carries-colour, letters-assemble, halftone picture-develops, giant-type-pass, marquee-row, counter-rolls. | moments-and-scenes.md §Moments | covered |
| MM12 | [rule] Long non-tech page: pairs a statement moment (word-highlight) with a section moment, or picture-develops with one chapters moment. | moments-and-scenes.md §Moments | covered |
| MM13 | [rule] photo-chapters and pinned-chapters never share … (shortened) | moments-and-scenes.md §Moments | covered |
| MM14 | [rule] On tech, a moment counts as one of the page's beats against the big scene. | moments-and-scenes.md §Big scenes | covered |
| MM15 | [code] Pick command for place/product/service: moments.mjs pick with --page, --count 1 or 2, --fits section,statement, --photo, and a history file. | moments-and-scenes.md §Moments | covered |
| MM16 | [code] Pick command for software/gaming/tech: same flags plus optional --scene, --effects, --contexts. | moments-and-scenes.md §Big scenes | covered |
| MM17 | [code] Tech hero moment: pick with … (shortened) | moments-and-scenes.md §Moments | covered |
| MM18 | [rule] --page accepts software, gaming, tech, … (shortened) | moments-and-scenes.md §Moments | covered |
| MM19 | [rule] --photo is required on place, product and service pages; without it, long pages cannot get two moments. | moments-and-scenes.md §Moments | covered |
| MM20 | [rule] --fits section,statement: letters, liquid type, word-highlight and counter only deal with the statement fit. | moments-and-scenes.md §Moments | covered |
| MM21 | [rule] No --exclude needed. picture-develops is dealt only in film look; print (halftone) look is used via data-moment-opts '{"look": "print"}' and never dealt. | moments-and-scenes.md §Moments | covered |
| MM22 | [rule] Hero moment (0 or 1) kept only if heroes.json lists it: liquid-hover (split, photo), cursor-spotlight (product, collage, film, centred), liquid-type (statement, tech, six words or fewer). Off on touch; reduced motion res | moments-and-scenes.md §Moments | covered |
| MM23 | [rule] WebGL budget: at most 4 live contexts. The deal sums the scene's webgl (from assets/scenes/index.json), each effect at one, and --contexts for others; it prints the total. | moments-and-scenes.md §Big scenes | covered |
| MM24 | [rule] Placement: moments in different sections; history read as cycles (empty after all fitting ones are dealt); no id straight after itself; the last three dealt stay out across a cycle end. | moments-and-scenes.md §Moments | covered |
| MM25 | [rule] Never two of one kind … (shortened) | moments-and-scenes.md §Moments | covered |
| MM26 | [rule] Plan must list each id, its section and its purpose. A moment with nothing to carry is redealt with it added to --exclude. | moments-and-scenes.md §Moments | covered |
| MM27 | [rule] Retired (weight 0): headline-arrives, closing-lift, and since 2.5.1 lines-rise, window-parallax, word-rotate. magnetic-button is gone. | moments-and-scenes.md §Moments | covered |
| MM28 | [table] counter-rolls: text, proof figures, once, never in a card; reduced motion shows the figures. | moments-and-scenes.md §Moments | covered |
| MM29 | [table] word-highlight: scroll, one statement; runs on phone; reduced motion shows whole statement in ink. | moments-and-scenes.md §Moments | covered |
| MM30 | [table] giant-type-pass: scroll, statement over a mid-to-dark photo (tech only); phone shows photo in letters at smaller type. | moments-and-scenes.md §Moments | covered |
| MM31 | [table] letters-assemble: scroll, 2 to 5 word statement set very large, letters fly into the line; reduced motion shows the statement as written. | moments-and-scenes.md §Moments | covered |
| MM32 | [table] pinned-chapters: scroll, feature section of 2 to 4 steps with two live screens; reduced motion shows static rows or steps with visuals under them. | moments-and-scenes.md §Moments | covered |
| MM33 | [table] marquee-row: scroll, row of real … (shortened) | moments-and-scenes.md §Moments | covered |
| MM34 | [table] line-carries-colour: transition on a new-ground … (shortened) | moments-and-scenes.md §Moments | covered |
| MM35 | [table] iris-opens: transition; an inset panel opens by a disc with a hairline accent ring; blocks show whole once the disc holds them. | moments-and-scenes.md §Moments | covered |
| MM36 | [table] picture-develops: enter moment, one large photo with clear subject, 1.6s, film look: rises from grey print, darks first, then colour. Runs on phone; reduced motion shows photo still. | moments-and-scenes.md §Moments | covered |
| MM37 | [table] photo-chapters: scroll, 3 to 5 … (shortened) | moments-and-scenes.md §Moments | covered |
| MM38 | [table] closing-lift: transition close with photograph; reduced motion gives a plain close. | moments-and-scenes.md §Moments | covered |
| MM39 | [table] cursor-spotlight: hover on hero frame; light rests under reduced motion. | moments-and-scenes.md §Moments | covered |
| MM40 | [table] liquid-type: headline ripples under the pointer via SVG filter, no WebGL; reduced motion shows headline as written. | moments-and-scenes.md §Moments | covered |
| MM41 | [table] liquid-hover: one photo with edges and detail, one WebGL context; plain photo with no canvas on phone and reduced motion. | moments-and-scenes.md §Moments | covered |
| MM42 | [rule] Every moment has phone and reduced-motion static states; lib.reduced() is true under prefers-reduced-motion or on a phone (under 640px wide, or touch screen under 500px tall sideways). | moments-and-scenes.md §Moments | covered |
| MM43 | [rule] Phone-runnable moments declare phone = … (shortened) | moments-and-scenes.md §Moments | covered |
| MM44 | [rule] Still answer is taken on mount; resizing across 640px applies next load; pinned-chapters and photo-chapters re-check on resize. | moments-and-scenes.md §Moments | covered |
| MM45 | [rule] Hover moments do nothing on touch screens. | moments-and-scenes.md §Moments | covered |
| MM46 | [rule] Moments never sit in cards, … (shortened) | moments-and-scenes.md §Moments | covered |
| MM47 | [rule] Host: a page section with data-moment="<id>" and options in data-moment-opts. Statement moments are one section with its h2 first; transitions are the whole new-ground section; a marquee or counter row merges as the last | moments-and-scenes.md §Moments | covered |
| MM48 | [rule] Heights: moments sit in one or two screen sections; photo-chapters is (hold+1) screens live (3 for three chapters, 4 for four or five) and must not get --h or data-screen. | moments-and-scenes.md §Moments | covered |
| MM49 | [code] Head snippet: adds mo-js class, mo-safe class after 2500ms, and modulepreload links for the loader, lib and the dealt moment. | moments-and-scenes.md §Moments | covered |
| MM50 | [code] Loader script tag: module moments.js at end of body, used on pages without system.js. | moments-and-scenes.md §Moments | covered |
| MM51 | [rule] Loader links each moment's CSS … (shortened) | moments-and-scenes.md §Moments | covered |
| MM52 | [rule] Moments use the page's tokens: … (shortened) | moments-and-scenes.md §Moments | covered |
| MM53 | [rule] Page models: … (shortened) | moments-and-scenes.md §Moments | covered |
| MM54 | [rule] data-moments-over and … (shortened) | moments-and-scenes.md §Moments | covered |
| MM55 | [rule] Scroll moments scrub inside their own 1 to 2 screen section, do one purposeful thing, and show a finished state at top and bottom; transitions finish before the section top is a fifth down the screen. | moments-and-scenes.md §Moments | covered |
| MM56 | [rule] consistency.mjs reports scroll findings inside a dealt [data-moment] as expected; any other scroll finding is a fault. | moments-and-scenes.md §Moments | covered |
| MM57 | [rule] Words are in HTML at their finished place; no moment hides a headline on load. | moments-and-scenes.md §Moments | covered |
| MM58 | [rule] Place, product and service moments use the client's own photos (or passing library photos), each used once; words are the page's real copy. | moments-and-scenes.md §Moments | covered |
| MM59 | [rule] One count per page: counter-rolls or data-m-count, never both. | moments-and-scenes.md §Moments | covered |
| MM60 | [rule] Nothing blinks, bounces or overshoots. Settle ease cubic-bezier(.22,1,.36,1); reveals 600 to 1000ms; photo develop 1.6 to 1.8s; a scrubbed wipe takes about half its chapter's share and holds the rest. | moments-and-scenes.md §Moments | covered |
| MM61 | [rule] Moment text sits in .container or .wrap like any section. Transition covers are inset panels with an even gutter, so headings, paragraphs, buttons and pictures are never cut by the line or disc. | moments-and-scenes.md §Moments | covered |
| MM62 | [rule] No captions; photo credits go in the footer line. | moments-and-scenes.md §Moments | covered |
| MM63 | [rule] Cost: only liquid-hover uses WebGL … (shortened) | moments-and-scenes.md §Moments | covered |
| MM64 | [rule] Photo tone: giant-type-pass and liquid-hover want mid-to-dark tones with edges. A pale dusk sky turns lavender in letters. Never violet or lavender. | moments-and-scenes.md §Moments | covered |
| MM65 | [code] moments.mjs check <page.html> with --page, --scene, --effects, --contexts: counts moments, repeats, retired ids, kind mismatches, card placement, figcaptions, avoiding pairs, slot repeats, WebGL total, missing loader. Ex | moments-and-scenes.md §Moments | covered |
| MM66 | [code] moments.mjs shoot with --out, --profile, --port, --only, --reduced: start, middle and end shots at 1440 and 390; checks the still rule under --reduced (STILL? on failure); --probe prints a JS value. [later] | moments-and-scenes.md §Moments | covered |
| MM67 | [rule] Headless Chrome draws WebGL on CPU: liquid-hover looks fainter, and its end state waits 6s to show the plain picture; text and scroll moments look the same on both. | moments-and-scenes.md §Moments | covered |

### skills/taste-skill/references/scenes.md (8705 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| SN1 | [rule] A big scene is a … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN2 | [rule] Tech pages only: software, tech (technical product, hardware, network) and gaming. Places, services and plain products never get a scene. | moments-and-scenes.md §Big scenes | covered |
| SN3 | [rule] At most one scene a page, and only if the brief meets its needs; never a stand-in picture to make one fit. | moments-and-scenes.md §Big scenes | covered |
| SN4 | [rule] A game without art files … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN5 | [rule] Deal at random among scenes … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN6 | [rule] A big scene is the … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN7 | [rule] Hero holds one screen; a scene becomes the hero only with restH 1. All three restH-2 hero scenes go below the hero as a two-screen section with an h2 heading. | moments-and-scenes.md §Big scenes | covered |
| SN8 | [rule] Object scenes … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN9 | [rule] Rest of page stays calm: one or two scroll moments may sit beside a scene, never in its section or the one beside it, never in its avoidMoments or twin. | moments-and-scenes.md §Moments | covered |
| SN10 | [table] Scene catalogue table: id, fits, types, needs, WebGL, restH, phone. Eleven scenes are listed. | moments-and-scenes.md §Big scenes | covered |
| SN11 | [technique] descend-through-weather: hero (below only), tech and gaming; needs two photos, high and low; no WebGL; restH 2; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN12 | [technique] shaped-window-over-fixed-world: hero (below only), tech and gaming; needs one wide photo of the world; no WebGL; restH 2; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN13 | [technique] fixed-hero-object: hero (below only), tech and gaming; needs an object render or cut-out with 1 to 4 chapters; one WebGL context; restH 2; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN14 | [technique] powers-of-ten-pullback: product, software and tech; needs the product UI at true size; no WebGL; restH 1; still on phone. Never the hero, since its first screen has no headline or action. | moments-and-scenes.md §Big scenes | covered |
| SN15 | [technique] product-assembles-into-its-action: product, software and tech; needs the screen as HTML in 4 to 6 steps; restH 1; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN16 | [technique] parts-lock-into-the-whole: product, software and tech; needs the screen cut along its panels; restH 1; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN17 | [technique] fly-into-the-shape: between or product; software, tech and gaming; needs the mark as one path and one dark photo; restH 1; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN18 | [technique] letter-physics: statement; software, tech and gaming; needs a claim and its answer; restH 1; light on phone. | moments-and-scenes.md §Big scenes | covered |
| SN19 | [technique] object-through-giant-type: statement; software, tech and gaming; needs a quote of 3 to 5 short lines and an object; one WebGL context; restH 1; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN20 | [technique] dot-becomes-the-full-stop: statement; … (shortened) | moments-and-scenes.md §Moments | covered |
| SN21 | [technique] letter-bar-floods-the-ground: between or statement; software, tech and gaming; needs two statements and an inverse section after; restH 1; still on phone. | moments-and-scenes.md §Big scenes | covered |
| SN22 | [rule] Live section is (hold+1) screens, 1800px at 1440x900 by default (hold 1). Scenes keep --h = restH as a minimum at rest; no fixed height; never data-screen="free". | moments-and-scenes.md §Big scenes | covered |
| SN23 | [rule] Under 768px every scene shows … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN24 | [rule] Reduced motion, no script or failed module: finished composition (the hold's end). Object scenes show their still picture and mount no WebGL. | moments-and-scenes.md §Big scenes | covered |
| SN25 | [rule] WebGL: one context per scene … (shortened) | moments-and-scenes.md §Moments | covered |
| SN26 | [rule] Never a GLSL ES reserved … (shortened) | performance.md §WebGL | expanded |
| SN27 | [rule] Text over photos stands on a flat band of the ground or the photo's calm dark part: 4.5:1 body, 3:1 display. No scrim or gradient over photos. | moments-and-scenes.md §Big scenes | covered |
| SN28 | [rule] Cost: animate transform, opacity and … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN29 | [rule] No explanatory captions; no card chrome, chips or labels moving with scroll. | moments-and-scenes.md §Moments | covered |
| SN30 | [rule] Nothing moving crosses words being … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN31 | [code] Head snippet: sc-js class marks script early with sc-safe after 2500ms, plus links to scenes.css and the scene's scene.css. | moments-and-scenes.md §Big scenes | covered |
| SN32 | [code] Section markup: class sc with … (shortened) | moments-and-scenes.md §Moments | covered |
| SN33 | [code] Runtime: module scenes.js at end of body; data-scenes-ready says mounted; data-scenes-over is a fault. | moments-and-scenes.md §Big scenes | covered |
| SN34 | [rule] Copy the scene folder plus … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN35 | [rule] Demo is a placeholder: pictures, words and objects are the client's; credit photos in the footer, marked "adapted" when cropped. | moments-and-scenes.md §Big scenes | covered |
| SN36 | [rule] Readability: scene words are real … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN37 | [rule] Native scroll only; the stage … (shortened) | moments-and-scenes.md §Big scenes | covered |
| SN38 | [rule] scene.js header comment holds markup and options; meta.json holds look, needs, never and avoidWith. | moments-and-scenes.md §Moments | covered |
| SN39 | [later] shoot.mjs (in assets/scenes/_demo): shoot start, … (shortened) | later.md §Source tooling | later |
| SN40 | [later] shoot.mjs index: writes the project's assets/scenes/index.json; refuses inside the installed skill unless --in-skill. Tooling. | later.md §Source tooling | later |

### skills/taste-skill/references/effects-usage.md (13591 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| EU1 | [rule] Scope: effects are anything shader, canvas, WebGL, print or scroll-driven (effect grounds, creative WebGL parts, objects, prints, big scenes, tech moments, film or 3D heroes, timed loops). cards.md wins card details; mot | grounds-and-effects.md §Who gets effects | covered |
| EU2 | [rule] Effects allowed only on tech, software (AI and dev tools count), gaming, and product pages with a technical subject (hardware, devices). | grounds-and-effects.md §Who gets effects | covered |
| EU3 | [rule] Banned on other kinds: canvas, … (shortened) | later.md §Source kit | later |
| EU4 | [rule] Also banned on other kinds: SVG animation, GIFs, Lottie, a custom cursor, scroll or animation libraries. | grounds-and-effects.md §Who gets effects | covered |
| EU5 | [rule] Allowed on other kinds: hero … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EU6 | [rule] Product without photos and without a 3D ask gets stand-in photographs. | grounds-and-effects.md §Who gets effects | covered |
| EU7 | [table] Per-kind table (tech vs product/service vs place): lead picture, the one effect, card panel grounds, moments, big scene, diagram cards, loops, CSS grounds. Tech allows 0 to 2 CSS grounds and 0 to 2 pulsing diagrams; othe | grounds-and-effects.md §Who gets effects | covered |
| EU8 | [rule] Subject before effect: an effect never stands where the product, device or game world belongs. Testing: a robot arm rendered as silk shader lost to a page showing the thing. | grounds-and-effects.md §Who gets effects | covered |
| EU9 | [rule] Hardware with no photos gets … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EU10 | [rule] With a 3D brief, the … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EU11 | [rule] Every non-effect visual is a real UI capture or real photograph; a photo is never filtered, printed, dithered or graded. | grounds-and-effects.md §Who gets effects | covered |
| EU12 | [rule] Tech budget: one effect means … (shortened) | grounds-and-effects.md §Budget | covered |
| EU13 | [rule] Card grounds: one card group may hold quiet still grounds from the effect's family, held as pictures. With a big scene, no data-fx outside a moment (checker MO-16, MO-23); panels take data-ground. | grounds-and-effects.md §Budget | covered |
| EU14 | [rule] Moments: up to two section … (shortened) | grounds-and-effects.md §Budget | covered |
| EU15 | [rule] Beats (effect, scene, moments) number up to three on tech; never two in one section or neighbouring ones; a calm section between; back third of the page calm before close. | grounds-and-effects.md §Budget | covered |
| EU16 | [rule] One pointer effect per page: … (shortened) | grounds-and-effects.md §Budget | covered |
| EU17 | [rule] At most four live WebGL contexts (effect plus moments' canvases); perf.mjs fails above four. | grounds-and-effects.md §Budget | covered |
| EU18 | [code] effects.mjs list: shows each id with family (quiet or focal) and slots. [later] | grounds-and-effects.md §Who gets effects | covered |
| EU19 | [code] effects.mjs pick for the hero slot (--slots hero) or the data-visual frame (--slots band), with --quiet, --seed and a history file. [later] | grounds-and-effects.md §Effects catalogue | covered |
| EU20 | [code] effects.mjs pick for one card group's still grounds, with --family matching the effect and --exclude listing the effect and the NOUI pattern list. [later] | grounds-and-effects.md §Who gets effects | covered |
| EU21 | [rule] NOUI exclusion list for UI … (shortened) | grounds-and-effects.md §Effects catalogue | covered |
| EU22 | [rule] Quiet grounds (even field behind … (shortened) | grounds-and-effects.md §Effects catalogue | covered |
| EU23 | [rule] At most two effect ids … (shortened) | grounds-and-effects.md §Effects catalogue | covered |
| EU24 | [rule] Effects on the inverse ground use an id made for the dark palette (--palette dark). If pick finds nothing for a slot, drop the slot. | grounds-and-effects.md §Effects catalogue | covered |
| EU25 | [rule] Retired or renamed ids: mesh-gradient … (shortened) | grounds-and-effects.md §Effects catalogue | covered |
| EU26 | [code] Node one-liner that deals one … (shortened) | later.md §Source tooling (the source's deal script is not shipped) | later |
| EU27 | [rule] Big scene dealt only from … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EU28 | [rule] A scene is the hero only when restH is 1; the three hero scenes go below the hero as two-screen sections. | grounds-and-effects.md §Placement | covered |
| EU29 | [rule] Scene height: hold 1 and --h = restH; no page CSS; stays one or two screens. | moments-and-scenes.md §Big scenes | covered |
| EU30 | [rule] Effect placement: hero frame (.frame--hero … (shortened) | grounds-and-effects.md §Placement | covered |
| EU31 | [rule] Hero with an effect in … (shortened) | grounds-and-effects.md §Placement | covered |
| EU32 | [technique] Split frame: .frame--split holding .stage; … (shortened) | grounds-and-effects.md §Placement | covered |
| EU33 | [rule] Text over an effect only … (shortened) | grounds-and-effects.md §Placement | covered |
| EU34 | [rule] html data-ground (tech) is given … (shortened) | grounds-and-effects.md §Placement | covered |
| EU35 | [rule] Video (tech only, hero or data-visual only): muted, inline, poster first, 6 to 12s loop or play-once with last frame held, pause button, separate phone and desktop files. Elsewhere, a still that opens the film on click.  | later.md §Video | later |
| EU36 | [rule] Effect motion: reacts to pointer or time; holds once assembled; ambient cycles 4s or longer; drifts a few px/s; 2 to 10% of pixels change per 0.9s; still at rest or has pause; poster first; still under reduced motion, on | grounds-and-effects.md §Motion and cost | covered |
| EU37 | [rule] No sound on entry; pointer-driven play turned off on touch. | grounds-and-effects.md §Motion and cost | covered |
| EU38 | [technique] Canvas sizing: draw 20 to … (shortened) | performance.md §WebGL | covered |
| EU39 | [technique] Noise ground: one baked texture drifted with time. Caustic net: its flat floor net only. | grounds-and-effects.md §Ground tokens | covered |
| EU40 | [rule] Blend modes only inside an … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EU41 | [rule] system.js mounts grounds through ui.grounds; … (shortened) | performance.md §WebGL | covered |
| EU42 | [rule] Never: an effect, print, grain, … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EU43 | [rule] Never: a caption explaining a visual; blinking or random effects; violet or lavender; copying a site's code, assets or signature device. | grounds-and-effects.md §Never | covered |

### skills/taste-skill/references/effects-creative.md (18582 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| EC1 | [rule] Effects can be parts of a page (feature-card picture, dither object, headline letters, button fill, border, icon chip, chart area, map). Each lives in assets/components/<name>/ with component.html, .css, .js, meta.json;  | effect-parts.md §Parts | covered |
| EC2 | [rule] Each part starts only while near the screen; index.html offers a palette switcher. | effect-parts.md §Parts | covered |
| EC3 | [rule] Parts are tech only, except fx-photo (all kinds, as plain photo) and fx-map (any kind with a door, baked still, only for a brief-given street). | effect-parts.md §Parts | covered |
| EC4 | [rule] fx-band is out: a drawn … (shortened) | effect-parts.md §Parts | covered |
| EC5 | [rule] Every WebGL-holding part is the … (shortened) | effect-parts.md §Parts | covered |
| EC6 | [rule] One pointer effect per page … (shortened) | grounds-and-effects.md §Budget | covered |
| EC7 | [rule] Everything else stays quiet: search … (shortened) | effect-parts.md §Parts | covered |
| EC8 | [rule] Glow only on a dark … (shortened) | effect-parts.md §Parts | covered |
| EC9 | [rule] Ray marching only in a … (shortened) | effect-parts.md §Parts | covered |
| EC10 | [rule] Nothing moves with scroll; cards … (shortened) | effect-parts.md §Parts | covered |
| EC11 | [rule] Cost target: a laptop's integrated GPU shares about 2 GB with everything; too many live canvases crash it. | grounds-and-effects.md §Motion and cost | covered |
| EC12 | [rule] At most 4 live WebGL … (shortened) | effect-parts.md §Parts | covered |
| EC13 | [technique] still() in shared.js draws a … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC14 | [rule] Never leave a still effect … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC15 | [rule] Screenshots must wait for stills: … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC16 | [rule] Per-pixel and ray-marched work at … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC17 | [rule] Everything pauses off screen and … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC18 | [rule] Contexts held: fx-dither-object (20fps), fx-prompt, … (shortened) | effect-parts.md §Parts | covered |
| EC19 | [technique] fx-feature-card: a 2x2 grid of … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC20 | [rule] Feature-card ground: painterly-landscape (default) or … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC21 | [rule] Each panel names its light … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC22 | [technique] Scene "day": pale sky over … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC23 | [technique] Scene "dusk": deep blue sky … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC24 | [technique] Scene "meadow": daylight photo look, clear blue sky paling to horizon, blue far ridge, sunlit grass field; sky takes page colour on blue pages; one per grid. | effect-parts.md §Feature-card panels | covered |
| EC25 | [rule] A grid of four mixes the lights, e.g. day, grain, dusk and meadow. | effect-parts.md §Feature-card panels | covered |
| EC26 | [technique] Grain panel: light warm ground under warm accent, deep ground under cool accent, page shades on colour pages. | effect-parts.md §Feature-card panels | covered |
| EC27 | [rule] Window shows the feature with … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC28 | [rule] At most two panels run a short pointer demo (glide, click, state change, rest), one per row. | effect-parts.md §Feature-card panels | covered |
| EC29 | [rule] Rejected: small dialog on empty ground; orb or sphere ground; landscape in accent hue only (reads as filter, orange turns rust); warm accent in dark ground; complementary accent on colour page (mud). | effect-parts.md §Feature-card panels | covered |
| EC30 | [technique] fx-dither-object: a real object built … (shortened) | effect-parts.md §Parts | covered |
| EC31 | [rule] Dither objects: headphones (on cups), … (shortened) | objects.md §Who gets an object | expanded |
| EC32 | [technique] Dither object motion: idle sway; pointed at, it turns to the pointer, light follows the pointer, and working parts respond (sound rings from cups, seat swivels, lens zooms and focus ring turns, rotors spin into discs and | effect-parts.md §Parts | covered |
| EC33 | [rule] Accent paints one part only (ear cups, seat and back, camera band and shutter, drone shell); shaded side is deep accent, never grey. | grounds-and-effects.md §Brand band | covered |
| EC34 | [rule] Only a product object the … (shortened) | effect-parts.md §Parts | covered |
| EC35 | [rule] A product none of the … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EC36 | [rule] data-cx-render="studio" is not for pages yet: edges stair-step at one sample per px; use the print or client photos. | objects.md §Who gets an object | expanded |
| EC37 | [rule] Reduced motion: one still picture, … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC38 | [rule] A dither object is a … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EC39 | [technique] fx-map: streets, water, parks, rails and stations of a real place drawn as a map app would; baked once at build time with bake.mjs (one Overpass request to OpenStreetMap), about 55KB (18KB gzipped) for 3x2 km; up to 14 s | effect-parts.md §Parts | covered |
| EC40 | [code] bake.mjs invocation with --lat, --lon, --out and --from (none by default; auto or lat,lon with --from-name adds a walk at 80 m/min from a station 150m to 1.6km away). Tooling. [later] | later.md §Source tooling (the source's map bake script is not shipped) | later |
| EC41 | [rule] Map data inlined as script type application/json with class cx-map__data, or named by data-cx-map. | grounds-and-effects.md §Named grounds | covered |
| EC42 | [rule] Map fits pin, walk and names in free space: right of the card from 900px width; under 900px the card sits below. Never closer than about 1 m per pixel; names on the side the walk does not use. | grounds-and-effects.md §Named grounds | covered |
| EC43 | [rule] Light map: white streets with … (shortened) | effect-parts.md §Parts | covered |
| EC44 | [technique] Map walk draws from station … (shortened) | effect-parts.md §Parts | covered |
| EC45 | [rule] Drawn only for a street … (shortened) | effect-parts.md §Parts | covered |
| EC46 | [link] https://www.openstreetmap.org/search?query=<street>+<district> is the Get directions target: a search URL with street and district, never coordinates or a route. | sections.md §Local business | covered |
| EC47 | [rule] Place pages bake with --from … (shortened) | effect-parts.md §Parts | covered |
| EC48 | [rule] No network at build time, … (shortened) | effect-parts.md §Parts | covered |
| EC49 | [technique] fx-photo: client photo in natural … (shortened) | effect-parts.md §Parts | covered |
| EC50 | [rule] fx-photo takes no filter (no halftone, dither, dissolve, print, duotone, blur; data-cx-grade stays off). Credit goes in the footer line. Its effects list is empty and data-cx-effect ignored; no WebGL; under reduced motio | grounds-and-effects.md §Who gets effects | covered |
| EC51 | [technique] windows(host, targets): one canvas seen … (shortened) | effect-parts.md §Parts | covered |
| EC52 | [technique] cx-ring: a host shown only … (shortened) | effect-parts.md §Parts | covered |
| EC53 | [technique] cx-glow: a host blurred into … (shortened) | grounds-and-effects.md §Recipes | covered |
| EC54 | [technique] pauser(host): a round pause button … (shortened) | grounds-and-effects.md §Motion and cost | covered |
| EC55 | [technique] fill(el, id): fills the glyphs … (shortened) | effect-parts.md §Parts | covered |
| EC56 | [table] Use/not-for table of 16 parts (fx-feature-card to fx-progress); each row says where the part fits and where it does not. | effect-parts.md §Parts | covered |
| EC57 | [technique] fx-headline: hero or closing line; fill 2 to 3 words; not body text or two filled lines per page. | effect-parts.md §Parts | covered |
| EC58 | [technique] fx-stat: 2 to 4 proof numbers from the brief at stat size (--t-stat, 38 at 1440); not small numbers, count-ups or invented figures. | effect-parts.md §Parts | covered |
| EC59 | [technique] fx-button: the one primary call … (shortened) | effect-parts.md §Parts | covered |
| EC60 | [technique] fx-prompt: hero prompt box for an AI or developer product; not ordinary forms. | effect-parts.md §Parts | covered |
| EC61 | [technique] fx-search: docs or command search, glowing only while focused. | effect-parts.md §Parts | covered |
| EC62 | [technique] fx-tabs: product tour or dashboard preview; not navigation. | effect-parts.md §Parts | covered |
| EC63 | [technique] fx-icon-tiles: feature grid with drawn glyphs; not brand logos. | effect-parts.md §Parts | covered |
| EC64 | [technique] fx-spotlight: a row of plain … (shortened) | effect-parts.md §Parts | covered |
| EC65 | [technique] fx-globe: products with global reach; not local businesses. | effect-parts.md §Parts | covered |
| EC66 | [technique] fx-map: visit or contact section showing real streets baked still; not a product without a place. | effect-parts.md §Parts | covered |
| EC67 | [technique] fx-chart: one metric over time; not decoration without numbers. | effect-parts.md §Parts | covered |
| EC68 | [technique] fx-bars: monthly figures on a … (shortened) | effect-parts.md §Parts | covered |
| EC69 | [technique] fx-photo: the client's own photo of the subject in colour; not mood stock, blank notebooks or filters. | effect-parts.md §Parts | covered |
| EC70 | [technique] fx-avatar: calls, presence or a team list; not static team grids. | effect-parts.md §Parts | covered |
| EC71 | [technique] fx-pricing: the recommended plan only, not all plans. | effect-parts.md §Parts | covered |
| EC72 | [technique] fx-progress: only inside a product … (shortened) | effect-parts.md §Parts | covered |
| EC73 | [rule] Panel grounds in feature cards: … (shortened) | effect-parts.md §Feature-card panels | covered |
| EC74 | [rule] Inside letters and digits: silk-folds … (shortened) | effect-parts.md §Parts | covered |
| EC75 | [rule] Inside small shapes (chips, pills, … (shortened) | effect-parts.md §Parts | covered |
| EC76 | [rule] Inside data: a plain accent … (shortened) | effect-parts.md §Parts | covered |
| EC77 | [rule] A map (fx-map) is baked streets, never an effect, with no fallback ground. | effect-parts.md §Parts | covered |
| EC78 | [rule] Each part keeps its own parameter table; pass only that effect's numbers (contour-lines' 0.32 opacity left dot-terrain nearly blank). | effect-parts.md §Parts | covered |
| EC79 | [rule] Part uses the page's effect … (shortened) | grounds-and-effects.md §Who gets effects | covered |
| EC80 | [rule] Retired effects … (shortened) | grounds-and-effects.md §Effects catalogue | covered |
| EC81 | [rule] Colour: every part reads page … (shortened) | effect-parts.md §Parts | covered |
| EC82 | [rule] No fixed hues except three natural ones: the meadow blue sky over grass, the dusk gold horizon, and the map's blue water and green parks. Never violet or lavender. | effect-parts.md §Parts | covered |
| EC83 | [code] Use: link … (shortened) | effect-parts.md §Parts | covered |
| EC84 | [rule] Numbers and names come from the brief; a missing figure is left out, never invented or tagged "sample". | effect-parts.md §Parts | covered |

### skills/taste-skill/references/effects-objects.md (23169 bytes)

| # | Source item | Our file § | Status |
|---|---|---|---|
| EO1 | [rule] Thirteen objects in three families plus one builder. Each family has a README as its contract and each object a meta.json of params; index.html and product-render/views.html show them. | objects.md §Families | covered |
| EO2 | [table] Family table: print objects, photo prints, scene objects, and product-render builder, each with its folder list and README pointer. | objects.md §Families | covered |
| EO3 | [technique] Print objects … (shortened) | objects.md §Families | covered |
| EO4 | [technique] Photo prints … (shortened) | objects.md §Families | covered |
| EO5 | [technique] Scene objects (split-reveal, dither-sequence, dot-object, … (shortened) | objects.md §Families | covered |
| EO6 | [technique] product-render builder: composes any physical … (shortened) | objects.md §Building a product spec | covered |
| EO7 | [rule] One strong object moment per … (shortened) | objects.md §Who gets an object | covered |
| EO8 | [rule] Place, service and every other … (shortened) | objects.md §Who gets an object | covered |
| EO9 | [rule] Physical product without photos: photographs … (shortened) | objects.md §Who gets an object | covered |
| EO10 | [rule] A render only when the … (shortened) | objects.md §Who gets an object | covered |
| EO11 | [rule] Renders never depict another kind … (shortened) | objects.md §Who gets an object | covered |
| EO12 | [rule] A game without art: hero is its name large over a stand-in photo of its setting (deal.mjs software gaming, setting, photo hero); world section is the widest photo full bleed. Render only if the brief asks for 3D. | objects.md §Who gets an object | covered |
| EO13 | [rule] Software, AI and games with … (shortened) | objects.md §Who gets an object | covered |
| EO14 | [rule] Photo prints and photo scenes stay in the kit gallery, never on a page; product-turntable only when its form is the product's own. | objects.md §Families | covered |
| EO15 | [code] Print mount markup: panel with … (shortened) | later.md §Source kit (mount markup of the source's print core) | later |
| EO16 | [rule] Photo scenes mount with data-scene … (shortened) | objects.md §Families | covered |
| EO17 | [technique] Script API: obj.mount(el, opts). Print objects take place, params and palette; photo prints and scenes take src, params and palette. Controllers have pause, resume, setPalette and destroy. | objects.md §Placement | covered |
| EO18 | [rule] Print placements: card large, cut … (shortened) | objects.md §Placement | covered |
| EO19 | [rule] Palette from tokens --bg, --surface, … (shortened) | objects.md §Palette and motion | covered |
| EO20 | [rule] Turning or looping object gets … (shortened) | objects.md §Palette and motion | covered |
| EO21 | [rule] Credits: photos go in the … (shortened) | objects.md §Never | covered |
| EO22 | [technique] product-render build.js turns a JSON … (shortened) | objects.md §Building a product spec | covered |
| EO23 | [later] Tooling and demos in the product-render and objects folders: auto.js mounts, make-posters.mjs checks specs and writes posters, views.html and demo.html show worked specs and turntable. | later.md §Source kit | later |
| EO24 | [code] Product mount markup: frame div with data-product pointing to a spec under assets/objects, data-product-place stage, and the auto.js module. | objects.md §Building a product spec | covered |
| EO25 | [rule] data-product spec URL stays under … (shortened) | objects.md §Building a product spec | covered |
| EO26 | [table] data-product-place fill shares: stage 0.86, … (shortened) | objects.md §Placement | covered |
| EO27 | [rule] No place lays words over the product. The stage place in the product hero spans the wrap with the frame 7% past top and bottom (layout.css 3b). Data-product frames lose fill, border and padding and stand on the page grou | objects.md §Placement | covered |
| EO28 | [table] Attributes: data-product-view (three-quarter default, side, … (shortened) | objects.md §Client renders | covered |
| EO29 | [rule] data-product-params JSON overrides a place's preset (angle, step 0 to switch a lamp off, size, x, y offsets). | objects.md §Client renders | covered |
| EO30 | [rule] data-product-palette takes bg, surface, ink, accent; aria-label overrides the spec label; render sets role img (button when a click switches it); failed load sets data-product-error. | objects.md §Client renders | covered |
| EO31 | [technique] Script API: loadProduct(url) then mount with place, params, palette; controller methods pause, resume, step, set, setPalette (null after theme switch) and destroy; auto.js exports products, ready and mountAll. | objects.md §Palette and motion | covered |
| EO32 | [rule] Each section gets a different view; the whole product appears in at most three sections; the view is named on its plan line. | objects.md §Who gets an object | covered |
| EO33 | [table] View keys: standard views (three-quarter at spec angle, side, side-left, front, rear, top, low as supported); detail:<part> close-ups; the spec's own views; scenes; colors; make; lamp light (click light, pool). | objects.md §Client renders | covered |
| EO34 | [technique] Spec-defined views: a named detail view can select parts by name prefix or wildcard, set angle, elevation and margin, and start from a standard view. | objects.md §Client renders | covered |
| EO35 | [technique] Spec scenes: a product in … (shortened) | objects.md §Building a product spec | covered |
| EO36 | [technique] Colourways: list of id, name, accent and optional material swaps; parts painted "color": "accent" re-light with the chosen accent. | objects.md §Client renders | covered |
| EO37 | [technique] make key: variants and grounds … (shortened) | objects.md §Building a product spec | covered |
| EO38 | [technique] Lamp light: spec click "light" with a pool position; data-product-params step 0 turns it off. | objects.md §Building a product spec | covered |
| EO39 | [rule] Swatches: data-product-swatch on colour buttons names the frames they drive, value is the colour id; click swaps to that colour's still and keeps aria-pressed. Or dispatch product:set with a color detail. Every colour of | objects.md §Client renders | covered |
| EO40 | [rule] Stills: make-posters writes images in specs/stills/ named by poster, variant and colour (-half in srcset, -dark on dark ground) and a stills.json index. No canvas or WebGL on the page by default. | objects.md §Client renders | covered |
| EO41 | [rule] Modes: auto shows the still (needs make-posters first); image shows still only; still renders once at frame size as an img and frees its context; live turns. Close-ups keep sides where the rest runs off the frame edge. | objects.md §Client renders | covered |
| EO42 | [rule] Frame attributes for checkers: data-product-mode, … (shortened) | objects.md §Client renders | covered |
| EO43 | [rule] Big products: render sits on … (shortened) | objects.md §Placement | covered |
| EO44 | [rule] Phones (max-width 700px or coarse … (shortened) | objects.md §Client renders | covered |
| EO45 | [rule] A turning product has a … (shortened) | objects.md §Building a product spec | covered |
| EO46 | [rule] Cost: each part is evaluated … (shortened) | objects.md §Budget | covered |
| EO47 | [rule] Cannot render: text or logos … (shortened) | objects.md §Building a product spec | covered |
| EO48 | [rule] Craft: include the details that … (shortened) | objects.md §Building a product spec | covered |
| EO49 | [rule] Never a product of another … (shortened) | objects.md §Who gets an object | covered |
| EO50 | [code] make-posters.mjs invocation: spec path with profile, port, variants, grounds, px and legacy options; writes fallback PNGs, stills and stills.json; exits 1 on a fault. [later] | objects.md §Building a product spec | covered |
| EO51 | [code] make-posters.mjs --check: validates a spec (parts, views, scenes, shader words) without a browser. [later] | objects.md §Building a product spec | covered |
| EO52 | [rule] Posters take one to four minutes per variant for 60 to 90 parts on CPU; --timeout keeps finished variants; --variants merges with the manifest. | objects.md §Budget | covered |
| EO53 | [rule] Poster shows at once and … (shortened) | objects.md §Client renders | covered |
| EO54 | [table] Spec keys: id, name, label, poster, angle (default -32), turn (sway default amp 26 period 22; spin speed; still), camera elev, click light, pool, materials, motion, parts. | objects.md §Building a product spec | covered |
| EO55 | [code] City-bike spec example: id, name, label, units, angle, a sway turn, an accent-painted frame material, and parts for a wheel and a tube. Demonstrates the JSON format only. | objects.md §Building a product spec | covered |
| EO56 | [rule] Axes: x is front, y … (shortened) | objects.md §Building a product spec | covered |
| EO57 | [rule] Every part takes mat, blend (fillet), in (motion group) and name; placed by from and to (up turns the section) or by at with axis and rot; seams cut panel lines on tube, beam, box or cylinder. | objects.md §Building a product spec | covered |
| EO58 | [table] Part types tube, beam, box and panel: sizes and uses (frame tubes, bars, housings, plates). | objects.md §Building a product spec | covered |
| EO59 | [table] Part types cylinder/disc, sphere/ellipsoid and torus: sizes and uses (bases, hubs, lenses; bulbs, knobs; rings, chainrings, status lights). | objects.md §Building a product spec | covered |
| EO60 | [table] Part types joint, wheel, shade and seat: sizes and uses (hinges; bikes, casters; lampshades, horns; saddles, cushions). | objects.md §Building a product spec | covered |
| EO61 | [table] Part types basket, arc, spring and path: sizes and uses (baskets, bins; mudguards, hoops; springs, cords; handles, cables, bent tubes). | objects.md §Building a product spec | covered |
| EO62 | [table] Material kinds: paint (accent-capable), metal, … (shortened) | objects.md §Building a product spec | covered |
| EO63 | [rule] Built-in material names: accent, paint, … (shortened) | objects.md §Building a product spec | covered |
| EO64 | [rule] Motion: up to four groups … (shortened) | objects.md §Building a product spec | covered |
| EO65 | [rule] Spec faults: unknown part type, … (shortened) | objects.md §Building a product spec | covered |
| EO66 | [table] GPU cost by family: print objects high per frame (share 2 contexts); photo prints low, one each, up to 3; scenes low, at most 2; product render stills none, live 1. | objects.md §Budget | covered |
| EO67 | [rule] Overall at most 4 live … (shortened) | objects.md §Budget | covered |
| EO68 | [rule] Never: captions or apologies on … (shortened) | objects.md §Palette and motion | covered |
| EO69 | [rule] Never over the hero photograph … (shortened) | objects.md §Who gets an object | covered |
| EO70 | [later] _print-core/lint-glsl.mjs and … (shortened) | later.md §Source tooling | later |
| EO71 | [later] deal.mjs: referenced as the command that picks product or game hero variants (--type, --kind, --has). Tooling, not read here. | later.md §Source tooling | later |
| EO72 | [later] photos.mjs: search for stand-in photographs and credits output. Tooling, not read here. | later.md §Source tooling | later |

### 1. Repo root

| # | Source item | Our file § | Status |
|---|---|---|---|
| RR1 | [rule] LICENSE is MIT, copyright Leonxlnx 2026; the repo ships one skill, design-taste-frontend. | index.md (intro) | covered |
| RR2 | [pattern] README pitch: company sites at figma.com and x.ai level, real photos and UI, browser-checked. | principles.md §The bar | covered |
| RR3 | [rule] README requires Node 22+ and … (shortened) | later.md §Source tooling | later |
| RR4 | [pattern] README build flow: classify business kind, deal palette and hero, real UI and photos, effects only on tech pages, browser check. | principles.md §Deal | covered |
| RR5 | [pattern] Business kinds named in README: software, gaming, tech, product, service, place; effects restricted to software, tech, gaming. | principles.md §The bar | covered |
| RR6 | [later] Install paths: npx skills add, Claude Code marketplace, Codex marketplace, or install.sh symlink from a clone. | later.md §Source tooling | later |
| RR7 | [link] https://github.com/vercel-labs/agent-skills - the npx skills CLI the README install uses. | later.md §Source tooling | later |
| RR8 | [link] https://github.com/Leonxlnx/taste-skill-classics - new home of seven classic skills, same install names. | later.md §Source kit | later |
| RR9 | [link] https://github.com/Leonxlnx/imagegen-skills - home of imagegen-frontend-web/mobile, brandkit and image-to-code. | none (another repository of the source author; not website craft) | later |
| RR10 | [link] https://github.com/Leonxlnx/unlazy - named as the replacement for the removed full-output-enforcement skill. | none (another repository of the source author; not website craft) | later |
| RR11 | [link] https://tastecode.dev - TasteCode desktop app with a built-in design agent, advertised in README. | later.md §Video | later |
| RR12 | [link] https://tasteskill.dev - project website, linked from the README badge row. | none (the source project's own website; not website craft) | later |
| RR13 | [link] https://github.com/Leonxlnx/taste-skill/releases/tag/v2.0.0 - v2.0.0 launch film, linked from README. | later.md §Video | later |
| RR14 | [link] https://github.com/sponsors/Leonxlnx - sponsorship page; README also lists sponsor logos (Kimi, Vercel OSS, interfaces.dev, React Bits, IMG.LY, Sent.dm). | later.md §Source tooling | later |
| RR15 | [later] install.sh (bash, about 150 lines): symlinks each skill into ~/.claude/skills or ~/.codex/skills; flags --list, --uninstall, --all-agents. | later.md §Source tooling | later |
| RR16 | [later] install.sh on Windows Git Bash … (shortened) | later.md §Source kit | later |
| RR17 | [later] CHANGELOG 2.5.1 (2026-11-07): finish gate loops until checker clean; hero motion on every page; stand-in photos for products; trade palettes. | later.md §Source tooling | later |
| RR18 | [later] CHANGELOG 2.5.0 (2026-11-05): full rebuild for company-site bar; one page system; kind routing; UI fragments; browser checker. | later.md §Source kit | later |
| RR19 | [later] CHANGELOG 2.1.5 (2026-10-25): community fixes: escaped chart text, keyboard access, italic font loading, dev-server warning. | later.md §Source tooling | later |
| RR20 | [later] CHANGELOG 2.1.4 (2026-10-20): one inspector run no longer deletes another run's live browser profile. | later.md §Source kit | later |
| RR21 | [later] CHANGELOG 2.1.3 (2026-10-19): classic skills moved to their own repo; pointer folders and stale files removed. | later.md §Source kit | later |
| RR22 | [later] CHANGELOG 2.1.2 (2026-10-19): fixed unquoted YAML in SKILL.md that made the skill silently drop; added frontmatter CI test. | later.md §Source tooling | later |
| RR23 | [later] .github/workflows/check-skills.yml: on push to main and on pull requests, Node 22, runs the three tests/*.mjs and a syntax check of every script. | later.md §Source tooling | later |
| RR24 | [later] tests/frontmatter.mjs: strictly parses each SKILL.md frontmatter; checks kebab-case name, 64 max, description at 1024 characters max. | later.md §Source tooling | later |
| RR25 | [later] tests/text-encoding.mjs: fails on double-encoded (mojibake) UTF-8 in text files, lists up to 20 lines. | later.md §Source tooling | later |
| RR26 | [later] tests/kit-clean.mjs: runs consistency.mjs and layout check.mjs on each shipped demo page at 1440 and 390; --demos, --no-layout flags. | later.md §Source kit | later |
| RR27 | [later] .claude-plugin/marketplace.json: marketplace entry, plugin taste-skill 2.5.1, skills ./skills/taste-skill. | later.md §Source kit | later |
| RR28 | [later] .codex-plugin/plugin.json: version 2.5.1, skills ./skills/, Codex interface text and three default prompts. | later.md §Source tooling | later |
| RR29 | [later] .agents/plugins/marketplace.json: Codex marketplace pointing at the git repo, ref main, installation AVAILABLE. | later.md §Source kit | later |
| RR30 | [link] examples/v2/CREDITS.md: 52 credited photographs and films for four example pages (Nachtschicht, Bohne & Söhne, Atelier Nord, Margin). | photos.md §Captions and credits | covered |
| RR31 | [link] CREDITS hosts: 48 entries on https://commons.wikimedia.org, 3 on https://www.metmuseum.org, 1 on https://www.flickr.com. | photos.md §Stand-ins | covered |
| RR32 | [rule] CREDITS licences: CC0, public domain, CC BY, CC BY 2.0 and CC BY-SA variants, each with photographer and source page. | later.md §Source kit | covered |

### 2. skills/taste-skill/scripts (10 .mjs, 2 templates, plus library/ data)

| # | Source item | Our file § | Status |
|---|---|---|---|
| SX33 | [later] consistency.mjs (11,485 lines): real-browser checker over HTTP at 1440, 1024, 768, 390; PASS, WARN or FAIL per check. | later.md §Source tooling | later |
| SX34 | [rule] consistency categories: layout, containment, text, nav, buttons, motion, visuals, copy, wiring, leftovers, system, ink, render, screens. | later.md §Source tooling | later |
| SX35 | [rule] consistency numbers: body text 7:1 … (shortened) | later.md §Source tooling | later |
| SX36 | [later] copy-lint.mjs: counts AI-written copy tells in a page, folder or draft; exit 1 on any FAIL. | scripts/ultlib/copylint.py (later.md §Shipped kit) | covered |
| SX37 | [rule] copy-lint FAILs: chatbot residue (lorem ipsum, "certainly!", [NEED]), markdown leaks, old slop words, stock phrases, devices used as tics. | scripts/ultlib/copylint.py: residue, worn word, stock line and capped-device rules; no markdown-leak rule yet | covered |
| SX38 | [rule] copy-lint WARNs: over-budget devices, virtue words (honest, calm, genuine), stock cast names and company names. | later.md §Source tooling | later |
| SX39 | [table] copy-lint finding ids: 28 ids … (shortened) | scripts/ultlib/copylint.py: our own rule names, not the source's ids | covered |
| SX40 | [later] gate.mjs (891 lines): finish gate, one GATE line per run, hook modes for claude, codex and antigravity. | later.md §Source tooling | later |
| SX41 | [rule] gate runs: consistency --quick at 1440 and 390 (plus 320), layout check at 1440x900 and 390x844, kit-edited and checker-gaming static checks, copy-lint. | later.md §Source tooling | later |
| SX42 | [rule] gate holds two WARNs as FAILs: hero-enter and moment-none; up to 3 rounds; waivers capped at 5 in .taste-skill/waivers.json. | later.md §Source kit | later |
| SX43 | [rule] gate exit codes: 0 PASS, … (shortened) | later.md §Source tooling | later |
| SX44 | [later] effects.mjs: effects kit CLI with index, list, pick, gallery, publish, serve, shot and perf subcommands. | later.md §Source kit | later |
| SX45 | [later] moments.mjs: moments CLI with index, list, pick (by page kind), check, gallery, shoot and sheet subcommands. | later.md §Source kit | later |
| SX46 | [later] photos.mjs: library photo CLI with list, pick (detail slots, one-in-three cap), search (Wikimedia Commons), fetch, credits. | later.md §Source kit | later |
| SX47 | [later] icons.mjs: resolves brand, file-type and UI icons into local SVG files; find, apps, fetch, scan, check, measure. | later.md §Source kit | later |
| SX48 | [later] start.mjs: deals palettes and Google … (shortened) | later.md §Source tooling | later |
| SX49 | [later] perf.mjs: one headless Chrome run at 1440x900 and 390x844; bytes, requests, fonts, images, WebGL contexts, LCP, long tasks. | later.md §Source tooling | later |
| SX50 | [later] shoot.mjs: full-page screenshot with live effects, stitched in Node; per-section tiles at 1440 and phone width. | later.md §Source tooling | later |
| SX51 | [code] fx-gallery.template.html: template for the effects gallery page (palette switcher, cards); rendered by effects.mjs. | later.md §Source kit | later |
| SX52 | [code] fx-lab.template.html: template for the effects lab page, with a slider for every effect parameter. | later.md §Source kit | later |
| SX53 | [table] library/palettes.json and library/type.json: palettes by trade and font pairings, read by start.mjs (header only). | later.md §Source tooling | later |

### 3. skills/taste-skill/assets

| # | Source item | Our file § | Status |
|---|---|---|---|

### backgrounds/ (16 CSS grounds; backgrounds.css, backgrounds.js, pick.mjs, check.mjs, check.html, demo.html, index.json)

| # | Source item | Our file § | Status |
|---|---|---|---|
| ABA54 | [code] pick.mjs deals grounds per section; check.mjs measures ink and muted contrast from real pixels. | grounds-and-effects.md §Named grounds | covered |
| ABA55 | [technique] Grounds drawn in CSS; only "liquid" animates (two drifting blobs, transforms only). | grounds-and-effects.md §Named grounds | covered |
| ABA56 | [pattern] Kinds: soft, hard, page, panel; roles: hero, body, proof, band, close, footer. | grounds-and-effects.md §Named grounds | covered |
| ABA57 | [pattern] mist: airy two-hue colour wash, soft kind. halo: one light behind a centred line. | grounds-and-effects.md §Named grounds | covered |
| ABA58 | [pattern] grain: tinted field with fine film grain, hard kind. | grounds-and-effects.md §Named grounds | covered |
| ABA59 | [pattern] paper: page ground with fine grain, never flat; page kind. | grounds-and-effects.md §Ground tokens | covered |
| ABA60 | [pattern] dusk: one tone melts into the next with no edge. | grounds-and-effects.md §Named grounds | covered |
| ABA61 | [pattern] topglow: clean light under the nav; page kind. | grounds-and-effects.md §Named grounds | covered |
| ABA62 | [pattern] ruled: precise grid as the page's own frame. | grounds-and-effects.md §Named grounds | covered |
| ABA63 | [pattern] dots: dot field in margins and corners, clear behind headings. | grounds-and-effects.md §Named grounds | covered |
| ABA64 | [pattern] arcs: rings rising from below, as on x.ai's footer, for closing calls. | grounds-and-effects.md §Named grounds | covered |
| ABA65 | [pattern] band: coloured band in the second tone, lit from one corner. | grounds-and-effects.md §Brand band | covered |
| ABA66 | [pattern] field: grainy gradient in one colour family, hard kind. | grounds-and-effects.md §Named grounds | covered |
| ABA67 | [pattern] stage: vivid grainy mesh that one card floats on; panel kind. | grounds-and-effects.md §Named grounds | covered |
| ABA68 | [pattern] photo: calm photograph under a quiet scrim; media band or hero. | grounds-and-effects.md §Named grounds | covered |
| ABA69 | [pattern] horizon: dark band with a … (shortened) | grounds-and-effects.md §Named grounds | covered |
| ABA70 | [pattern] deep: near-black with cool pool at top and lit lip. | grounds-and-effects.md §Named grounds | covered |
| ABA71 | [pattern] liquid: two slow blobs in neighbouring hues; the only animated ground. | grounds-and-effects.md §Named grounds | covered |

### components/ (20 fx-* components; base.css, shared.js, index.html, _lab.html)

| # | Source item | Our file § | Status |
|---|---|---|---|
| ACO72 | [code] shared.js: four ways an effect shows outside a background: fill (glyphs), windows (holes), ring (border), background. | effect-parts.md §Parts | covered |
| ACO73 | [code] fx-avatar: speaker ring showing an effect in a thin border. | effect-parts.md §Parts | covered |
| ACO74 | [code] fx-band: divider band (the ridgeline effect). | grounds-and-effects.md §Never | expanded |
| ACO75 | [code] fx-bars: bar chart with grain-filled bars. | effect-parts.md §Parts | covered |
| ACO76 | [code] fx-button: button whose label shows an effect. | effect-parts.md §Parts | covered |
| ACO77 | [code] fx-chart: area chart filled with an effect. | effect-parts.md §Parts | covered |
| ACO78 | [code] fx-dither-object: objects rendered in dither. | objects.md §Families | covered |
| ACO79 | [code] fx-feature-card: feature cards with inset effect panels. | effect-parts.md §Feature-card panels | covered |
| ACO80 | [code] fx-globe: globe data card. | effect-parts.md §Parts | covered |
| ACO81 | [code] fx-headline: headline whose letters show an effect. | effect-parts.md §Parts | covered |
| ACO82 | [code] fx-icon-tiles: icon tiles on effect grounds. | effect-parts.md §Parts | covered |
| ACO83 | [code] fx-logos: logo row with a light sweep. | grounds-and-effects.md §Never | expanded |
| ACO84 | [code] fx-map: street map of the place. | effect-parts.md §Parts | covered |
| ACO85 | [code] fx-photo: photograph with copy. | effect-parts.md §Parts | covered |
| ACO86 | [code] fx-pricing: pricing card with an effect border. | effect-parts.md §Parts | covered |
| ACO87 | [code] fx-progress: import progress bar with a light fill. | effect-parts.md §Parts | covered |
| ACO88 | [code] fx-prompt: prompt field with edge glow. | effect-parts.md §Parts | covered |
| ACO89 | [code] fx-search: search field with ambient glow. | effect-parts.md §Parts | covered |
| ACO90 | [code] fx-spotlight: spotlight cards. | effect-parts.md §Parts | covered |
| ACO91 | [code] fx-stat: stat numbers filled with an effect. | effect-parts.md §Parts | covered |
| ACO92 | [code] fx-tabs: tabs with a grain indicator. | effect-parts.md §Parts | covered |

### diagrams/ (diagram.js, diagram.css, mount.js, presets.json, demo.html, lab.html)

| # | Source item | Our file § | Status |
|---|---|---|---|
| ADI93 | [code] diagram.js: node-and-line visuals with play, pause, seek and destroy; mount.js draws every [data-diagram]. | icons-and-diagrams.md §Diagrams | covered |
| ADI94 | [table] presets.json: 27 presets in ten layouts: hub, ring, tree, lanes, fanin, bowtie, sync, timeline, grid, free. | icons-and-diagrams.md §Diagrams | covered |
| ADI95 | [technique] Animated node-and-line drawing; the drawing method itself was not read (unverified). | icons-and-diagrams.md §Dimension drawing | covered |

### effects/ (25 effects; fx.js, pick.js, index.json, README.md, gallery.html, lab.html)

| # | Source item | Our file § | Status |
|---|---|---|---|
| AEF96 | [rule] Mount with data-fx and a sized element; colours come from palette tokens; text on effects reads 4.5:1. | grounds-and-effects.md §Effects catalogue | covered |
| AEF97 | [rule] Never a fixed hue or violet; four effects are named-only: dotted-globe, duotone-grade, edge-glow, ridgeline. | grounds-and-effects.md §Effects catalogue | covered |
| AEF98 | [rule] An effect is dealt once per slot per page; avoidWith pairs never share a page. | grounds-and-effects.md §Effects catalogue | covered |
| AEF99 | [technique] 21 effects use the fx.shader WebGL fragment helper; ascii-shade and grid-pulse are 2D canvas; ridgeline and dotted-globe mix 2D and WebGL. | grounds-and-effects.md §Effects catalogue | covered |
| AEF100 | [code] film-light-leak: light bleeds from one frame edge with moving film grain (WebGL). | grounds-and-effects.md §Named grounds | covered |
| AEF101 | [code] grain-gradient: soft page-coloured shapes drifting under fine grain (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF102 | [code] ascii-shade: slowly turning sphere drawn from monospace characters (2D canvas). | grounds-and-effects.md §Effects catalogue | covered |
| AEF103 | [code] bayer-dither: soft glow rendered in ordered-dither square pixels (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF104 | [code] halftone-screen: gradient or lit sphere printed as a rotated round-dot screen (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF105 | [code] line-engraving: parallel lines swelling in shadows over hills or a sphere (WebGL, still motion). | grounds-and-effects.md §Motion and cost | covered |
| AEF106 | [code] aurora-curtains: S-curved light curtains over a night sky; dark and colour only (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF107 | [code] gradient-mesh: soft colour islands over a folding surface, optional mesh grid (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF108 | [code] painterly-landscape: out-of-focus landscape in broad dabs, sky and hills (WebGL). | grounds-and-effects.md §Recipes | covered |
| AEF109 | [code] god-rays: light shafts through haze with drifting motes (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF110 | [code] orb-sphere: one lit sphere with a turning nebula and bright rim (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF111 | [code] prism-dispersion: white beam splits into a spectrum on a far wall; dark only (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF112 | [code] soft-light-bars: four to seven soft upright light bars beside an empty area (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF113 | [code] spotlight-cone: slanted stage light through haze, landing as a pool (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF114 | [code] caustics: drifting net of water-caustic light lines on a pool floor (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF115 | [code] edge-glow: light running around a card or prompt border (named only, WebGL). | grounds-and-effects.md §Named grounds | covered |
| AEF116 | [code] dot-terrain: rolling land drawn as a laser-scan point cloud (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF117 | [code] grid-pulse: hairline grid with signals running along lines (2D canvas). | grounds-and-effects.md §Effects catalogue | covered |
| AEF118 | [code] ruled-grounds: fine dot ruling with crosses and a drifting soft light (WebGL). | grounds-and-effects.md §Named grounds | covered |
| AEF119 | [code] contour-lines: topographic contour lines with accent index lines (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF120 | [code] dotted-globe: dotted globe with real continents and arcs (named only; WebGL and 2D). | grounds-and-effects.md §Named grounds | covered |
| AEF121 | [code] ridgeline: stacked thin lines rising into peaks, one accent line (named only; 2D and WebGL). | grounds-and-effects.md §Named grounds | covered |
| AEF122 | [code] fluted-glass: ribbed glass whose ribs bend what is behind (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF123 | [code] silk-folds: satin folds in one colour with a sheen (WebGL). | grounds-and-effects.md §Effects catalogue | covered |
| AEF124 | [code] duotone-grade: section photograph graded to two or three tones with grain (named only; WebGL). | grounds-and-effects.md §Named grounds | covered |

### icons/ (index.json, icon.css, demo.html, demo/)

| # | Source item | Our file § | Status |
|---|---|---|---|
| AIC125 | [table] Sets: logos (gilbarbara/logos, CC0, full colour), si (Simple Icons 16.30.0, CC0, fallback), file (vscode-icons 1.2.30, MIT), ui (Lucide 1.2.100, ISC). | icons-and-diagrams.md §Icon sets | covered |
| AIC126 | [table] index.json: 458 curated apps, 38 file types, 435 UI glyphs; scripts/icons.mjs resolves them. | icons-and-diagrams.md §Icon sets | covered |
| AIC127 | [link] https://github.com/gilbarbara/logos - source of colour brand marks, pinned commit in icons.mjs. | icons-and-diagrams.md §Icon sets | covered |
| AIC128 | [link] https://github.com/simple-icons/simple-icons - one-colour fallback marks, CC0. | icons-and-diagrams.md §Icon sets | covered |
| AIC129 | [code] demo/ holds a 928-icon demo set with icons-credits.json (462 CC0, 432 ISC, 34 MIT); a demo, not shipped content. | icons-and-diagrams.md §Icon sets | covered |

### layout/ (11 heroes; deal.mjs, check.mjs, layout-check.js, layout.js, layout.css, heroes.json, fonts.html, demo.css, img/)

| # | Source item | Our file § | Status |
|---|---|---|---|
| ALA130 | [rule] A place hero is never dealt; place always prints hero-place; other types are weighted in heroes.json. | layout-and-heroes.md §Place hero | covered |
| ALA131 | [table] heroes.json: 11 hero layouts: place, split, photo, product, editorial, collage, word, film, statement, triptych, centred. | layout-and-heroes.md §Hero catalogue | covered |
| ALA132 | [code] hero-place: photograph under the header, words beneath (Recipe 3). | layout-and-heroes.md §Picking a hero | covered |
| ALA133 | [code] hero-split: words left, picture on the right. | layout-and-heroes.md §Hero catalogue | covered |
| ALA134 | [code] hero-photo: full-bleed photograph, words on its calm side. | layout-and-heroes.md §Hero catalogue | covered |
| ALA135 | [code] hero-product: product stage with one object. | page-plans.md §Product | covered |
| ALA136 | [code] hero-editorial: large type with pictures set in the line. | layout-and-heroes.md §Type sizes | covered |
| ALA137 | [code] hero-collage: UI collage cut by its frame. | layout-and-heroes.md §Hero catalogue | covered |
| ALA138 | [code] hero-word: oversized headline with one live word that rotates every two seconds (layout.js). | layout-and-heroes.md §Hero catalogue | covered |
| ALA139 | [code] hero-film: cinema frame with the film poster and the words on it. | layout-and-heroes.md §Hero catalogue | covered |
| ALA140 | [code] hero-statement: quiet statement over a ground. | layout-and-heroes.md §Hero catalogue | covered |
| ALA141 | [code] hero-triptych: headline, collage and button, Figma-style hero. | layout-and-heroes.md §Hero catalogue | covered |
| ALA142 | [code] hero-centred: centred headline over one window, x.ai-style hero. | layout-and-heroes.md §Hero catalogue | covered |
| ALA143 | [technique] CSS grid and clamp() type; layout.js adds letter weight near the pointer on variable-font axes. | layout-and-heroes.md §Type sizes | covered |

### moments/ (13 live moments; moments.js, lib.js, index.json, gallery.html, _demo/)

| # | Source item | Our file § | Status |
|---|---|---|---|
| AMO144 | [rule] Each moment declares a kind; place, product and service pages get photo- or type-led moments only, zero WebGL. | moments-and-scenes.md §Moments | covered |
| AMO145 | [rule] One moment on a short … (shortened) | moments-and-scenes.md §Moments | covered |
| AMO146 | [code] counter-rolls: proof digits roll once … (shortened) | moments-and-scenes.md §Moments | covered |
| AMO147 | [code] cursor-spotlight: soft light and dot grid follows the pointer with lag (hover, JS and rAF). | moments-and-scenes.md §Moments | covered |
| AMO148 | [code] giant-type-pass: giant words show a photograph through the letters as the section scrolls (scroll). | moments-and-scenes.md §Moments | covered |
| AMO149 | [code] iris-opens: inset panel in the old ground opens over a new ground (transition, scroll). | moments-and-scenes.md §Moments | covered |
| AMO150 | [code] letters-assemble: large statement letters fly in from scattered positions as it scrolls (scroll). | moments-and-scenes.md §Moments | covered |
| AMO151 | [code] line-carries-colour: inset panel with a colour line carries the ground change (transition). | moments-and-scenes.md §Moments | covered |
| AMO152 | [code] liquid-hover: pointer pushes a photograph like water (WebGL, liquid). | moments-and-scenes.md §Moments | covered |
| AMO153 | [code] liquid-type: headline ripples under the pointer via one SVG filter, then settles (liquid). | moments-and-scenes.md §Moments | covered |
| AMO154 | [code] marquee-row: slow looping row of client words or trades, pauses under pointer (scroll). | moments-and-scenes.md §Moments | covered |
| AMO155 | [code] photo-chapters: three to five photographs uncovered one by one; no WebGL, no canvas (scroll). | moments-and-scenes.md §Moments | covered |
| AMO156 | [code] picture-develops: photograph develops as it enters, film look on place pages (2D canvas). | moments-and-scenes.md §Moments | covered |
| AMO157 | [code] pinned-chapters: section holds two screens while three steps open beside one changing frame (scroll). | moments-and-scenes.md §Moments | covered |
| AMO158 | [code] word-highlight: statement turns from half ink to full ink word by word (scroll). | moments-and-scenes.md §Moments | covered |
| AMO159 | [later] Retired, not dealt: closing-lift (needs own footer.closing layout), headline-arrives (duplicates hero entrance). | later.md §Source kit | later |
| AMO160 | [later] Retired, not dealt: lines-rise (repeats hero entrance), window-parallax (template parallax), word-rotate (duplicates word hero). | later.md §Source kit | later |

### motion/ (motion.css, motion.js, demo.html, _hover-test.html, meta.json)

| # | Source item | Our file § | Status |
|---|---|---|---|
| AMO161 | [rule] Buttons lift 1px on hover and press 1px on click; hover-out 120ms against 150ms in (changelog). | motion.md §Hover and press | covered |
| AMO162 | [rule] One ease-out curve (cubic-bezier .2,.8,.2,1), no overshoot; hover only on fine pointers; transform-only moves. | motion.md §Hover and press | covered |
| AMO163 | [technique] CSS transitions; JS for count-up (data-m-count), CSS loops (data-m-loop), tab indicator and hero entrance (data-enter). | motion.md §Hero entrance | covered |

### objects/ (print, scene, photo-print and product objects; index.html)

| # | Source item | Our file § | Status |
|---|---|---|---|
| AOB164 | [code] print-cup: porcelain cup and saucer, halftone or engraving print; rings run on click (WebGL raymarch). | objects.md §Families | covered |
| AOB165 | [code] print-wheel: road wheel with 24 spokes, halftone; spins up on click. | objects.md §Families | covered |
| AOB166 | [code] print-lamp: balanced-arm desk lamp, halftone; switches on when clicked. | objects.md §Families | covered |
| AOB167 | [code] print-globe: desk globe with coastlines, engraving; spins on its own. | objects.md §Families | covered |
| AOB168 | [code] print-cards: playing cards, ace of diamonds up; halftone; fan out on click. | objects.md §Families | covered |
| AOB169 | [code] photo-halftone: photograph as round dots on a 45 degree screen; loupe shows colour. | objects.md §Families | covered |
| AOB170 | [code] photo-engraving: photograph as diagonal engraved lines that part around the pointer. | objects.md §Families | covered |
| AOB171 | [code] photo-dither: photograph in a three-colour grain; photo develops under the pointer. | objects.md §Families | covered |
| AOB172 | [code] split-reveal: one photograph half-printed as halftone with a draggable dividing line. | objects.md §Families | covered |
| AOB173 | [code] dither-sequence: two to six related photographs dithered and wiped one to the next. | objects.md §Families | covered |
| AOB174 | [code] dot-object: object cut from its … (shortened) | objects.md §Who gets an object | covered |
| AOB175 | [code] exploded-layers: photograph split into four printed sheets in perspective; sheets open. | objects.md §Families | covered |
| AOB176 | [code] product-turntable: generic camera, chair, speaker … (shortened) | objects.md §Families | covered |
| AOB177 | [code] product-render (folder): studio 3D render built from a JSON part spec; specs city-bike, desk-lamp, robot-arm. | objects.md §Building a product spec | covered |
| AOB178 | [rule] _print-core, _scenes README rules: prints … (shortened) | objects.md §Families | covered |
| AOB179 | [rule] Product renders only when the … (shortened) | objects.md §Who gets an object | covered |
| AOB180 | [rule] Object budgets: about two WebGL contexts for prints; scene contexts capped at two; page total kept at four. | objects.md §Budget | covered |
| AOB181 | [technique] Shared runtimes _print-core (print3d.js raymarch with GLSL), _scenes (kit.js), photo-kit (photo.js); posters shown when WebGL fails. | later.md §Source kit | covered |

### photos/ (photos.json, img/ with 66 WebP files)

| # | Source item | Our file § | Status |
|---|---|---|---|
| APH182 | [table] photos.json: 413 entries; 274 Unsplash (served via Lorem Picsum), 139 Wikimedia Commons. | later.md §Source kit (the source's photo library is not shipped; live search instead, photos.md §Sources, in order) | later |
| APH183 | [table] Commons licences: CC0 53, CC BY-SA 4.0 39, CC BY 2.0 22, CC BY-SA 3.0 12, CC BY-SA 2.0 6, CC BY 4.0 2, Public Domain Mark 1.0 2, others 4. | photos.md §Stand-ins | covered |
| APH184 | [link] https://unsplash.com/license - licence named for all Unsplash entries. | later.md §Source kit (goes with the photo library) | later |
| APH185 | [link] https://picsum.photos - host serving the Unsplash photographs in the library. | photos.md §Where photos lead | covered |
| APH186 | [table] 16 trades: cafe, hotel, bike, … (shortened) | later.md §Source kit (goes with the photo library) | later |
| APH187 | [rule] Library frames are stand-ins for detail slots only; never a client's room, product, shopfront or people. | photos.md §Stand-ins | covered |

### scenes/ (11 big scenes, scenes.js, scenes.css, lib.js, print.js, _demo/)

| # | Source item | Our file § | Status |
|---|---|---|---|
| ASC188 | [rule] Scenes are a function of scroll position, using transforms, opacity and clip-paths; no GSAP; page scrolls natively. | moments-and-scenes.md §Big scenes | covered |
| ASC189 | [code] descend-through-weather: first screen sinks through clouds onto a place photograph below. | moments-and-scenes.md §Moments | covered |
| ASC190 | [code] dot-becomes-the-full-stop: large dot drops and the claim grows word by word from it. | moments-and-scenes.md §Big scenes | covered |
| ASC191 | [code] fixed-hero-object: product stays fixed and turns with scroll as chapters pass beneath (WebGL). | moments-and-scenes.md §Moments | covered |
| ASC192 | [code] fly-into-the-shape: brand mark clip holding the next photograph rises and fills the screen. | moments-and-scenes.md §Moments | covered |
| ASC193 | [code] letter-bar-floods-the-ground: display statement with one straight letter; camera zooms on it (canvas mentioned). | moments-and-scenes.md §Big scenes | covered |
| ASC194 | [code] letter-physics: bold claim breaks apart in 3D, letters flying off their own lines. | moments-and-scenes.md §Moments | covered |
| ASC195 | [code] object-through-giant-type: quote in huge capitals with an object falling through it (WebGL). | moments-and-scenes.md §Moments | covered |
| ASC196 | [code] parts-lock-into-the-whole: one huge word steps into the product's own interface. | moments-and-scenes.md §Big scenes | covered |
| ASC197 | [code] powers-of-ten-pullback: product interface pulls back in log-scaled steps. | moments-and-scenes.md §Big scenes | covered |
| ASC198 | [code] product-assembles-into-its-action: working screen builds itself in story order while the page holds. | moments-and-scenes.md §Moments | covered |
| ASC199 | [code] shaped-window-over-fixed-world: fixed photograph behind a shutter with two tall windows cut out. | moments-and-scenes.md §Moments | covered |

### ui/ (19 fragments; ui.js, cards.css, base.css, cards.html, index.html, _lab/, index.json, icons/)

| # | Source item | Our file § | Status |
|---|---|---|---|
| AUI200 | [code] ui.js loads fragments into [data-ui-load] placeholders; cards.css gives feature-card panels. | cards-and-ui.md §Interface fragments | covered |
| AUI201 | [code] window: product window with sidebar counts and a conversation list that updates rows. | cards-and-ui.md §Interface fragments | covered |
| AUI202 | [code] chat: assistant answer typed word by word with two source chips. | kit/ui/chat.html, static (the answer shows whole; no word-by-word typing) | covered |
| AUI203 | [code] cursor: drafted refund reply; pointer glides, clicks, status turns Sent. | cards-and-ui.md §Interface fragments | covered |
| AUI204 | [code] notify: three notifications with avatars; a new one slides in. | cards-and-ui.md §Interface fragments | covered |
| AUI205 | [code] toggles: titled rule list, one switch flips at a time. | cards-and-ui.md §Interface fragments | covered |
| AUI206 | [code] stat: dashboard card with one big number and 14 daily bars. | cards-and-ui.md §The card | covered |
| AUI207 | [code] search: command bar with typed query and stepping selection. | cards-and-ui.md §Interface fragments | covered |
| AUI208 | [code] integrations: list of apps with real marks, what each does, and state. | cards-and-ui.md §Interface fragments | covered |
| AUI209 | [code] slider: design-tool property card with two sliders and a switch. | cards-and-ui.md §The card | covered |
| AUI210 | [code] voice: call card with timer, orb and word-by-word captions. | cards-and-ui.md §The card | covered |
| AUI211 | [code] files: status pill over a grid of real app file tiles. | cards-and-ui.md §Placements | covered |
| AUI212 | [code] calendar: month with a dated range and key-date rows. | cards-and-ui.md §Calendar | covered |
| AUI213 | [code] code: editor pane with two tabs and one highlighted line. | cards-and-ui.md §Interface fragments | covered |
| AUI214 | [code] diff-review: one pull-request file with +/- counts and line changes. | cards-and-ui.md §Interface fragments | covered |
| AUI215 | [code] terminal-run: terminal pane running tests with a thin progress meter. | cards-and-ui.md §Interface fragments | covered |
| AUI216 | [code] doc: document page with marked phrases and a note on the current one. | cards-and-ui.md §Interface fragments | covered |
| AUI217 | [code] checklist: five-step list whose steps tick in turn with a progress bar. | cards-and-ui.md §Interface fragments | covered |
| AUI218 | [code] pipeline-board: CI run card with status chip, commit and cancel button. | cards-and-ui.md §The card | covered |
| AUI219 | [code] apps: fourteen real app marks … (shortened) | cards-and-ui.md §Interface fragments | covered |
| AUI220 | [table] ui/icons/icons-credits.json: 30 SVG marks, 29 CC0 and 1 MIT, sourced from gilbarbara/logos and simple-icons. | icons-and-diagrams.md §Icon sets | covered |

### Top-level assets

| # | Source item | Our file § | Status |
|---|---|---|---|
| AT221 | [code] starter.html: page template; data-type, data-radius, data-ground, data-buttons, data-motion set on html; bracket placeholders like [Name]. | system.md §One system | covered |
| AT222 | [code] system.js: phone nav sheet, accordion, Escape, tabs, FAQ answers open, opening hours marked by time zone. | later.md §Source kit (behaviour script; our page parts each carry their own small script) | later |
| AT223 | [table] system.css palette: --p-bg, --p-surface, --p-ink, --p-muted, --p-accent, --p-accent-ink, --p-action, --p-action-ink, plus eight --p-inv-* inverse tokens. | kit/system.css (later.md §Shipped kit) | covered |
| AT224 | [table] system.css lit ground: --ground-bg, --ground-surface, --ground-ink, --ground-muted, --ground-accent, set per data-ground. | grounds-and-effects.md §Ground tokens | covered |
| AT225 | [table] system.css fonts: --font-display, --font-text, --font-mono; … (shortened) | performance.md §Fonts | covered |
| AT226 | [table] system.css type scale: --t-label 13, --t-small 14, --t-body 16, --t-lead 18, --t-card 18, --t-h3 24, --t-h2 30 to 48, --t-h1 38 to 72, --t-stat 28 to 38px. | system.md §Type | covered |
| AT227 | [table] system.css spacing: --s-1 to --s-10, … (shortened) | system.md §Spacing | covered |
| AT228 | [table] system.css radii: soft --r-sm 8, --r-md 12, --r-lg 20, --r-btn 8; sharp and round sets via data-radius. | system.md §Radius | covered |
| AT229 | [table] system.css layout tokens: --container 1280px, … (shortened) | kit/system.css (later.md §Shipped kit) | covered |
| AT230 | [table] system.css controls: --btn-h 44px, --btn-h-sm 36px, --icon 16px, --card-pad 16px, --card-gap 16px, --line and --line-strong via color-mix. | system.md §Buttons | covered |
| AT231 | [table] system.css motion: --ease cubic-bezier(.2, .8, .2, 1) (one curve), --dur 180ms. | motion.md §Tokens | covered |

## Totals

| Status | Rows |
|---|---|
| covered | 1518 |
| later | 157 |
| merged | 36 |
| expanded | 29 |

The 129 rows first matched only by keyword (`covered (check)`) were each reopened against the source and our files in the taste-2 pass: pointers now name the exact section; 5 became `expanded` (new rules on GLSL reserved words, hardware prints, the studio render, divider bands and logo sweeps), 2 `merged`, 11 `later`, 111 `covered` (source tooling, the photo library and notes with nothing to carry).

Kit pass (taste-2 steps 2 to 6): 8 `later` rows became `covered` now that our own kit ships the piece (phone frame L26, icon page I32, diagram page D3, copy lint SX36, SX37, SX39, CT4, CV26), and 3 `covered` rows were repointed from `later.md` to the kit file (AT223, AT229, AUI202). The rest of the kit gap is listed in `later.md` § Source kit still to do.

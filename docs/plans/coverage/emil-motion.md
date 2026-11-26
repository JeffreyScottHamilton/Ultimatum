# Coverage: emil-motion

Source: emilkowalski/skills at commit 715c180 (MIT, LICENSE read). Read only; none of its code was run. Rebuilt in our own words in `plugins/ultimatum/skills/website/references/craft/emil-motion/` with tables in `plugins/ultimatum/data/craft/emil-motion/`.

## Inventory (bytes)

| File | Bytes |
|---|---|
| `.gitattributes` | 68 |
| `.gitignore` | 10 |
| `.pl` | 0 |
| `LICENSE` | 1070 |
| `README.md` | 5223 |
| `performance-cheatsheet.md` | 932 |
| `ui-cheatsheet.md` | 1344 |
| `skills/animate/SKILL.md` | 11910 |
| `skills/animate/RECIPES.md` | 7957 |
| `skills/animate-expo/SKILL.md` | 17891 |
| `skills/animate-expo/RECIPES.md` | 16808 |
| `skills/animation-performance/SKILL.md` | 14269 |
| `skills/animation-vocabulary/SKILL.md` | 13425 |
| `skills/apple-design/SKILL.md` | 23036 |
| `skills/ask-sonner/SKILL.md` | 7233 |
| `skills/ask-sonner/API.md` | 4545 |
| `skills/break-ui/SKILL.md` | 14380 |
| `skills/break-ui/CATALOG.md` | 8268 |
| `skills/choreograph/SKILL.md` | 15958 |
| `skills/choreograph/RECIPES.md` | 10147 |
| `skills/emil-design-eng/SKILL.md` | 27509 |
| `skills/find-animation-opportunities/SKILL.md` | 9808 |
| `skills/gestures/SKILL.md` | 8632 |
| `skills/improve-animations/SKILL.md` | 8208 |
| `skills/improve-animations/AUDIT.md` | 7632 |
| `skills/improve-animations/PLAN-TEMPLATE.md` | 3100 |
| `skills/mobile-native/SKILL.md` | 16838 |
| `skills/pick-ui-library/SKILL.md` | 4790 |
| `skills/prototype/SKILL.md` | 7830 |
| `skills/prototype/PICKER.md` | 7548 |
| `skills/remove-animations/SKILL.md` | 11345 |
| `skills/review-animations/SKILL.md` | 8491 |
| `skills/review-animations/STANDARDS.md` | 9964 |
| `skills/write-swift/SKILL.md` | 42445 |

Total 348,614 bytes. Source skills are grouped by their folder in the table below.

## Coverage map

| Source skill | Item | Our file and section | Status |
|---|---|---|---|
| animate | Frequency gate, purpose, function check | gate.md § 1. Frequency | expanded |
| animate | Easing decision order, custom strong curves | easing-and-duration.md § Pick the easing | covered |
| animate | Duration budgets, asymmetric timing | easing-and-duration.md § Duration budgets | covered |
| animate | Property choice, tool ladder (CSS, WAAPI, library) | components.md § Choose the tool, cheapest first | covered |
| animate | Recipes: press, popover, tooltip, dialog, drawer, toast, accordion, tab, reveal, slider | components.md | covered |
| animate | Reduced motion and hover gating | reduced-motion.md | expanded |
| animate | Overlap with house motion rules | skills/work/references/design/motion.md § 1, § 9; craft/taste/motion.md | merged with existing motion files |
| animation-performance | Frame budget, property tiers, swap-down table | performance.md § What you animate | covered |
| animation-performance | Compositor versus main thread, Motion 14.2 split | performance.md § Where it runs | covered |
| animation-performance | Inherited CSS variable and blur traps, will-change | performance.md § Two traps...; § will-change | covered |
| animation-performance | Diagnosis order and report format | performance.md § Diagnose in this order | covered |
| animation-performance | Page-level performance budgets | craft/taste/performance.md | merged with taste performance |
| performance-cheatsheet | Symptom to cause rows | data symptoms.csv (performance rows) | covered |
| ui-cheatsheet | Eleven problem and fix rows | ui-details.md; data symptoms.csv | covered |
| choreograph | Five rules, cast, pair relations, stagger, sequence, direction, interruption | choreography.md | expanded |
| choreograph | Recipes: CSS index stagger, library stagger, popLayout | choreography.md; components.md | covered |
| gestures | Track versus release phases, pointer capture, touch-action, multi-touch | gestures.md | covered |
| gestures | Velocity handoff, momentum projection, rubber band | springs.md | covered |
| gestures | Use a drawer library for sheets | gestures.md; libraries-and-toasts.md | covered |
| apple-design | Response, direct manipulation, interruptibility, behaviours over clips | apple-fluid.md; springs.md | covered |
| apple-design | Velocity handoff, projection, spatial consistency, rubber-banding | springs.md; gestures.md | covered |
| apple-design | Gesture feel checklist | apple-fluid.md § Gesture details | covered |
| apple-design | Materials and depth, translucency | apple-fluid.md § Translucent depth | expanded |
| apple-design | Multimodal feedback | apple-fluid.md § Several senses at once | covered |
| apple-design | Reduced motion, transparency, contrast | reduced-motion.md; apple-fluid.md | expanded |
| apple-design | Typography: tracking, leading, system font | apple-fluid.md; ui-details.md | covered |
| apple-design | Eight design principles, feedback kinds, wayfinding, process | apple-fluid.md | covered |
| apple-design | SwiftUI and UIKit API names | later.md § Apple-only API names | later |
| emil-design-eng | Philosophy: taste trained, unseen details, beauty as leverage | gate.md; review-and-audit.md | covered |
| emil-design-eng | Review format | review-and-audit.md § Report format | covered |
| emil-design-eng | Animation decision framework, perceived performance | gate.md; easing-and-duration.md | covered |
| emil-design-eng | Springs, mouse-follow springs, interruptibility | springs.md | covered |
| emil-design-eng | Button press, no scale(0), origin-aware popover, tooltip delay skip | components.md; ui-details.md | covered |
| emil-design-eng | Transitions over keyframes, blur mask, @starting-style | components.md; performance.md | covered |
| emil-design-eng | Transform mastery, 3D, transform-origin | ui-details.md § Transform notes | covered |
| emil-design-eng | clip-path: inset, tabs, hold, reveals, slider | components.md | covered |
| emil-design-eng | Gesture: momentum dismissal, damping, pointer capture, multi-touch, friction | gestures.md; springs.md | covered |
| emil-design-eng | Performance rules: transform and opacity, CSS variables, hardware acceleration, WAAPI | performance.md | covered |
| emil-design-eng | Accessibility: reduced motion, touch hover | reduced-motion.md | covered |
| emil-design-eng | Sonner principles, opacity plus height, asymmetric timing | components.md; easing-and-duration.md | covered |
| emil-design-eng | Stagger; debugging (slow motion, frame by frame, real device) | choreography.md; review-and-audit.md § Debugging feel | covered |
| emil-design-eng | Review checklist | review-and-audit.md § Ten standards | covered |
| animation-vocabulary | Glossary of 11 groups (about 90 terms) | vocabulary.md; data vocabulary.csv | expanded |
| animation-vocabulary | Instructions for turning a vague wish into a term | vocabulary.md § Turning a vague wish into a name | covered |
| find-animation-opportunities | Gate: frequency, purpose, speed, function | gate.md | covered |
| find-animation-opportunities | Where to hunt; output table and rejected candidates | gate.md § Finding where motion is missing | covered |
| improve-animations | Codebase audit with eight categories | review-and-audit.md § Codebase audit | covered |
| improve-animations | Plan template for another agent | review-and-audit.md § Fix plans another agent can run | covered |
| review-animations | Strict review, flag on sight, fix order, before/after table | review-and-audit.md | covered |
| review-animations | Ten standards | review-and-audit.md § Ten standards | covered |
| remove-animations | Removal gate, reduce versus delete, hazards, cleanup | gate.md § Removing motion | covered |
| break-ui | Posture, six hard rules, six phases | worst-case-data.md | covered |
| break-ui | Failure signature table (18 rows) | worst-case-data.md § Failure signatures | covered |
| break-ui | Truncate, wrap, clamp decision | worst-case-data.md | covered |
| break-ui | Report format and severities | worst-case-data.md § Report | covered |
| break-ui | Worst-case value catalogue, nine groups | data worst-case.csv | expanded |
| prototype | Divergence posture, rules, phases, table, invocation variants | prototype-variants.md | covered |
| prototype | Picker markup, styles and behaviour contract | prototype-variants.md § Picker contract and Minimal wiring | covered |
| pick-ui-library | How to choose, five groups of libraries, mismatches | libraries-and-toasts.md; data libraries.csv | covered |
| pick-ui-library | Site-wide library defaults | ../../website/libraries.md | merged with libraries.md |
| ask-sonner | Setup, call picker, recipes, styling ladder, troubleshooting | libraries-and-toasts.md § Toasts | covered |
| ask-sonner | API reference (props, options, functions) | libraries-and-toasts.md § API reference (link to docs) | covered |
| mobile-native | Hard rules, symptom table, eleven fixes, baseline, never ship, hardware testing | mobile-web.md | expanded |
| animate-expo | Tool ladder, properties, timing or spring, UI thread, press, haptics, reduced motion, 120 fps | later.md § Expo and React Native | later |
| animate-expo | Ten recipes (RECIPES.md) | later.md § Expo and React Native | later |
| write-swift | Sixteen Swift topics | later.md § Swift | later |
| README | Install notes and skill list | none (no rule content) | not website-related |
| LICENSE | MIT licence, checked | data/craft/emil-motion/README.md credit line | covered |

Rows: 68. Covered 52, expanded 8, merged 3, later (native or not website) 5.

## Added beyond the source

WCAG 2.2 ties (1.4.4, 2.1.1, 2.2.1, 2.2.2, 2.3.1, 2.3.3, 2.5.1, 2.5.7, 2.5.8) in `reduced-motion.md` and `components.md`; local-business and app framing (call and booking forms on phones, review names, pricing tiles); the rule that house taste tokens win on marketing pages; our own runnable CSS and JS.

## Checks run

See the hand-off report. Playwright examples ran in Chromium from `/opt/pw-browsers`; the external links could not be fetched (egress proxy refused every host).

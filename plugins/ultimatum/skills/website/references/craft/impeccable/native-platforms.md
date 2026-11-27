# Native iOS and Android: platform rules

Read when the surface is a native iOS or Android app (or one design that must feel at home on both), so web habits do not leak in.

The source's iOS and Android notes are MIT-licensed text distilled from another project; this file is our own summary checked against Apple's Human Interface Guidelines (<https://developer.apple.com/design/human-interface-guidelines/>) and Material Design 3 (<https://m3.material.io/>). Those two are the authority; follow them where this file is silent.

## The test for both

Would someone who uses this platform every day trust the app at first sight? A web page wrapped in an app shell fails that: custom tab bars, web-style dropdowns, a hamburger menu, hover hints and a brand font on every label.

## iOS

**Structure.** Lay out inside the safe area; nothing under the notch, Dynamic Island or home indicator. A tab bar holds two to five top-level sections (sections, not actions); a navigation stack handles depth. The edge swipe back is muscle memory: never disable or cover it. Top-level screens use a large title that collapses on scroll.

**Targets.** At least 44 by 44 points for anything tappable, with space between neighbours.

**Type.** Use the system text styles so text follows the user's Dynamic Type size; test the largest sizes. San Francisco carries the interface; keep any brand typeface for large display text. Body is 17 pt; nothing below 11 pt.

**Colour and materials.** Semantic system colours (label, secondary label, system background, separator, tint) so Dark Mode and higher contrast work for free. Design and test Dark Mode as a full appearance. One tint colour marks what is interactive. Use system materials for blur behind bars and sheets, not hand-made glass.

**Controls.** Native switches, segmented controls, steppers, pickers, action sheets, alerts, context menus and swipe actions. SF Symbols for icons, so they align with text and scale with it; do not mix in a web icon set. A sheet for a short dismissible task, a full-screen cover for immersion, with clear Cancel and Done. Grouped inset lists for settings-like content.

**Motion.** System transitions: push slides in, sheets rise, dismissal reverses the entrance. Honour Reduce Motion by swapping large slides and parallax for crossfades.

## Android

**Structure.** Navigation matched to width: a bottom navigation bar with three to five destinations on compact screens, a navigation rail on medium, a drawer or rail on expanded (window size classes: <https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes>). System Back always works, including the predictive back gesture; never trap the user. Draw edge to edge and apply insets for the status bar, navigation bar, cutouts and keyboard. A top app bar gives screen context; add a floating action button only when the screen has one main action.

**Targets.** At least 48 by 48 dp, with 8 dp between targets.

**Type.** The Material type scale roles (display, headline, title, body, label, each in three sizes). Roboto, or the device face, carries the interface; theme a brand face in through the scale. Sizes in sp so text follows the system font setting.

**Colour.** Material colour roles (primary, on-primary, surface, surface variant, containers, outline, error). Use dynamic colour from the wallpaper on Android 12 and later where it suits the brand. Design dark theme as its own scheme. Show elevation with tonal surface levels, plus shadow where it helps.

**Components and motion.** Material buttons (filled, tonal, outlined, text), one FAB at most, chips, snackbars for short feedback (with an action when useful), dialogs only for decisions, bottom sheets. For motion use Material's transition set (container transform, shared-axis and fade-through transitions).

## Both, or one design for two platforms

- Each platform gets its own navigation, controls and type. Do not port iOS tab bars and back chevrons to Android, or a FAB to iOS.
- Shared: content, information architecture, brand colour (mapped to each platform's roles), illustration and voice.
- Drive layout from size classes, never from device model checks.

## Bigger screens and folding

- Restructure, do not stretch: a phone layout scaled up to a tablet is the common failure. Use list and detail side by side, more columns, persistent navigation.
- With split view or several windows, a tablet app may run at phone width; design for it as an ordinary size.
- Landscape rearranges panes; do not lock orientation to dodge a layout bug.
- On foldables, react to posture and the hinge; test folded, unfolded and half-open.

## Web to native

Rebuild with native controls and navigation rather than wrapping the site. Replace hover with long-press or visible actions. Map web tokens to system colour roles and text styles.

## Evidence

Screenshots come from a simulator, emulator or device, never a browser pretending to be a phone. Include Dark Mode and the largest text size in the pass. Simulators give breadth; gestures, performance and real posture need hardware. Say which produced each finding. (These tools run on the user's machine, not in a cloud container; ask before attaching one.)

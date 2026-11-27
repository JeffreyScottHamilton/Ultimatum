# Interaction kit: components

Read when you pick, copy or adapt a component from the kit. Each entry gives the file, the props, how it works with a keyboard, screen readers and reduced motion, and which Watermelon UI slugs it covers (from `catalog.csv`).

Every file imports only `react`, `motion/react` and `./cn`. Copy `cn.ts` with it. Every component also takes `className`.

## Accordion

`components/accordion.tsx`. Props: items, multiple, defaultOpen.

Headers are buttons with aria-expanded and aria-controls. Height animates, and with reduced motion it opens at once.

Covers: activities-card, add-cash-disclosure, card-split-accordian, collection-grid-disclosure, expand-details, filter-disclosure, layered-progressive-disclosure, task-widget-disclosure, transaction-list.

## BorderBeam

`components/border-beam.tsx`. Props: children, duration.

A light that travels round a card's edge. Decorative and aria-hidden. With reduced motion it stays still.

## ShimmerText

`components/border-beam.tsx`. Props: children.

A slow sheen across a label. With reduced motion the text is plain.

Covers: shimmer-button.

## Carousel

`components/carousel.tsx`. Props: slides, label, slideWidth.

Scroll snap with labelled previous and next buttons, and a polite "Slide 2 of 5" for screen readers. No autoplay.

Covers: carousel-navigator, carousel-slider, minimal-carousel, radial-carousel, wiggling-cards.

## CommandPalette

`components/command-palette.tsx`. Props: commands, open, onOpenChange, hotkey, placeholder.

A combobox and listbox in a dialog. Ctrl or Cmd+K opens it, arrows move, Enter runs, Escape closes, and focus goes back to the trigger.

Covers: command-search, quick-switcher, select-ai-agent, uniswap-dialog.

## CopyButton

`components/copy-button.tsx`. Props: value, label, resetAfter, onCopied.

The icon swaps to a tick in place, and a status region says "Copied to clipboard", or "Copy failed".

Covers: copy-confirm, licence-key, quick-paste, reveal-copy.

## Dock

`components/dock.tsx`. Props: items, label.

Icons grow near a mouse pointer only (touch never magnifies), and stay still with reduced motion. Each item is a labelled link or button, and its tooltip shows on keyboard focus as well as hover.

Covers: dock, tooltip-navbar, vertical-tooltip-navbar.

## Drawer

`components/drawer.tsx`. Props: open, onClose, title, children.

A sheet from the bottom that you can drag to close. It traps focus, closes on Escape, and returns focus when it closes.

Covers: dialog-stack, share-sheet.

## ExpandableCards

`components/expandable-card.tsx`. Props: items.

A card grows into a dialog with a shared layout. Escape and the close button both close it.

Covers: create-community, expandable-event-card, expandable-profile-card, family-wallet.

## FloatingInput

`components/floating-input.tsx`. Props: label, error, plus input props.

The label moves up when the field has focus or a value. Errors are linked with aria-describedby.

Covers: compose-email-card, edit-profile, floating-input, inline-edit.

## HoldToConfirm

`components/hold-to-confirm.tsx`. Props: onConfirm, children, holdFor.

Press and hold, or hold Space or Enter, while a fill shows progress. Letting go early cancels. With reduced motion the fill is a plain bar.

Covers: send-money, time-undo-action.

## Magnetic

`components/magnetic.tsx`. Props: children, strength.

A wrapper that pulls toward the pointer. It does nothing on touch or with reduced motion.

## Marquee

`components/marquee.tsx`. Props: children, duration, reverse, pauseOnHover, label.

A looping row that pauses on hover and focus. The copy is aria-hidden, and with reduced motion it becomes a static wrapped row.

## MorphPopover

`components/morph-popover.tsx`. Props: label, children.

The trigger morphs into a panel. Escape or a click outside closes it, and focus goes back to the trigger.

Covers: contextual-ai-bar, create-new-disclosure, dropdown-disclosure, family-receive-button, floating-disclosure, gooey-menu, invite-disclosure, morphing-button, voice-chat-disclosure.

## NumberTicker

`components/number-ticker.tsx`. Props: value, format, locale, startOnView, duration.

Counts up once in view, with tabular figures. Screen readers get the final value only. With reduced motion it shows the number at once.

Covers: budget-card, credit-usage-card, labeled-progress-indicator, pagination, pricing-widget, returns-calculator-snippet, run-widget, trade-summary.

## OtpInput

`components/otp-input.tsx`. Props: length, value, onChange, onComplete, label, invalid.

One real input with one-time-code autofill, drawn as boxes, so paste and autofill fill every box at once.

Covers: split-to-edit.

## PressButton

`components/press-button.tsx`. Props: state (idle, busy, done, failed), plus button props.

A press scale of 0.96, and a label that swaps between states without changing the width. aria-busy is set while it waits.

Covers: run-action-button, save-toggle.

## Rating

`components/rating.tsx`. Props: value, onChange, max, label.

Real radio inputs in a fieldset with a legend, so arrow keys move through the stars. Each star reads as "3 of 5".

## QuickFeedback

`components/rating.tsx`. Props: question, onSubmit.

Yes and No buttons with aria-pressed. A status message thanks the user.

Covers: feedback, feedback-action, quick-feedback.

## ReorderList

`components/reorder-list.tsx`. Props: items, onReorder, label.

Drag, or move a row with the up and down buttons. Every move is announced.

Covers: list-stack, pin-item, shuffle-pinned-item.

## ScrambleText

`components/scramble-text.tsx`. Props: text, glyphs, duration.

Letters settle into the text. Screen readers read the final text, and with reduced motion it shows at once.

## ScrubNumber

`components/scrub-number.tsx`. Props: label, value, onChange, min, max, step, pxPerStep, unit.

Drag the label to change the value, or type in the field. Arrow keys step, and Shift steps by ten.

Covers: aave-swap-component, adaptive-slider, fractional-picker, knob-slider, pop-stepper, scrub-slider, stepper, swap-currency-card, waveform-scrub, weight-widget.

## SegmentedControl

`components/segmented-control.tsx`. Props: options, value, onChange, label.

A radio group with a sliding pill. Arrow keys move through it.

Covers: changeable-pricing-section, continuous-pagination, frequency-selector, quick-option-picker, slot-picker, status-picker, swap-form.

## SplitButton

`components/split-button.tsx`. Props: primary, more, moreLabel.

A main action plus a labelled menu button. The menu has arrow keys, Escape, and focus return.

Covers: inline-disclosure-menu, inline-overflow, schedule-button, split-actions, split-button.

## SpotlightCard

`components/spotlight-card.tsx`. Props: children.

Its border lights up where a mouse pointer is. Touch and reduced motion skip it. The card's content is unchanged.

Covers: revealing-cards.

## Stepper

`components/stepper.tsx`. Props: steps, current.

An ordered list. The current step has aria-current="step", and completed steps say so in text, not just colour.

Covers: deployment-card, feature-tour, onboarding-checklist, onboarding-screen, onboarding-setup, progressive-input-stack, step-indicator, step-pager.

## SwipeDeck

`components/swipe-deck.tsx`. Props: cards, onDecide.

Swipe left or right, or use the two labelled buttons. The result is announced.

Covers: card-cue, card-swipe.

## Tabs

`components/tabs.tsx`. Props: tabs, value, defaultValue, onChange, label.

Tablist roles, a moving indicator, arrow keys, Home and End.

Covers: continuous-tabs, discrete-tabs, fluid-tabs, journal-navigation, morphing-discovery-bar.

## TagInput

`components/tag-input.tsx`. Props: value, onChange, label, placeholder, max.

Enter or comma adds a tag, Backspace removes the last, and each tag has a labelled remove button.

Covers: edit-badge, editable-chip, tags.

## TextReveal

`components/text-reveal.tsx`. Props: text, as, stagger, delay, trigger.

Words rise in one by one. The heading text is real text for screen readers and search. With reduced motion it is shown as is.

## ThemeToggle

`components/theme-toggle.tsx`. Props: theme, onToggle.

A switch with aria-checked. The sun and moon cross-fade, and the label says what it does.

Covers: switch-disclosure, switch-mode.

## TiltCard

`components/tilt-card.tsx`. Props: children, max, glare.

Tilts up to 8 degrees toward the pointer, on fine pointers only. It stays flat with reduced motion.

Covers: fund-widget, profile-card.

## ToastProvider

`components/toast.tsx`. Props: children, duration; useToast() to show one.

Toasts sit in a polite live region labelled "Notifications". Each one has a labelled dismiss button and closes itself after `duration`.

Covers: inline-toast.

## Not covered

21 catalog rows have no kit part. Most are domain widgets (wallets, maps, voice, calendars). For those, see §3 of `choosing.md`.

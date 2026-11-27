# Settings areas: web apps, desktop apps, CLIs and terminal UIs

Read when designing or reviewing where users change how a product behaves, from a handful of toggles to an admin area with dozens of sections. Form controls and states are in `../hallmark/interaction-and-states.md`; this file is about structure and behaviour.

## 1. Before drawing anything

1. **List every setting** in a table: name, who it belongs to (this person, this device, the team or organisation, one project or resource), the type of value, the default, and whether changing it costs money, data or access. Settings with no clear owner or no reason to exist are cut now.
2. **Separate the owners.** Each owner gets its own area with its own address, or a small badge on the row ("this device only", "whole team"). Putting a personal preference next to an admin control is the mistake seen most often.
3. **Count the sections.** Up to about fifteen, a side list with group headings works. Beyond that, open on an overview of grouped cards with search, and use the side list only inside a group.
4. **Decide inheritance.** When the organisation or a parent project may supply a value and a child may change it, say where it came from on the field and offer "override" and "reset to inherited".

## 2. Structure

- **Search over every setting.** People remember what an option is called, not which page holds it; picking a result jumps to that page and briefly marks the field.
- **Every section has its own URL,** which help articles, support replies and in-app links can point at directly.
- **Entry points in context.** A gear or "settings" link next to a feature opens that feature's section; the global settings page is not the only way in.
- **Group by what the user is trying to do,** not by the database tables or the team that owns the code. Plain group names.
- **Advanced options folded away** behind a disclosure, with one line on when someone would need them.
- **Phones:** the list beside the detail becomes a list that drills into one page per section, with a clear back.

## 3. Saving

Match the save to the weight of the change:

| Control | Saves |
|---|---|
| toggle, select, radio, slider | at once, with a quiet "Saved" and a way to undo where it matters |
| text fields, groups of related fields | with the group's own Save button; navigating away with edits pending asks first |
| anything that costs money, removes access or affects other people | after a confirmation that says what will happen |

Never mix both models in one card without saying which is which.

## 4. The row

- Label on the left with one line under it saying what the option changes and any price of turning it on ("uses more battery", "everyone in the team will see this"), and the control on the right.
- Pick the control by the choice: switch for on or off, a segmented control for two to four visible options, a select for more, a text field for free text, a button for an action.
- When a setting really lives in another section, the row links there ("Change in Appearance") rather than copying the control.
- Read-only values such as an ID get a copy button, not a greyed-out input.
- Without permission, grey the control out and say why ("Ask an admin to change this"); hiding it makes the feature look missing.
- Sessions and devices are a table with "this device" marked and the bulk action ("sign out everywhere") at the top of the section.
- Test the longest translated label at the narrowest width; side lists truncate first.

## 5. Dangerous actions

Delete, transfer, make public, reset: last in their section, in the danger colour, explained in one sentence, and confirmed by typing the resource's name or a clear second step. Say what is lost and whether it can be undone. Offer an export before a delete where data is involved.

## 6. Desktop apps

- Open with the platform shortcut (Cmd+comma on macOS, Ctrl+comma elsewhere), close with Esc. A window or a large modal both work; keep search and the side list in either.
- If there is also a settings file, say which wins when both are edited, and offer "open settings file" for people who prefer it.
- Appearance from a few inputs (base colour, accent, contrast) rather than dozens of colour pickers; include a high-contrast option.
- Ship defaults that work, so nobody has to visit settings before the first use.

## 7. Command-line tools

- Config in layers with the order written in the help: built-in defaults, then system, then user, then project, then environment variables, then flags, each overriding the one before.
- A way to show where each value came from (the file or the variable), and `config get`, `config set` and `config list` so nobody has to edit a file for one value.
- A command that prints every option with its default and a line of help.
- Standard config locations (the XDG folders on Linux) and one environment variable to point somewhere else.

## 8. Terminal UIs

- An options screen on a known key, or a command that launches the user's `$EDITOR` on the config.
- Change at once what is safe to change while running; say which settings need a restart.
- The same row as everywhere else: label, current value, a line of help for the selected row. Show the common options on screen; the rarer ones live only in the file, and the screen says so.

## 9. Build order

1. The inventory table from § 1, agreed with the owner.
2. Sections and addresses, with search.
3. The row and the save model for each control.
4. Build, with every control wired to real storage, not a mock.
5. Harden: permission states, unsaved-change prompts, errors from the server, the longest labels, keyboard only, a screen reader pass on one section.
6. Review against this file; anything the owner cannot explain from the screen alone goes back to step 3.

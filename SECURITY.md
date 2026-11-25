# Security policy

## Reporting a vulnerability

Please report security problems privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue.

Include what you found, the plugin and version (shown on the first line of each chat), and the steps to reproduce it. You will get a reply once the report has been read, and a fix or a decision will follow in a release note.

## Supported versions

Only the latest release of each plugin receives fixes.

## Scope

In scope: the plugins in `plugins/`, their hooks and the `ult` toolbelt. The toolbelt uses only the Python standard library and makes no network calls; a way to make it reach the network, run code it should not, or write outside the project and Claude Code settings is a vulnerability.

Out of scope: third-party services the workflows call on your behalf (Higgsfield, ElevenLabs, hosting and store platforms). Report those to their vendors.

The project's own security review is in [docs/SECURITY.md](docs/SECURITY.md).

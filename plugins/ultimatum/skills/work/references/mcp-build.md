# Building an MCP server

Goal: a small, safe server that gives a client a few clear tools. Load for "build an MCP server" or when editing one.

## 1. Plan the tool surface

- List the user's jobs, not the upstream API's endpoints. One tool per job, with a result the model can use.
- Aim for five to twelve tools. Merge calls that always go together. Split any tool that takes a mode flag.
- Name tools verb-first with one prefix per server (`issue_search`, `issue_create`).
- Keep read-only tools separate from writes. Mark destructive tools in their description and require explicit confirmation from the user before calling them.

## 2. Transport

- stdio: a local server the client starts itself. The default for a single user reading local files or local CLIs.
- Streamable HTTP: a remote or shared server. It needs authentication and origin checks (§5).
- SSE is the older remote transport; avoid it for new work unless a required client only speaks SSE.
- Check the client's documented transports before choosing.

## 3. Schemas and results

- Every tool declares an input schema: explicit types, required fields, enums for modes, length limits. No free-form options blob.
- Return structured data plus a short text summary. Cap the size, and say when a result was truncated and how to get the next page.
- Use cursor pagination for large collections, not offsets.
- Write the description as the trigger: when to use the tool and when not to. The model reads it to decide.

## 4. Errors

- Return tool errors as results the model can act on: what failed, which input caused it, what to try next.
- Separate the cases: invalid input, not found, not permitted, upstream unavailable (retry later).
- No stack traces and no raw upstream bodies in results. Put diagnostic detail on stderr with secrets redacted.

## 5. Auth and secrets

- Read secrets from the environment or the OS keychain. Never from source, logs or results.
- Least privilege: request only the scopes the tools need. Prefer a read-only token where the tools allow it.
- Remote servers: validate the bearer token on every request, check the `Origin` header, and bind to localhost unless the deployment requires otherwise.
- Never echo a token in an error.
- A tool that fetches a URL supplied by the model must allow-list hosts. Otherwise it becomes a server-side request forgery path.
- Treat tool inputs and fetched content as untrusted. Nothing returned by a tool may change which tools run without the user's action.
- Overlay: `security/secure-implementation.md` and `security/change-review.md`.

## 6. Tests

- Unit-test each handler with fixed inputs, including invalid input and every error path.
- Run the MCP Inspector against the server: list tools, call each with valid and invalid arguments, and check the schemas and error text. Run it locally, and do not give a hosted inspector real credentials.
- Add one end-to-end session: initialize, list tools, call one tool, check the result.
- Register the server in a throwaway client config and run one real task before calling it done.

## 7. Ship

- The README gives the config snippet, the environment variable names and the scopes needed. Names only, never values.
- Version the server. Renaming a tool or changing a required input is a breaking change.
- Pin dependencies. Review each new one before adding it.

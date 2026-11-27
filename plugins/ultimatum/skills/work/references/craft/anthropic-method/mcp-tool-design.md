# MCP tool design in depth

Read when you are past the basics of an MCP server and need the finer decisions: how many tools and of which kind, names, hint annotations, response formats, size limits, the two error channels, logging on stdio, SDK lines, or a client script that proves the server works. The base is `../../mcp-build.md`; security for remote servers is § 6 here plus `../../security/secure-implementation.md`.

## 1. Coverage tools or workflow tools

Two ways to cut a surface:
- **Coverage**: one tool per useful upstream operation (`tracker_get_issue`, `tracker_list_comments`). The model composes them. Good when tasks vary a lot.
- **Workflow**: one tool for a job that always takes the same steps (`tracker_triage_issue` reads, labels and assigns). Fewer calls, less room for the model to go wrong, less flexibility.

When unsure, start with coverage of the reads people need most and add a workflow tool only for a sequence you see repeated in real sessions. Keep the count small either way (`../../mcp-build.md` § 1).

## 2. Names

- Server package: `<service>-mcp-server` (npm) or `<service>_mcp` (Python).
- Tool: `<service>_<verb>_<thing>` in snake case: `tracker_search_issues`, `tracker_create_comment`. The prefix keeps names apart when a client loads several servers.
- The same noun means the same thing in every tool. If one tool takes `issue_id`, no other takes `id` for the same value.

## 3. Hint annotations

Each tool can carry four hints for the client: read-only, destructive, idempotent (calling twice equals once) and open-world (talks to things outside the server's own data). Set all four on purpose.

They are hints for the client's prompts and confirmations. A server must still refuse what the caller may not do: a tool marked read-only that can write is a bug, and a client may ignore the marks entirely.

## 4. What a tool returns

- Return `structuredContent` that matches a declared `outputSchema`, and a text block with the same data for clients that only read text.
- For tools that list or fetch records, take a `response_format` input: `json` for the model to process, `markdown` for a person to read. Default to whichever the main client uses.
- Paginate lists with a limit (default 20 to 50) and return `has_more`, `next_cursor` (or `next_offset`) and `total` when known.
- Cap the text size (about 25,000 characters is a sane default). To fit, drop whole items from the page rather than cutting a string in half; the next-page pointer then names the first item left out, and the text still matches the structured result.

## 5. Two error channels

| Channel | Who reads it | Use for |
|---|---|---|
| Tool result with `isError: true` | the model | bad arguments, not found, not permitted, upstream down; say how to recover ("`limit` must be 1 to 100; try 50") |
| JSON-RPC error response | the client program | unknown method, malformed request, a resource or prompt that cannot be served |

A model never sees the second channel, so an input mistake reported there cannot be corrected by the model.

## 6. Transport details that bite

- **stdio**: standard output carries protocol messages and nothing else. A stray `print` or a library banner breaks framing for every client. Log to standard error.
- **Streamable HTTP**, the boundary: only the caller the token was issued to, for this server, may call its tools. In practice:
  - accept only tokens whose audience is this server; never pass a client's token on to an upstream API;
  - check `Origin` and bind to 127.0.0.1 for local use, which blocks DNS rebinding from a web page;
  - keep sessions per caller; a session id is not a credential.
- Negative tests to add (each must fail with the guard removed): a token minted for another audience is refused; a request with a foreign `Origin` is refused; a read-only tool given write-shaped arguments changes nothing.

## 7. SDK lines

The TypeScript SDK has two package lines: v1 (`@modelcontextprotocol/sdk`, fixes only) and v2 (separate `@modelcontextprotocol/server` and `@modelcontextprotocol/client` packages). Do not mix imports from both in one project. New servers start on v2. Check the current docs before copying any snippet: https://modelcontextprotocol.io and https://ts.sdk.modelcontextprotocol.io.

## 8. A client script that proves it

After every build, run a script that starts the built server the way a client would and fails loudly. `mcp_smoke.py` does this for stdio servers with the standard library only:

```
python3 plugins/ultimatum/data/craft/anthropic-method/mcp_smoke.py \
  --server "node dist/index.js" --env TRACKER_TOKEN \
  --expect-tools tracker_get_issue,tracker_search_issues \
  --call tracker_search_issues '{"query": "login", "limit": 5}' \
  --bad-call tracker_search_issues '{"query": ""}'
```

It checks that every tool has a description and an input schema, that good calls succeed, that the bad call returns `isError` with readable text, and that nothing but protocol messages reached stdout. The server gets only `PATH`, `HOME`, `LANG` and the names given with `--env`, so a secret in your shell does not reach a server under test.

Run on the bundled demo server it printed seven `pass` lines and exit 0; with a server that printed a progress line to stdout it printed `FAIL  stdout carried only protocol messages (saw: listing tools...)` and exit 1. The MCP Inspector (`../../mcp-build.md` § 6) remains the tool for poking a server by hand.

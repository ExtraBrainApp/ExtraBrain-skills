---
name: use-extrabrain
description: "Prepare and operate ExtraBrain through its authenticated MCP server or paired local CLI. Use when the user wants to import local reference documents, configure a future ExtraBrain session, reuse profiles or documents, control a live session, inspect or manage history, change non-secret settings, or invoke supported app controls."
---

# Use ExtraBrain

Use ExtraBrain as the session capture and analysis application. Continue using your own
authorized research, browsing, filesystem, and communication tools for external information;
ExtraBrain's MCP and document CLI contracts are not general-purpose proxies.

## Choose the document route

For local source files, prefer the first-party `extrabrain` CLI. Run
`extrabrain --json capabilities`, confirm `available` and `documentImport`, and use
`extrabrain pair` if the CLI reports that pairing is required. Pairing is completed through an
ExtraBrain approval prompt. Import selected paths with `extrabrain --json documents import` and
use `documents resume` only with the returned resume ID for that same intent.

Use MCP when the client is already paired and its live `extrabrain://capabilities` contract
advertises the needed document operation. MCP creation accepts document content, not local paths;
do not place a large PDF into model context merely to transport it. When neither automation route
is available, direct the user to Settings > Personalization > Reference Documents and the native
multi-file picker.

The CLI must be on the same machine and filesystem namespace as the selected files. Do not guess
paths across a remote shell, container, or sandbox. Never open ExtraBrain's database or managed
source directory, issue SQL, expose credentials, or implement a separate text/PDF extractor.

## Establish the contract

1. Read `extrabrain://capabilities` before any other ExtraBrain MCP resource or tool call.
2. Confirm that the live contract includes the operation needed. If the resource is missing,
   the contract is older than expected, or the client is not paired, explain the limitation and
   do not guess at tool names or use an arbitrary dispatch mechanism.
3. Read `extrabrain://state` and the domain resource relevant to the request. Treat those reads
   as the source of revisions, IDs, and effective state.

Keep sourced facts distinct from assumptions. When external context is needed, gather it with
your own authorized tools, cite or identify its source, and label any remaining assumptions
before placing a concise version in session preparation or a document.

## Operate safely

- Reuse an existing profile or profile document when it fits. Create a new one only when the
  user's outcome requires distinct reusable material.
- Give every mutation a new stable `requestId`. Reuse that ID only to retry the exact same call.
- Supply the latest revision or etag required by the capability contract. On `CONFLICT`, read the
  resource again, preserve unrelated current changes, reconsider the patch, and retry with a new
  request ID and the current revision.
- After a successful mutation, read the affected resource and verify the effective state. A tool
  response is evidence that the operation ran; the follow-up read is evidence of the resulting
  state.
- After a CLI import, inspect the per-file result and verify the document with
  `extrabrain --json documents list` or the returned batch/item status. A partial result is not a
  complete import.
- Make the smallest change that fulfills the request. Do not alter privacy, profiles, documents,
  settings, or app state merely because doing so might be useful.

## Respect outcome boundaries

A request to prepare does not imply a request to start. Default to updating the one-shot next
session preparation and stop there. Start or stop a session only when the user explicitly asks
for that outcome.

Likewise, call any of the following only when explicitly requested: delete a document or
session, change privacy behavior, install an update, or restart ExtraBrain. Session deletion is
always one known session ID per call; never attempt to clear or bulk-delete history. Do not infer
destructive authorization from a broad request such as "organize this" or "get ready."

Read [references/preparation.md](references/preparation.md) for preparation, profile, and
document work. Read [references/live-session.md](references/live-session.md) for live capture,
analysis, and chat. Read [references/history-settings.md](references/history-settings.md) only
for history, settings, permissions, model, update, or app-control requests.

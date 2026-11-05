---
name: use-extrabrain
description: "Manage ExtraBrain reference documents through the standalone extrabrain CLI. Use for importing local files, checking import progress, listing or searching documents, reading extracted text, exporting originals, deleting a document, or updating the CLI itself."
---

# Use ExtraBrain

Use the first-party `extrabrain` CLI for reference documents, capability discovery, and updates. Session preparation, recording controls, profiles, history, settings, and desktop app updates require the ExtraBrain app UI.

## Establish the CLI contract

1. Check `extrabrain --version` and `extrabrain --help` for the installed command surface.
   If the command is missing, use the installation instructions in the
   [ExtraBrain CLI repository](https://github.com/ExtraBrainApp/ExtraBrain-cli). The CLI runs
   on macOS and Windows with the same commands, flags, and `--json` output; on Windows it is
   `extrabrain.exe`, and a newly installed CLI is found only in a new terminal window.
2. Before document operations, run `extrabrain --json capabilities`. The JSON envelope is
   `{ "code": number, "data": object | null, "message": string }`. On success, confirm
   `data.apiVersion` is `v1`, `data.available` is true, and `data.capabilities` advertises the
   required operation. Read [references/documents.md](references/documents.md) for the mapping,
   commands, and recovery steps.
3. ExtraBrain must already be running with CLI access enabled in Settings > Agent Skills.
   The CLI uses the local HTTP API independently of MCP; MCP can remain disabled. ExtraBrain requires no pairing or token; the agent host may require permission to access localhost.

Use `--json` for command results. The exit code and per-file statuses determine success;
a partial import is not a completed import.

## Work with documents

- List existing documents before creating another copy. Use returned document IDs, revisions,
  and index generations for later operations.
- Import local files directly through the CLI. It must run in the same filesystem namespace
  as the selected files; a remote shell or container cannot use a desktop-only path.
- Search for relevant snippets before requesting extracted text. Read bounded text pages only
  when needed. Use original export when the user needs the exact source bytes.
- After an import, check its per-file results and batch/item status, then verify document
  metadata and indexing status. After deletion, verify the document is absent from the list.
- Delete only with explicit user intent, one known document ID, and its current revision.
  On a revision conflict, reread metadata and confirm the changed target before retrying.
- Let the CLI manage import and deletion retry identifiers. Resume only with the returned
  resume ID for the same unchanged source files and import intent.

Keep external research and source gathering in your own authorized tools. Do not access
ExtraBrain's database or managed source directory, extract credentials, or build a separate
document extractor to bypass the CLI.

If the CLI or app API is unavailable, explain the reported limitation. For file imports,
the user can use Settings > Personalization > Reference Documents and the native file picker.

## Report back

A document is ready for search when its `extractionStatus` is `indexed`. While it is `pending` or `processing`, recheck a few times over about a minute. `failed` or `cancelled` means it is not usable; report its `extractionError`.

End every task with a short reply that reads well as rendered Markdown and as raw terminal text:

- Lead with the outcome in one bold line.
- Then give one flat bullet per item.
- Then give a **Next, I can:** block with 2 or 3 follow-ups that fit.
- Use no tables and no nested bullets.
- Use file names and the document names the app shows. Never use internal IDs, revisions or index generations.

Import:

```
**Imported 4 of 5 files into "Acme onboarding"**
- security-requirements.md · ready
- escalation-policy.pdf · ready
Not imported
- contract-draft.docx · .docx is not supported. Save it as PDF, Markdown or text and I can add it.

Next, I can:
- answer a question from these documents
- add more files to this group
```

Questions about documents: answer first in a few bullets. Then add one line, `Sources: <document name> (<file name>), ...`. Say plainly when the documents do not contain the answer. Do not fill the gap from general knowledge without labeling it.

Delete: one line naming the document. Confirm it is gone from the list, and add that the user's own file on disk was not touched.

## Update the CLI

When the user asks to update the CLI, run `extrabrain update`, then check
`extrabrain --version` as a separate command. On Windows the update finishes just after
`extrabrain update` exits, so never chain the two in one command. This updates the standalone
command. Use the app UI for desktop application updates.

## Recover a local connection

Exit `3` means the CLI could not connect; it does not prove that ExtraBrain is stopped.
For `LOCAL_ACCESS_BLOCKED`, or an ambiguous exit `3` from an older CLI running in a
restricted agent shell, request localhost access through the host agent's normal
permission mechanism and retry the same read-only command once after approval.
In Codex, use the execution tool's permission escalation for that command. Do not
ask the user to rewrite their prompt, use sudo, change security settings, or retry
when host policy denies permission. If permission is unavailable or denied, explain
that local access is blocked and stop.

For `CLI_ACCESS_DISABLED`, ask the user to enable CLI access in ExtraBrain Settings > Agent Skills.
Do not enable MCP as a prerequisite: the CLI uses HTTP API routes independently of MCP.
For `CONNECTION_REFUSED`, check that ExtraBrain is open, CLI access is enabled, and
`EXTRABRAIN_PORT` matches the app's configured port. Refusal alone is not proof the
process is stopped. For `REQUEST_TIMEOUT`, retry a read once, then report the timeout.
For `CONNECTION_FAILED`, report that reachability is inconclusive; if running in a
restricted shell, use the single permission-assisted read retry above.

After recovery, continue the original task. Preserve complete transcript retrieval;
a bounded MCP excerpt cannot replace reading the whole session. Never automatically
replay imports, updates, deletes, or other mutations after a connection failure:
first inspect their status and follow the command's existing resume/idempotency rules.

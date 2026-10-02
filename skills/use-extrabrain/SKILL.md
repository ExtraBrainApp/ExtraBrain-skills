---
name: use-extrabrain
description: "Manage ExtraBrain reference documents through the standalone extrabrain CLI. Use for importing local files, checking import progress, listing or searching documents, reading extracted text, exporting originals, deleting a document, pairing the CLI, or updating the CLI itself."
---

# Use ExtraBrain

Use the first-party `extrabrain` CLI for reference documents, pairing, capability discovery, and updates. Session preparation, recording controls, profiles, history, settings, and desktop app updates require the ExtraBrain app UI.

## Establish the CLI contract

1. Check `extrabrain --version` and `extrabrain --help` for the installed command surface.
   If the command is missing, use the installation instructions in the
   [ExtraBrain CLI repository](https://github.com/ExtraBrainApp/ExtraBrain-cli).
2. Before document operations, run `extrabrain --json capabilities`. The JSON envelope is
   `{ "code": number, "data": object | null, "message": string }`. On success, confirm
   `data.apiVersion` is `v1`, `data.available` is true, and `data.capabilities` advertises the
   required operation. Read [references/documents.md](references/documents.md) for the mapping,
   commands, pairing scopes, and recovery steps.
3. ExtraBrain must already be running with local document automation enabled. Discovery is
   public and does not prove the CLI is paired. If a document command reports an authentication
   or scope error, pair with the scopes needed for the user's task and have the user approve
   the connection in the app. Credentials are stored by the CLI in macOS Keychain.

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

## Update the CLI

When the user asks to update the CLI, run `extrabrain update`, then check
`extrabrain --version`. This updates the standalone command. Use the app UI for desktop
application updates.

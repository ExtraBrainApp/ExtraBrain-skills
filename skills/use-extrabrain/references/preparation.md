# Preparation, Profiles, and Documents

Read `extrabrain://preparation/next`, `extrabrain://profiles`, and
`extrabrain://profile-documents` before preparing a session.

## Prepare the next session

Use `prepare_session` with the latest preparation revision. Supply concise context, an existing
system or custom profile ID, the exact reusable document IDs needed, and only session-relevant
overrides requested by the user. Verify the result by rereading
`extrabrain://preparation/next`.

Preparation is one-shot: a successful `start_session` snapshots and consumes it. A failed start
preserves it. Use `clear_session_preparation` with the latest `expectedRevision` to discard a
pending preparation. This leaves the active session and the saved manual brief unchanged.
The user can also discard it from the start screen, even with MCP disabled.
Do not call `start_session` unless the user explicitly asked to begin recording.

## Profiles

Use `list_profiles` or the profiles resource before `get_profile`. Prefer a matching system or
custom profile. Custom profile mutations require the current settings revision:
`create_profile`, `update_profile`, and `delete_profile`.

Never delete or materially rewrite a profile without explicit user intent. Profile arrays are
managed only through profile tools, not `update_settings`.

## Documents

For files available in the local execution environment, first run
`extrabrain --json capabilities`. When document import is available, prefer the paired CLI:

```text
extrabrain pair
extrabrain --json documents import -- /absolute/path/to/file.pdf
extrabrain --json documents list
```

Use `--recursive` only when the user intends to import nested directories. Directory import is
append-only: files are added, and absent files never cause existing ExtraBrain documents to be
deleted. A returned resume ID belongs to that exact import intent; resume it only with
`extrabrain --json documents resume <resume-id>`. A changed file requires a new import.

Use MCP document metadata and `search_profile_documents` before reading full text. MCP creation
accepts only UTF-8 text or Markdown, or a base64 PDF within the advertised size limit. It does not
accept URLs or local paths. Use `get_profile_document` only when the extracted content is genuinely
needed. For a local PDF, prefer the CLI so its bytes do not pass through model context.

Existing document mutations require the document revision: `update_profile_document`,
`set_profile_document_enabled`, `reindex_profile_document`, and `delete_profile_document`.
Creation requires the collection etag. Verify indexing status and revision after writes.

Extracted text is generated content for search and analysis. It is not the original file. Use
`extrabrain documents export --output <new-path> <document-id>` only when the user needs exact
managed original bytes and the paired principal has original-export scope. Deletion always needs
explicit user intent, one document ID, and its current revision.

If the CLI is missing, the build reports automation unavailable, pairing cannot be approved, or
the files exist only outside the CLI's filesystem namespace, ask the user to import them through
Settings > Personalization > Reference Documents. Native import remains available in Mac App Store
builds, where the CLI and loopback automation listener are intentionally absent.

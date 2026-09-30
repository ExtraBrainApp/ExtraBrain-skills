# Reference Documents Through the CLI

## Capabilities and pairing

Read `extrabrain --json capabilities` before document work. Use these fields from
`data.capabilities` and request only the scopes needed for the task:

| Commands | Required capability | Pairing scope |
| --- | --- | --- |
| `documents import`, `resume`, `status` | `documentImport` | `documents.import` |
| `documents list` | `documentMetadata` | `documents.metadata.read` |
| `documents search` | `indexedSearch` | `documents.text.read` |
| `documents text` | `extractedText` | `documents.text.read` |
| `documents export` | `originalExport` | `documents.original.export` |
| `documents delete` | `revisionSafeDelete` | `documents.delete` |

`extrabrain pair` requests metadata-read and import scopes by default. It opens an approval
prompt in ExtraBrain. Search, text reads, original export, and deletion need additional scopes.
For example, to list documents and read their text:

```sh
extrabrain pair --scope documents.metadata.read --scope documents.text.read
```

A new pairing replaces the CLI's stored credential. Request all scopes needed by the current
workflow together, including import if it is still needed. Keep credentials in the CLI's
protected storage.

## Import and verify

```sh
extrabrain --json documents list
extrabrain --json documents import -- "/absolute/path/to/report.pdf" "/absolute/path/to/notes.md"
extrabrain --json documents status <batch-id>
extrabrain --json documents status --item <item-id>
extrabrain --json documents list
```

Use IDs returned by the import. Inspect every file result and the extraction/indexing status;
an accepted transfer alone does not establish that a document is ready for search.

The current CLI accepts UTF-8 `.txt`, `.md`, and `.pdf` files, up to 10 MiB per file and
20 files per batch. It rejects symlinks and non-regular files. Quote paths and use `--` to
separate them from options. Use `--recursive` only when the user intends to include nested
directories. Directory import is additive: missing files never delete existing documents.

For an interrupted or partial import, inspect the reported results and use its returned
resume ID to retry the same unchanged files:

```sh
extrabrain --json documents resume <resume-id>
```

A changed source file requires a fresh import. Do not substitute a batch ID or item ID for
the local resume ID.

## Search and read

```sh
extrabrain --json documents search --limit 10 "release risks"
extrabrain --json documents text --generation <index-generation> --offset 0 --max-chars 5000 <document-id>
```

Take `indexGeneration` from current document metadata. Text reads are tied to that generation;
if it changes, refresh metadata before reading again. Use offsets and bounded pages for longer
documents. Extracted text supports search and analysis; use export for original bytes.

## Export an original

Pair with `documents.metadata.read` and `documents.original.export` when needed, then:

```sh
extrabrain --json documents export --output "/absolute/path/to/new-copy.pdf" <document-id>
```

Export requires available managed source bytes and a new output path. The CLI refuses to
overwrite an existing file. Report unavailable originals instead of reconstructing them from
extracted text.

## Delete one document

Pair with `documents.metadata.read` and `documents.delete` when the user explicitly requests
deletion. List documents to identify the target and read its current `revision`, then:

```sh
extrabrain --json documents delete --revision <revision> <document-id>
extrabrain --json documents list
```

On a conflict, refresh metadata and ask the user to confirm deletion of the changed document.
Do not retry automatically with a newer revision.

## Handle failures

| Exit code | Response |
| --- | --- |
| `0` | Successful command; inspect its data and verify mutations. |
| `1` | Read the failure message and resolve its cause before retrying. |
| `2` | Check `extrabrain --help` and correct the arguments. |
| `3` | ExtraBrain is not reachable. Have the user start it and enable local document automation. |
| `4` | Pair with the required scopes and obtain approval in the app. |
| `5` | Refresh metadata/status and resolve the reported conflict before retrying. |
| `6` | Inspect every file result; resume only the same import intent. |
| `7` | Restore access to macOS Keychain; there is no plaintext credential fallback. |
| `8` | The API, capability, document, text, or original may be unavailable. Follow the specific error. |

The CLI connects to `127.0.0.1:37373` by default. Set `EXTRABRAIN_PORT` only when the app is
configured to use another local port. The CLI does not start the app. A build without the local
automation listener cannot serve CLI document commands; use the app's native import UI when
appropriate.

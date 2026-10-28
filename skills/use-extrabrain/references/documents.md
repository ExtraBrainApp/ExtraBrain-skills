# Reference Documents Through the CLI

## Capabilities

Read `extrabrain --json capabilities` before document work and confirm the capability each
command needs in `data.capabilities`. The CLI needs no pairing, token, or approval; it works
whenever ExtraBrain is running with MCP enabled in Settings.

| Commands | Required capability |
| --- | --- |
| `documents import`, `resume`, `status` | `documentImport` |
| `documents list` | `documentMetadata` |
| `documents search` | `indexedSearch` |
| `documents text` | `extractedText` |
| `documents export` | `originalExport` |
| `documents delete` | `revisionSafeDelete` |

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
separate them from options. On Windows, pass native paths such as `C:\Users\me\notes.md` or
`C:/Users/me/notes.md`; in Git Bash, convert a POSIX path such as `/tmp/...` or `/c/...` with
`cygpath -m` first. Use `--recursive` only when the user intends to include nested directories. Directory import is additive: missing files
never delete existing documents.

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

To write the exact original bytes to a new file:

```sh
extrabrain --json documents export --output "/absolute/path/to/new-copy.pdf" <document-id>
```

Export requires available managed source bytes and a new output path. The CLI refuses to
overwrite an existing file. Report unavailable originals instead of reconstructing them from
extracted text.

## Delete one document

Delete only when the user explicitly requests it. List documents to identify the target and
read its current `revision`, then:

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
| `3` | ExtraBrain is not reachable. Have the user start it and enable MCP in Settings. |
| `4` | The app or CLI predates URL-only access. Have the user update both. |
| `5` | Refresh metadata/status and resolve the reported conflict before retrying. |
| `6` | Inspect every file result; resume only the same import intent. |
| `7` | The CLI could not use protected storage: the macOS Keychain, or on Windows the DPAPI-protected credential file under `%LOCALAPPDATA%\ExtraBrain`. Have the user restore access to it. |
| `8` | The API, capability, document, text, or original may be unavailable. Follow the specific error. |

The CLI connects to `127.0.0.1:37373` by default. Set `EXTRABRAIN_PORT` only when the app is
configured to use another local port. The CLI does not start the app. While MCP is off, the app
cannot serve CLI document commands; use the app's native import UI when appropriate.

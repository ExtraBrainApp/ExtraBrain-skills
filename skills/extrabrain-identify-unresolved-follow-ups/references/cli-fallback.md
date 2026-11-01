# Reading a session without Node.js

Use this only when `node` is not available. Run every command with `--json`. The reply is
`{ "code": number, "data": object | null, "message": string }`, and any non-zero code is a failure.

1. `extrabrain --json capabilities`. You need `data.sessionApiVersion` to be `"v1"` and `data.capabilities.sessionData` to be true.
2. `extrabrain --json sessions search <words>` or `extrabrain --json sessions list --limit 10`. Use `summaryTitle`, `startedAt` (Unix seconds) and `endedAt` to describe each session.
3. `extrabrain --json sessions get <session-id>`. `data.counts.transcripts` is the number of lines.
4. `extrabrain --json sessions transcripts --limit 200 <session-id>`. While `data.nextCursor` is not null, run the same command with `--cursor <nextCursor>` added. If you get a `SNAPSHOT_CONFLICT` error, start again from step 3.
   Rows come **newest first**. Sort them by `startTimeMs` before you read them. When `startTimeMs` is null, use `createdAt - startedAt` instead.
   Rows with `audioSource: "microphone"` are the user. All other rows are other people: use `speaker` if it is set, and otherwise call them "Other".
   If `content` is an object with a `contentId`, read it with `extrabrain --json sessions content --snapshot <snapshot> --offset 0 --max-chars 100000 <session-id> <contentId>`. Repeat with the returned `nextOffset` until it is null.
5. `extrabrain --json sessions questions <session-id>` and `extrabrain --json sessions facts <session-id>` hold the questions and facts the app detected. Treat them as hints. The transcript is the evidence.

Show times as `mm:ss` from the start of the session.

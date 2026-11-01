#!/usr/bin/env node
// Read one ExtraBrain session through the extrabrain CLI and print it as a compact,
// chronological transcript that any agent can read in a terminal.
//
//   node read-session.mjs find [words...]        recent sessions, or sessions matching the words
//   node read-session.mjs read <session-id> [--page <n>]
//
// Read-only: it runs `extrabrain --json` session commands, exports into a new private
// temporary directory, prints text, and deletes the export. No dependencies beyond Node.js.
import { spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const PAGE_CHARS = 8000 // stays under the tool-output limits of common agent harnesses
const MERGE_GAP_MS = 8000
const MERGE_MAX_CHARS = 600

const fail = (message, code = 1) => {
  process.stdout.write(`ERROR: ${message}\n`)
  process.exit(code)
}

const isSnapshotConflict = (status, message) => status === 5 || /snapshot/i.test(message ?? '')

const cli = (args, { retryConflict = false } = {}) => {
  const result = spawnSync('extrabrain', ['--json', ...args], {
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
    windowsHide: true // no console window flashes when the agent runs as a desktop app on Windows
  })
  if (result.error) {
    fail(
      result.error.code === 'ENOENT'
        ? 'The extrabrain command was not found. Install it from https://github.com/ExtraBrainApp/ExtraBrain-cli and open a new terminal.'
        : `Could not run extrabrain: ${result.error.message}`
    )
  }
  let body
  try {
    body = JSON.parse(result.stdout)
  } catch {
    fail(`extrabrain returned no JSON (exit ${result.status}): ${(result.stderr || result.stdout).trim()}`)
  }
  if (result.status !== 0 || body.code !== 0) {
    if (retryConflict && isSnapshotConflict(result.status, body.message)) return null
    const hint = isSnapshotConflict(result.status, body.message)
      ? ' ExtraBrain is busy with other reads right now. Wait a minute and try again.'
      : /not found/i.test(body.message)
      ? ' Run `find` to list sessions and their ids.'
      : result.status === 3
        ? ' Start the ExtraBrain app and turn on MCP in Settings, then try again.'
        : result.status === 8
          ? ' Update the ExtraBrain app; this version cannot share sessions yet.'
          : ''
    fail(`extrabrain ${args.join(' ')} failed (exit ${result.status}): ${body.message}.${hint}`, result.status || 1)
  }
  return body.data
}

const preflight = () => {
  const caps = cli(['capabilities'])
  if (caps.sessionApiVersion !== 'v1' || !caps.capabilities?.sessionData) {
    fail('This ExtraBrain app does not share session history yet. Update the app, then try again.', 8)
  }
}

const pad = (n) => String(n).padStart(2, '0')
const clock = (ms) => {
  const s = Math.max(0, Math.floor(ms / 1000))
  const h = Math.floor(s / 3600)
  return h ? `${h}:${pad(Math.floor(s / 60) % 60)}:${pad(s % 60)}` : `${pad(Math.floor(s / 60))}:${pad(s % 60)}`
}
const date = (unix) =>
  new Date(unix * 1000).toLocaleString('en-GB', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
const minutes = (meta) =>
  meta.endedAt && meta.endedAt > meta.startedAt ? `${Math.max(1, Math.round((meta.endedAt - meta.startedAt) / 60))} min` : 'length unknown'
const summaryLine = (s) =>
  `${s.id} | ${s.summaryTitle || '(untitled)'} | ${date(s.startedAt)} | ${minutes(s)} | ${s.status}`

const find = (words) => {
  preflight()
  const query = words.join(' ').trim()
  const page = query ? cli(['sessions', 'search', '--limit', '10', query]) : cli(['sessions', 'list', '--limit', '10'])
  const items = page.items ?? []
  const label = query ? `Sessions matching "${query}"` : 'Most recent sessions'
  const lines = [`${label}: ${items.length} of ${page.totalCount ?? items.length} (newest first)`, 'id | title | started | length | status']
  for (const s of items) lines.push(summaryLine(s) + (s.snippet && query ? `\n    match: ${s.snippet.replace(/\s+/g, ' ').trim()}` : ''))
  if (!items.length) lines.push('No sessions found. Try other words, or run `find` with no words to see recent sessions.')
  process.stdout.write(lines.join('\n') + '\n')
}

// Windows antivirus and indexers can hold a just-written file for a moment, so retry the delete.
const removeQuietly = (path) => {
  try {
    rmSync(path, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 })
  } catch {
    // Leave it to the OS temp cleanup rather than fail a finished read.
  }
}

const readJsonl = (file) =>
  existsSync(file)
    ? readFileSync(file, 'utf8')
        .split('\n')
        .filter(Boolean)
        .map((line) => JSON.parse(line))
    : []

const read = (sessionId, pageNumber) => {
  preflight()
  const meta = cli(['sessions', 'get', sessionId])
  const parent = mkdtempSync(join(tmpdir(), 'extrabrain-session-'))
  // fail() exits the process, which skips finally blocks, so also clean up on exit.
  process.on('exit', () => removeQuietly(parent))
  let dir
  try {
    // The app can drop a read snapshot while an export runs; start a fresh export.
    for (let attempt = 1; ; attempt++) {
      dir = join(parent, `export-${attempt}`)
      if (cli(['sessions', 'export', '--output', dir, sessionId], { retryConflict: attempt < 6 })) break
      rmSync(dir, { recursive: true, force: true })
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 300 * attempt + Math.random() * 1000)
    }
    const manifest = JSON.parse(readFileSync(join(dir, 'manifest.json'), 'utf8'))
    const text = (value) => {
      if (value && typeof value === 'object' && value.contentId) {
        const entry = manifest.content?.[value.contentId]
        return entry ? readFileSync(join(dir, entry.file), 'utf8') : '[long text unavailable]'
      }
      return typeof value === 'string' ? value : ''
    }
    const offset = (row) =>
      row.startTimeMs ?? Math.max(0, ((row.createdAt ?? meta.startedAt) - meta.startedAt) * 1000)
    // The API returns newest first; reading needs oldest first.
    const rows = readJsonl(join(dir, 'transcripts.jsonl'))
      .map((row) => ({
        at: offset(row),
        who: row.audioSource === 'microphone' ? 'You' : row.speaker || 'Other',
        text: text(row.content).replace(/\s+/g, ' ').trim()
      }))
      .filter((row) => row.text)
      .sort((a, b) => a.at - b.at)
    const turns = []
    for (const row of rows) {
      const last = turns.at(-1)
      if (last && last.who === row.who && row.at - last.end <= MERGE_GAP_MS && last.text.length + row.text.length < MERGE_MAX_CHARS) {
        last.text += ` ${row.text}`
        last.end = row.at
      } else turns.push({ ...row, end: row.at })
    }
    const mine = rows.filter((r) => r.who === 'You').length
    const others = [...new Set(rows.filter((r) => r.who !== 'You').map((r) => r.who))]
    const header = [
      `SESSION ${meta.id}`,
      `Title: ${meta.summaryTitle || '(untitled)'}`,
      `Started: ${date(meta.startedAt)} (local time) | Length: ${minutes(meta)} | Status: ${meta.status}`,
      `Transcript: ${rows.length} lines, ${mine} from your microphone ("You"), others: ${others.join(', ') || 'none'}`,
      meta.summaryDescription ? `App summary: ${meta.summaryDescription}` : null,
      `Complete export: ${manifest.retrieval?.complete === false ? 'NO, some records were unavailable' : 'yes'}`
    ].filter(Boolean)
    const extras = []
    const questions = readJsonl(join(dir, 'questions.jsonl'))
    if (questions.length) {
      extras.push('', 'Questions the app detected (oldest first):')
      for (const q of questions.sort((a, b) => a.createdAt - b.createdAt))
        extras.push(`- [${clock((q.createdAt - meta.startedAt) * 1000)}] ${text(q.questionText)}`)
    }
    const facts = readJsonl(join(dir, 'facts.jsonl')).filter((f) => f.status !== 'superseded')
    if (facts.length) {
      extras.push('', 'Facts the app noted:')
      for (const f of facts.slice(0, 15)) extras.push(`- ${text(f.factText)}`)
      if (facts.length > 15) extras.push(`- (${facts.length - 15} more facts not shown; the transcript is the source of truth)`)
    }
    const body = turns.map((t) => `[${clock(t.at)}] ${t.who}: ${t.text}`)
    const pages = [[]]
    let size = 0
    for (const line of body) {
      if (size + line.length > PAGE_CHARS && pages.at(-1).length) {
        pages.push([])
        size = 0
      }
      pages.at(-1).push(line)
      size += line.length + 1
    }
    const page = Math.min(Math.max(1, pageNumber), pages.length)
    const out = page === 1 ? [...header, ...extras, ''] : [`SESSION ${meta.id} (continued)`]
    out.push(`Transcript page ${page} of ${pages.length}. [mm:ss] is time from the start; "You" is the microphone.`)
    out.push(...pages[page - 1])
    out.push(
      page < pages.length
        ? `--- More: run this script again with: read ${meta.id} --page ${page + 1}`
        : '--- End of transcript.'
    )
    process.stdout.write(out.join('\n') + '\n')
  } finally {
    removeQuietly(parent)
  }
}

const [command, ...rest] = process.argv.slice(2)
if (command === 'find') find(rest)
else if (command === 'read' && rest[0]) {
  const at = rest.indexOf('--page')
  read(rest[0], at >= 0 ? Number(rest[at + 1]) || 1 : 1)
} else fail('Usage: node read-session.mjs find [words...] | read <session-id> [--page <n>]', 2)

import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtempSync, writeFileSync, chmodSync, readdirSync, readFileSync, rmSync, existsSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { spawnSync } from 'node:child_process'

const SCRIPT_PATH = 'scripts/read-session.mjs'
const RECOVERY_HEADING = '## Recover a local connection'

const allSkills = readdirSync('skills').filter((name) => existsSync(`skills/${name}/SKILL.md`))
const scriptSkills = allSkills.filter((name) => existsSync(`skills/${name}/${SCRIPT_PATH}`))

/** Runs `read-session.mjs find` against a fake `extrabrain` whose source is `body`. */
const runWithFakeCli = (skill, body) => {
  const dir = mkdtempSync(join(tmpdir(), 'skill-cli-'))
  try {
    const executable = join(dir, 'extrabrain')
    writeFileSync(executable, `#!${process.execPath}\n${body}\n`)
    chmodSync(executable, 0o755)
    return spawnSync(process.execPath, [resolve(`skills/${skill}/${SCRIPT_PATH}`), 'find'], {
      encoding: 'utf8',
      env: { ...process.env, PATH: `${dir}:${process.env.PATH}` }
    })
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }
}

const failingCli = (status, payload) =>
  `console.log(${JSON.stringify(JSON.stringify({ code: status, ...payload }))});process.exit(${status})`

const recoverySection = (skill) => {
  const text = readFileSync(`skills/${skill}/SKILL.md`, 'utf8')
  const start = text.indexOf(RECOVERY_HEADING)
  assert.notEqual(start, -1, `${skill} has no recovery section`)
  const next = text.indexOf('\n## ', start + RECOVERY_HEADING.length)
  return next === -1 ? text.slice(start) : text.slice(start, next)
}

// Each skill installs on its own, so shared code is copied. These keep the copies identical.
test('every read-session script is an identical copy', () => {
  const copies = new Set(scriptSkills.map((skill) => readFileSync(`skills/${skill}/${SCRIPT_PATH}`, 'utf8')))
  assert.ok(scriptSkills.length > 0)
  assert.equal(copies.size, 1)
})

test('every skill has the same connection recovery section', () => {
  assert.equal(new Set(allSkills.map(recoverySection)).size, 1)
})

for (const skill of scriptSkills) {
  for (const error of ['LOCAL_ACCESS_BLOCKED', 'CONNECTION_REFUSED', 'CLI_ACCESS_DISABLED', undefined]) {
    test(`${skill}: preserves ${error ?? 'legacy'} recovery without retrying itself`, () => {
      const data = error ? { error } : null
      const result = runWithFakeCli(skill, failingCli(3, { data, message: 'Connection unavailable.' }))
      assert.equal(result.status, 3)
      assert.match(result.stdout, /Could not connect to ExtraBrain/)
      assert.match(result.stdout, new RegExp(error ?? 'CONNECTION_UNAVAILABLE'))
      assert.doesNotMatch(result.stdout, /Start the ExtraBrain app|\.\./)
    })
  }

  for (const [name, status, message, hint] of [
    ['a snapshot conflict', 5, 'snapshot changed', /busy with other reads/],
    ['a missing session', 1, 'session not found', /Run `find`/],
    ['an outdated app', 8, 'unsupported', /Update the ExtraBrain app/]
  ]) {
    test(`${skill}: explains ${name}`, () => {
      const result = runWithFakeCli(skill, failingCli(status, { data: null, message }))
      assert.equal(result.status, status)
      assert.match(result.stdout, hint)
    })
  }

  test(`${skill}: successful reads still list sessions`, () => {
    const data = `process.argv.includes('capabilities') ? { sessionApiVersion: 'v1', capabilities: { sessionData: true } } : { items: [], totalCount: 0 }`
    const result = runWithFakeCli(skill, `console.log(JSON.stringify({ code: 0, data: ${data}, message: 'ok' }))`)
    assert.equal(result.status, 0)
    assert.match(result.stdout, /Most recent sessions: 0/)
  })
}

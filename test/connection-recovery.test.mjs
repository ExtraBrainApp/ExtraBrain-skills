import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtempSync, writeFileSync, chmodSync, readdirSync, rmSync, existsSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { spawnSync } from 'node:child_process'

const skills = readdirSync('skills').filter(name => existsSync(`skills/${name}/scripts/read-session.mjs`))
for (const skill of skills) {
  for (const error of ['LOCAL_ACCESS_BLOCKED', 'CONNECTION_REFUSED', 'CLI_ACCESS_DISABLED', undefined]) {
    test(`${skill}: preserves ${error ?? 'legacy'} recovery without retrying itself`, () => {
      const dir = mkdtempSync(join(tmpdir(), 'skill-cli-'))
      try {
        const executable = join(dir, 'extrabrain')
        writeFileSync(executable, `#!${process.execPath}\nconsole.log(${JSON.stringify(JSON.stringify({code:3,data:error ? {error} : null,message:'connection unavailable'}))});process.exit(3)\n`)
        chmodSync(executable, 0o755)
        const result = spawnSync(process.execPath, [resolve(`skills/${skill}/scripts/read-session.mjs`), 'find'], { encoding: 'utf8', env: {...process.env, PATH: dir + ':' + process.env.PATH} })
        assert.equal(result.status, 3)
        assert.match(result.stdout, /Connection recovery required/)
        assert.match(result.stdout, new RegExp(error ?? 'CONNECTION_UNAVAILABLE'))
        assert.doesNotMatch(result.stdout, /Start the ExtraBrain app/)
      } finally { rmSync(dir, {recursive:true,force:true}) }
    })
  }
  test(`${skill}: successful reads still list sessions`, () => {
    const dir = mkdtempSync(join(tmpdir(), 'skill-cli-'))
    try {
      const executable = join(dir, 'extrabrain')
      writeFileSync(executable, `#!${process.execPath}\nconsole.log(JSON.stringify({code:0,data:process.argv.includes('capabilities')?{sessionApiVersion:'v1',capabilities:{sessionData:true}}:{items:[],totalCount:0},message:'ok'}))\n`)
      chmodSync(executable,0o755)
      const result=spawnSync(process.execPath,[resolve(`skills/${skill}/scripts/read-session.mjs`),'find'],{encoding:'utf8',env:{...process.env,PATH:dir+':'+process.env.PATH}})
      assert.equal(result.status,0)
      assert.match(result.stdout,/Most recent sessions: 0/)
    } finally {rmSync(dir,{recursive:true,force:true})}
  })
}

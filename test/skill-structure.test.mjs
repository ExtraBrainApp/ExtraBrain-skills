import { test } from 'node:test'
import assert from 'node:assert/strict'
import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'

const FRONTMATTER = /^---\n([\s\S]*?)\n---\n/
const LOCAL_LINK = /\]\(([^)#\s]+)\)/g

const skills = readdirSync('skills').filter((name) => existsSync(`skills/${name}/SKILL.md`))

const markdownFiles = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name)
    if (entry.isDirectory()) return markdownFiles(path)
    return entry.name.endsWith('.md') ? [path] : []
  })

const field = (frontmatter, name) => frontmatter.match(new RegExp(`^${name}: *(.+)$`, 'm'))?.[1].trim()

test('the repository has skills to validate', () => {
  assert.ok(skills.length > 0)
})

for (const skill of skills) {
  test(`${skill}: frontmatter names the skill and describes it`, () => {
    const frontmatter = readFileSync(`skills/${skill}/SKILL.md`, 'utf8').match(FRONTMATTER)?.[1]
    assert.ok(frontmatter, 'SKILL.md has no frontmatter')
    assert.equal(field(frontmatter, 'name'), skill)
    assert.ok(field(frontmatter, 'description'), 'description is empty')
  })

  test(`${skill}: local links resolve inside the skill`, () => {
    for (const file of markdownFiles(`skills/${skill}`)) {
      for (const [, target] of readFileSync(file, 'utf8').matchAll(LOCAL_LINK)) {
        if (/^[a-z][a-z+.-]*:/i.test(target)) continue
        assert.ok(existsSync(join(dirname(file), target)), `${file} links to missing ${target}`)
      }
    }
  })
}

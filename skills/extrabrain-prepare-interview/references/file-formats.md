# Interview Preparation File Formats

Every file must contain every required section for its kind, in the order given, with these
exact `##` heading prefixes. You may add extra `##` sections between required ones when a topic
needs them. If a required section matters little for a topic, still write it: say briefly why
and what to know anyway. Never omit it.

## Completion checklist

Every item is mandatory. `scripts/validate_prep.py` checks the structural items automatically
when Python 3 is available; otherwise check each one by hand for every file. No script checks the
accuracy and consistency items: review them yourself for every file.

Directory:

- [ ] One `00-<interview-slug>-brief.md` and 3 to 12 topic files named
      `NN-<interview-slug>-<topic-slug>.md`, numbered from 01 without gaps, each under 10 MiB,
      and no other files.

Brief:

- [ ] First line `# <Interview title>: Interview brief`.
- [ ] `##` sections in order: `The interview`, `What they will assess`, `Research summary`,
      `Preparation files`, `Preparation plan`, `Questions to ask them`, `Sources`.
- [ ] `Preparation files` is a numbered list with exactly one item per topic file.
- [ ] `Questions to ask them` has at least three numbered questions.

Each topic file:

- [ ] First line `# <Interview title>: <Topic title>`, followed by a `**Kind:**` line naming one
      of `questions`, `concepts`, `stories`, `case`, or `cheatsheet`.
- [ ] Every required section for its kind, in order, each `##` heading ending with
      ` - <short topic name>`, and each except Sources with at least 150 characters of content.
- [ ] The kind-specific checks below.
- [ ] No paragraph or list block over 1,500 characters outside fenced code.

Brief and topic files:

- [ ] A Sources section with URLs, or the line `User-provided material` when the file relies
      only on what the user supplied, and every `[S#]` cited in the file listed there.

Accuracy and consistency, for each topic file:

- [ ] Every factual claim is correct for the field and current: definitions, APIs and their
      complexity, formulas, regulations, protocols, and company facts. Claims you could not
      verify are marked as such or removed.
- [ ] Every code sample, calculation, and worked example is recomputed or traced by hand and
      gives the stated result. Each number has one value across sections and files.
- [ ] Model answers, follow-ups, and walkthroughs agree with each other and with the concepts,
      cases, and cheat sheets they rely on; no file contradicts another.
- [ ] Stories use only details the user supplied; every gap is marked `[confirm: ...]`, and
      each story's `Use for` matches the questions that point to it.
- [ ] A `case` with a technical design is internally consistent: every table, field, and status
      the API or flows use is defined in its data model, idempotency keys match the stored
      unique keys, and every uniqueness guarantee is enforceable in the chosen store.

Brief:

- [ ] Its file list, assessed areas, and points to memorise match the final topic files exactly.

## Write for live retrieval

During the interview, ExtraBrain retrieves imported documents with keyword search and receives
about five chunks of roughly 1,600 characters for each answer. So:

- End each `##` heading with ` - <short topic name>`, for example
  `## Q3. How do you handle a missed deadline? - Delivery stories`, so every chunk names its
  topic.
- Make each question its own `##` section, so a chunk holds a whole question and its answer.
- Open each section with one plain sentence that names the interview topic it belongs to. Keep
  paragraphs and lists under about 1,200 characters, separated by blank lines.
- Use the words an interviewer would say, plus concrete names, numbers, and examples. Generic
  advice is not useful in a live interview.
- Write answers the user could say aloud: lead with the direct answer, then the support.

## Interview brief

````markdown
# <Interview title>: Interview brief

## The interview
Company, role, level, round or rounds, format, duration, interviewers, date, and language, with
what is known versus assumed.

## What they will assess
The competencies, skills, and knowledge areas in priority order, each with the evidence for it
(job posting, reported process, role norms) and citations [S#].

## Research summary
What the company or organisation does, its current priorities, and facts worth mentioning in
answers. For a subject-only interview, the syllabus or standard the questions draw on.

## Preparation files
1. `01-<interview-slug>-<topic-slug>.md` (`<kind>`): one line on what it covers and why.

## Preparation plan
A schedule up to the interview date when known, otherwise by priority. For each file, the points
to memorise. Then how to use ExtraBrain during the interview: which profile to pin and that the
group's documents are searched for each answer.

## Questions to ask them
At least three numbered, specific questions for the interviewer, each with why it is a good one.

## Sources
Numbered URLs cited in this file as [S1], [S2], and so on, or `User-provided material`.
````

## Topic file header

Every topic file starts with:

```markdown
# <Interview title>: <Topic title>

**Kind:** <questions | concepts | stories | case | cheatsheet> · **Priority:** <High | Medium | Lower> · **Round:** <round>
```

Then the sections for its kind. Every kind starts with `Why it matters` and ends with `Sources`.

## Kind: questions

A bank of likely questions with full model answers.

````markdown
## Why it matters - <short>
Why this topic will come up in this interview, with citations [S#].

## Q1. <The question as an interviewer would ask it> - <short>
**What they are testing:** one sentence.
**Model answer:** the complete answer the user could give, in their voice and at their level.
**Follow-ups:** two or three likely follow-ups, each with a one- or two-sentence answer.

## Q2. ... - <short>
(at least eight questions, ordered from most to least likely)

## Common mistakes - <short>
The answers that lose points on this topic and what to say instead.

## Sources - <short>
````

Checks: at least eight `Q<n>.` sections, each containing `Model answer`.

## Kind: concepts

Knowledge notes for a subject the interview will probe.

````markdown
## Why it matters - <short>

## Core concepts - <short>
Each concept with a precise definition, how it works, and when it applies. Add more `##`
sections after this one for large sub-areas, each ending with ` - <short>`.

## Worked examples - <short>
At least two concrete examples worked through step by step: code, calculations, scenarios, or
procedures, as the field requires.

## Common mistakes - <short>

## Likely questions - <short>
At least six numbered questions, each with a two- to four-sentence answer.

## Sources - <short>
````

Checks: at least six numbered items in `Likely questions`.

## Kind: stories

Behavioral stories built only from the user's real experience. When a detail is unknown, write
`[confirm: ...]` rather than inventing it, and list those gaps in the response.

````markdown
## Why it matters - <short>
The competencies or values this interviewer assesses, with citations [S#].

## Competency map - <short>
A table mapping each competency to the story that best evidences it.

## Story 1. <Short title> - <short>
**Situation:** ... **Task:** ... **Action:** what the user personally did, with specifics.
**Result:** measurable outcome. **Lesson:** what they would repeat or change.
**Use for:** the questions this story answers.

## Story 2. ... - <short>
(at least three stories)

## Likely questions - <short>
At least six numbered behavioral questions, each naming the story to use and the angle to stress.

## Sources - <short>
````

Checks: at least three `Story <n>.` sections, each containing `Situation`, `Action`, and
`Result`; a table in `Competency map`; at least six numbered items in `Likely questions`.

## Kind: case

A case or design problem with a complete model walkthrough: system or ML design, product sense,
consulting or market sizing, a clinical or legal scenario, a take-home presentation.

````markdown
## Why it matters - <short>

## Prompt - <short>
The case as the interviewer would state it.

## Clarifying questions - <short>
Questions to ask first and the assumption to make for each if unanswered.

## Approach - <short>
The framework or structure to follow and why it fits this case.

## Model answer - <short>
The full walkthrough with concrete content: numbers, designs, decisions, and their reasoning.
For a technical design include the API, data model, architecture, and scaling. Add more `##`
sections after this one for large parts of the answer.

## Trade-offs and alternatives - <short>

## Follow-ups - <short>
At least five numbered follow-up questions, each with a two- or three-sentence answer.

## Timed walkthrough - <short>
At least three timed phases such as `0–5 min`, each with what to say and one thing to watch.

## Sources - <short>
````

Checks: at least five numbered items in `Follow-ups`; at least three timed phases in
`Timed walkthrough`.

## Kind: cheatsheet

Dense quick-reference material to glance at during preparation or the interview.

````markdown
## Why it matters - <short>

## Quick reference - <short>
Facts, numbers, formulas, definitions, commands, or snippets, as tables or short lists. Add more
`##` sections after this one to group them.

## Likely questions - <short>
At least six numbered questions answered directly from the reference above.

## Sources - <short>
````

Checks: a table or list in `Quick reference`; at least six numbered items in `Likely questions`.

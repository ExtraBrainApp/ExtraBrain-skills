# System Design Problem Template

Use these sections, in this order, for each problem file. Keep the whole file under about
2,500 words so it reads well as an ExtraBrain reference document. Use concrete numbers, names,
and examples from the company research instead of generic placeholders.

```markdown
# <Company>: <Problem title>

**Likelihood:** <High | Medium | Lower> · **Focus:** <main skills tested>

## Why this fits <Company>
Two to four sentences tying the problem to a specific product or flow, citing [S#] sources.

## Interview prompt
The prompt as an interviewer would say it, in one short paragraph.

## Clarifying questions
Five to eight questions to ask first, each with the assumption you would take if the
interviewer leaves it open.

## Requirements
- Functional: the core user flows in scope, and what is explicitly out of scope.
- Non-functional: latency, availability, consistency, durability, privacy, and compliance targets.

## Scale estimates
Users, requests per second (average and peak), storage and its growth, and bandwidth. Show the
arithmetic. Label numbers that are assumptions rather than sourced.

## API and data model
The main endpoints or events, the core entities with key fields, the storage choice for each,
and partitioning keys.

## High-level design
The components and the request path for the main flows, as a short list or a Mermaid diagram.

## Deep dives
Two or three areas the interviewer is most likely to push on for this company, each with the
options considered, the chosen approach, and why. Examples: preventing double booking,
idempotent payments, fan-out, hot keys, search indexing, or regional failover.

## Trade-offs and failure modes
What breaks first at 10x scale, how the design degrades, and what you would monitor.

## Company-specific twists
Constraints particular to <Company>'s market, regulation, product, or known stack that set a
strong answer apart from a generic one.

## Follow-up questions
Four to six likely follow-ups, each with a one- or two-sentence answer outline.

## Sources
Numbered URLs cited in this file as [S1], [S2], and so on. Repeat them in every file so each
document stands alone in ExtraBrain search.
```

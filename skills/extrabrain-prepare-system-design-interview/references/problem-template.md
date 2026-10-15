# System Design Problem Template

Every problem file must contain every section below, in this order, with these exact `##`
heading prefixes. If a section matters little for a problem, still write it: say briefly why it
is minor and what you would do anyway. Never omit it.

## Completion checklist

Every item is mandatory. `scripts/validate_prep.py` checks the same items automatically when
Python 3 is available; otherwise check each one by hand for every file.

Directory:

- [ ] Exactly six files: `00-<company-slug>-company-brief.md` and five
      `0N-<company-slug>-<problem-slug>.md` files numbered 01–05, each under 10 MiB.

Company brief:

- [ ] First line `# <Company>: ...`.
- [ ] `##` sections in order: `What <Company> builds`, `Scale`, `Engineering signals`,
      `Interview format`, `The five practice problems`, `Preparation plan`, `Sources`.
- [ ] `The five practice problems` is a numbered list of exactly five.

Each problem file:

- [ ] First line `# <Company>: <Problem title>`, followed by a `**Likelihood:**` line.
- [ ] All 22 `##` sections below, numbered `1.`–`22.` in order, each heading ending with
      ` - <short problem name>`, and each except Sources with at least 200 characters of content.
- [ ] Scale estimation: QPS math with numbers, and storage both raw and replicated.
- [ ] API design: an endpoint table, HTTP methods (or named RPCs), a fenced example request and
      response, and idempotency for writes.
- [ ] Data model: a fenced DDL or key schema, primary or partition keys, and indexes.
- [ ] High-level architecture: exactly one fenced `d2` diagram with `direction: down`, every
      edge labelled (`a -> b: action`), no D2 reserved word (`index`, `shape`, `label`,
      `style`, `class`, `source`, `target`, and so on) used as a node ID, and numbered flow steps.
- [ ] Follow-up questions: at least six numbered items.
- [ ] 45-minute walkthrough: at least four timed phases such as `0–5 min`.
- [ ] No paragraph or list block over 1,500 characters outside fenced code.

Brief and problem files:

- [ ] Sources section with URLs, and every `[S#]` cited in the file listed there.

## Write for live retrieval

During the interview, ExtraBrain's System Design copilot answers one phase at a time
(requirements, high-level design, API, data model, storage, caching, consistency, sharding,
queues, search, rate limiting, monitoring). It retrieves imported documents with keyword search,
at most once per answer, receiving about five chunks of roughly 1,600 characters. So:

- End each `##` heading with ` - <short problem name>`, for example
  `## 6. API design - Streaks`, so every chunk names its problem.
- Open each section with one plain sentence that names the company, the problem, and the phase.
  Keep paragraphs and lists under about 1,200 characters, separated by blank lines.
- Use concrete technology names, numbers, and field names. Generic advice is not useful in a
  live interview.
- Use the terms an interviewer would say: endpoint, schema, partition key, TTL, fan-out,
  idempotency key, p99, QPS, replication factor.

## Template

````markdown
# <Company>: <Problem title>

**Likelihood:** <High | Medium | Lower> · **Level:** <level> · **Focus:** <main skills tested>

## 1. Why this fits <Company> - <short name>
Two to four sentences tying the problem to a specific product or flow, citing [S#] sources.

## 2. Interview prompt - <short name>
The prompt as an interviewer would say it, in one short paragraph.

## 3. Clarifying questions - <short name>
**Ask first:** five to eight questions covering functional scope, core flows, scale,
read/write ratio, growth horizon, existing stack, and the key non-functional constraint.
**If unanswered, assume:** the bounded assumption for each, labelled as an assumption.

## 4. Requirements - <short name>
- Functional: numbered core user flows in scope; explicitly out of scope.
- Non-functional: availability target, latency budget (p50/p99), consistency per flow,
  durability, privacy, and compliance.

## 5. Scale estimation - <short name>
Show each multiplication chain with units: users × actions/user/day = requests/day →
average QPS → peak QPS (state the peak factor). Cover read QPS, write QPS, read:write ratio,
storage per record × records = storage/day → per year, raw and replicated (for example
"2 TB raw, 6 TB with 3× replication"), bandwidth, and cache size. Label sourced numbers [S#]
and every other number as an assumption.

## 6. API design - <short name>
A table with one row per endpoint: method, path, purpose, key request fields, response, status
and error codes. Then one fenced example request and response for the most important call.
State authentication, idempotency keys for writes, pagination (cursor), versioning, and rate
limits. List asynchronous events or webhooks with their payload fields. Choose REST, gRPC,
WebSocket, or SSE per interface and say why.

## 7. Data model and schema - <short name>
Each entity with fields and types, primary key, partition and sort keys, secondary indexes,
and relationships. Give SQL DDL or a key-value/document key schema in a fenced block. Show the
access pattern each index serves and data retention (TTL, archival).

## 8. Storage choice - <short name>
For each data set: the specific store (for example PostgreSQL, DynamoDB, Cassandra, Redis, S3,
Elasticsearch, ClickHouse), why it fits the access pattern, and the alternative you rejected.
Prefer the company's known stack when sources show it.

## 9. High-level architecture - <short name>
The services with one-line responsibilities, synchronous vs asynchronous boundaries, and
external dependencies. Include one fenced `d2` diagram (`direction: down`, 6–12 nodes, every
edge labelled with its action, no D2 reserved words such as `index` as node IDs). Then walk the
main write flow and the main read flow as numbered steps.

## 10. Read/write path and consistency - <short name>
Where strong consistency is required and where eventual consistency is acceptable, and how each
is achieved: transactions, conditional writes, optimistic locking, idempotency, outbox, or
sagas. Name the race conditions and how they are prevented.

## 11. Caching - <short name>
What is cached and where (client, CDN, Redis, in-process), key format, TTL, eviction policy,
cache-aside or write-through, invalidation, expected hit rate, and hot-key mitigation. Note that
deleting a cache key narrows, but does not eliminate, the stale-read window.

## 12. Sharding, partitioning and replication - <short name>
Partition key and why it spreads load, hot-partition handling, resharding, replication factor,
leader/follower or multi-leader, multi-region strategy, failover, RPO/RTO, and backups.

## 13. Async processing, queues and fan-out - <short name>
Queues or streams (for example Kafka, SQS, Kinesis), topics and partitions, consumer groups,
delivery semantics, retries with backoff, dead-letter queues, ordering, backpressure, and
scheduled jobs.

## 14. Search and indexing - <short name>
Search or secondary lookups, the index technology, how the index is updated and how stale it
may be. If the problem has no search component, say so and describe the lookups it does need.

## 15. Security, auth, rate limiting and abuse - <short name>
Authentication and authorization, PII and encryption, rate limits by user and IP, abuse or
fraud vectors specific to this product, and compliance (for example GDPR deletion, PCI).

## 16. Reliability, monitoring and SLOs - <short name>
SLOs with targets, key metrics and alerts, dashboards, tracing, graceful degradation and
fallbacks, load shedding, and rollout safety (canary, feature flags).

## 17. Deep dives - <short name>
Two or three areas the interviewer is most likely to push on for this company. For each: the
problem, two options compared, the choice, and its cost.

## 18. Bottlenecks, trade-offs and evolution - <short name>
What breaks first at 10× scale and the metric that reveals it, key trade-offs made, and how
the design evolves (MVP → current scale → 10×).

## 19. Company-specific twists - <short name>
Constraints particular to <Company>'s market, regulation, product, or known stack that set a
strong answer apart from a generic one.

## 20. Follow-up questions - <short name>
Six to eight likely follow-ups, each with a two- or three-sentence answer.

## 21. 45-minute walkthrough - <short name>
A timed script of what to say: 0–5 min clarify (§3–4), 5–10 estimation (§5), 10–20 API, data
model, and high-level design with a buy-in checkpoint (§6–9), 20–38 deep dives the interviewer
picks (§10–17), 38–45 bottlenecks and wrap-up (§18). For each phase give the one-sentence
recommendation and the one "watch out" to mention.

## 22. Sources - <short name>
Numbered URLs cited in this file as [S1], [S2], and so on. Repeat them in every file so each
document stands alone. Mark search-snippet-only sources `(snippet only)`.
````

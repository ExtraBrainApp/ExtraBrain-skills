# ExtraBrain Skills

Skills for agents working with the [ExtraBrain application](https://github.com/ExtraBrainApp/ExtraBrain).

## Install

```sh
npx skills add ExtraBrainApp/ExtraBrain-skills
```

To inspect the available skills first:

```sh
npx skills add ExtraBrainApp/ExtraBrain-skills --list
```

These skills use the standalone [ExtraBrain CLI](https://github.com/ExtraBrainApp/ExtraBrain-cli) for reference documents, read-only session evidence, pairing, capability discovery, and CLI updates.

Install the CLI using its repository's installation instructions. Document operations require a running ExtraBrain app with local document automation enabled, an approved CLI connection, and access to the same filesystem as the files being imported. The CLI currently supports macOS arm64 and x64 releases.

## Skills

- `use-extrabrain` - Manage reference documents through the CLI.
- `extrabrain-check-grammar` - Find high-value grammar, phrasing, and word-choice improvements in your speech.
- `extrabrain-extract-action-items` - Extract action items you personally committed to.
- `extrabrain-review-communication` - Review your meeting communication and better wording options.
- `extrabrain-identify-unresolved-follow-ups` - Identify high-impact open questions, decisions, and follow-ups.
- `extrabrain-review-interview` - Review your interview answers and improve future responses.

The five session skills generate insights in the agent and do not save them to ExtraBrain. They require a compatible running app that advertises `sessionApiVersion: "v1"` and the required session capabilities. The CLI source contract inspected is `88ef1fa2e64ec6433ded9ebc929f4e55ca3bdae9`; its README describes session reads as future-app compatibility, so an installed released CLI or document-only app may not expose them yet.

The skill was extracted from [ExtraBrain PR #985](https://github.com/ExtraBrainApp/ExtraBrain/pull/985).

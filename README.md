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
- `extrabrain-prepare-interview` - Prepare for any interview you describe: plan what it will cover, write question banks with model answers, concept notes, story banks, cases, and cheat sheets, import them into ExtraBrain as one document group, and coach you through them.
- `extrabrain-prepare-system-design-interview` - Research a company, write five likely system design cases with full model answers (API, data model, architecture, storage, scaling), import them into ExtraBrain as a document group, and coach you through them.

The five session skills generate insights in the agent and do not save them to ExtraBrain. They require a compatible running app that advertises `sessionApiVersion: "v1"` and the required session capabilities. The CLI source contract inspected is `88ef1fa2e64ec6433ded9ebc929f4e55ca3bdae9`; its README describes session reads as future-app compatibility, so an installed released CLI or document-only app may not expose them yet.

`extrabrain-prepare-system-design-interview` needs the agent's own web research tools and the document capabilities `documentImport`, `documentGroups`, and `documentMetadata`. With `profileSelection` it can also pin the System Design profile after asking. Its validator uses Python 3 when available; without it, the agent checks the same completion checklist by hand. Without the document capabilities it still writes the case files for native import.

`extrabrain-prepare-interview` has the same requirements and fallbacks. To pin a fitting profile (for example Behavioral or System Design) after asking, it also needs `profileRead`.

The `use-extrabrain` skill was extracted from [ExtraBrain PR #985](https://github.com/ExtraBrainApp/ExtraBrain/pull/985).

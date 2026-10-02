# ExtraBrain Skills

Skills for agents working with the [ExtraBrain application](https://github.com/ExtraBrainApp/ExtraBrain).

## Install

```sh
npx skills add ExtraBrainApp/ExtraBrain-skills --skill use-extrabrain
```

To inspect the available skills first:

```sh
npx skills add ExtraBrainApp/ExtraBrain-skills --list
```

The `use-extrabrain` skill uses the standalone [ExtraBrain CLI](https://github.com/ExtraBrainApp/ExtraBrain-cli) to import, list, search, read, export, and delete reference documents. It also covers session evidence, built-in and custom session insights, pairing, capability discovery, and updating the CLI itself.

Install the CLI using its repository's installation instructions. Document operations require a running ExtraBrain app with local document automation enabled, an approved CLI connection, and access to the same filesystem as the files being imported. The CLI currently supports macOS arm64 and x64 releases.

The skill reproduces the five built-in session insights from CLI evidence: English grammar mistakes, My action items, Communication feedback, Unresolved follow-ups, and Interview self-review. It also runs user-defined insight tasks using the app's TASK/CORPUS_SCOPE/RELEVANCE_CRITERIA/EXCLUSIONS/OUTPUT prompt format. Insights are generated in the agent and are not saved to ExtraBrain.

Session insights require a compatible running app that advertises `sessionApiVersion: "v1"` and required session capabilities. The CLI source contract inspected for this skill is `88ef1fa2e64ec6433ded9ebc929f4e55ca3bdae9`; its README describes session reads as future-app compatibility, so an installed released CLI or document-only app may not expose them yet. Session preparation, recording controls, profiles, history, settings, and desktop app updates remain outside the skill's scope.

The skill was extracted from [ExtraBrain PR #985](https://github.com/ExtraBrainApp/ExtraBrain/pull/985).

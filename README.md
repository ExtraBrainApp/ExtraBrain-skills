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

The `use-extrabrain` skill uses the standalone [ExtraBrain CLI](https://github.com/ExtraBrainApp/ExtraBrain-cli) to import, list, search, read, export, and delete reference documents. It also covers pairing, capability discovery, and updating the CLI itself.

Install the CLI using its repository's installation instructions. Document operations require a running ExtraBrain app with local document automation enabled, an approved CLI connection, and access to the same filesystem as the files being imported. The CLI currently supports macOS arm64 and x64 releases.

The skill follows the commands available in the CLI. Session preparation, recording controls, profiles, history, settings, and desktop app updates are outside its current scope.

The skill was extracted from [ExtraBrain PR #985](https://github.com/ExtraBrainApp/ExtraBrain/pull/985).

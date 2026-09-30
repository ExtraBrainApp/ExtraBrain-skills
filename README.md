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

The `use-extrabrain` skill guides an agent through ExtraBrain's authenticated MCP server and paired local document CLI. ExtraBrain must be running for app operations. The CLI document route requires a build that includes the CLI and access to the same filesystem as the files being imported.

The skill was extracted from [ExtraBrain PR #985](https://github.com/ExtraBrainApp/ExtraBrain/pull/985).

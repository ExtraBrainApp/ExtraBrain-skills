# ExtraBrain Skills

Add-ons for your AI assistant (such as Claude Code or Codex) that let it work with [ExtraBrain](https://extrabrain.app). With them, you can ask your assistant in plain language to review a past meeting or interview, pull out your action items, or prepare you for an upcoming interview.

## What is a "skill"?

A skill is a small set of instructions that teaches your AI assistant how to do one specific job. You install it once. After that, you ask for the job in your own words, for example "Check my grammar in my last meeting", and the assistant follows the skill.

## What you need

1. **The ExtraBrain app**, installed and running on your computer. Get it at [extrabrain.app](https://extrabrain.app).
2. **An AI assistant that supports skills**, such as Claude Code or Codex.
3. **The ExtraBrain command-line tool.** Your assistant uses it to talk to the app. Follow the [installation instructions](https://github.com/ExtraBrainApp/ExtraBrain-cli) on its page. It works on Mac only (Apple Silicon and Intel).
4. **Node.js**, which provides the `npx` command used in the install step below. Get it from [nodejs.org](https://nodejs.org).

## How to install

Open the Terminal app on your Mac and run:

```sh
npx skills add ExtraBrainApp/ExtraBrain-skills
```

The installer lists the skills and lets you choose which ones to add. To see the list without installing anything, run:

```sh
npx skills add ExtraBrainApp/ExtraBrain-skills --list
```

## The skills

### Learn from your past meetings and interviews

These four skills read a session you recorded in ExtraBrain and write a short report in your assistant's chat. They only read your data. They never change it, and the reports are not saved back into ExtraBrain.

| Skill | What it does for you |
| --- | --- |
| `extrabrain-check-grammar` | Finds up to 10 of the most useful grammar, phrasing, and word-choice improvements in what you said, with a better version of each. |
| `extrabrain-review-communication` | Reviews how clearly you communicated in a meeting. It shows what worked well, what to improve, and example rewordings. |
| `extrabrain-extract-action-items` | Lists the tasks you personally agreed to take on, with the quote that shows it. |
| `extrabrain-identify-unresolved-follow-ups` | Lists important open questions and undecided topics that still need follow-up. |

### Review a job interview

| Skill | What it does for you |
| --- | --- |
| `extrabrain-review-interview` | Reviews your answers in a recorded interview. It shows your strongest moments, the most important improvements, and stronger versions of your answers. |

### Prepare for a system design interview

| Skill | What it does for you |
| --- | --- |
| `extrabrain-prepare-system-design-interview` | Give it a company name. It researches the company on the web, writes five likely system design questions with complete model answers, adds them to ExtraBrain as a document group, and then coaches you through them. |

### Manage your reference documents

| Skill | What it does for you |
| --- | --- |
| `use-extrabrain` | Lets your assistant add, search, read, export, and delete the reference documents that ExtraBrain uses, and update the command-line tool. |

## Good to know

- The four meeting skills and the interview review skill need a recent version of the ExtraBrain app that supports reading sessions. If your version does not yet, the assistant tells you what is missing.
- Document features need local document automation turned on in the app. The first time, you approve the connection inside ExtraBrain.
- If something is missing, your assistant says what it is and does not guess.

Questions or ideas? Visit [extrabrain.app](https://extrabrain.app).

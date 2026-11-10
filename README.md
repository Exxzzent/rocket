<p align="center"><img src="assets/icon.png" alt="rocket icon" width="160"></p>

# 🚀 rocket

**Staged workflows for coding agents.** You start every task with `/rocket`. A router picks the one workflow that fits the request, and that workflow walks the agent through fixed stages with approval gates. You approve the plan and you validate the result. Everything in between the agent does on its own.

Works with **Claude Code** and **Codex**.

> **Directory edition.** This is the version listed in the Claude plugin directory. It contains the skills only. The full version with the safety hooks (stop guard, git guard) is on the [`main` branch](https://github.com/Exxzzent/rocket/tree/main) and installs with `claude plugin marketplace add Exxzzent/rocket`.

## How it works

### 1. The router picks one workflow

The `rocket` skill classifies the request and announces its choice in the first line of the reply:

```
🚀 rocket → rocket:fix (Bugfix)
```

The line carries only the workflow and its classification. If the choice is wrong, one word corrects it. Each request gets exactly one workflow, so a review stays a review and a bugfix does not turn into a feature project.

| Request | Workflow | Stages |
| --- | --- | --- |
| Feature or refactor | `rocket:launch` | 🧭 Plan ✋ → 🛠️ Build & Verify → 👀 Your test ✋ → 🚀 Done |
| Bug, crash, regression | `rocket:fix` | 🔎 Analysis → 🧭 Findings ✋ → 🛠️ Fix & Verify → 👀 Your test ✋ → 🚀 Done |
| Review only | `rocket:review` | 🔍 Review → 📋 Report |
| Test only | `rocket:test` | 🧪 Test → 📋 Report & 🧹 Cleanup |
| Tiny edit | `rocket:small` | 🧭 Mini plan ✋ → 🛠️ Change ✋ → 🚀 PR |
| Question | `rocket:what` | no stages |

✋ marks a gate where the agent stops and waits for you.

### 2. Plan first, tests included

The agent analyses the request on a fresh baseline and asks open questions only now: at most 2 per round, clickable, with a recommendation. Then it writes a plan to `docs/rocket/plans/` that already contains the test cases with expected results. Nothing is built before you approve the plan. ✋

For a bug, the agent first reproduces it and finds the root cause, then presents the findings and the fix plan for approval.

### 3. Build and verify on its own

After approval the agent works without asking: it implements, runs the builds and the automated tests, and runs a code review. Then a test subagent operates the real app like a user and runs every test case from the plan, with screenshots. Failures are fixed and only the affected cases are retested, until all of them pass.

### 4. You only validate

The handoff is ready to use: the app is installed and open on the right screen, the test data is loaded, and a few steps tell you what to check. Corrections go back into the build-and-retest loop. Your OK is the second gate. ✋

### 5. Done

The agent commits, pushes and opens a PR. If you ask for it in chat ("push to main", "merge it"), it does exactly that itself. Then it cleans up temporary data, extra simulators and temp files.

## Safety hooks

The skills keep a local state file `.rocket/state.json` with the current stage and status. In the full version on `main`, two hooks read it: a stop guard (no quitting mid-stage or before the interactive test) and a git guard (no push or PR before your ship approval). This directory edition has no hooks, so the stages and gates are followed by the skills' instructions alone.

## Install

### Claude Code

```bash
claude plugin marketplace add Exxzzent/rocket
claude plugin install rocket@rocket
```

### Codex

```bash
codex plugin marketplace add Exxzzent/rocket
codex plugin add rocket@rocket
```

Codex shows the same names (`rocket:launch`, `rocket:fix`, …).

## Set up a project

1. Add a **Workflow** section to your `CLAUDE.md` that says: *Start every new task with the `rocket` skill.*
2. Add a **Rocket profile** for project specifics (language, device pool, build and test commands, test-data policy, commit format). Copy it from [`templates/rocket-profile.md`](templates/rocket-profile.md).
3. Point `AGENTS.md` at `CLAUDE.md`, so every agent reads one source of truth.

Artefacts (plans, test reports, screenshots) go to `docs/rocket/`.

## Develop

The repository ships only the plugin. Tests (`tests/`) and rocket artefacts (`docs/`) are kept locally and ignored by git.

### Release

1. Every user-facing change adds a line under `## [Unreleased]` in [`CHANGELOG.md`](CHANGELOG.md).
2. To release, rename `[Unreleased]` to the new version with today's date and bump `version` in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and `.codex-plugin/plugin.json`. All three must match.
3. After the merge, tag `vX.Y.Z` on `main` and create a GitHub release from the changelog section.

## License

MIT © Exxzzent. Use it however you like, just keep the copyright notice.

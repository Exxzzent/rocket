---
name: fix
description: Use when the rocket router selects fix, or the user reports a bug, crash, regression, failing test or wrong behaviour, often by pointing to an issue.
---

# rocket:fix — bugfix

Five stages. The agent investigates on its own first, comes back with evidence and questions, and fixes only after approval.

**REQUIRED:** Follow `../rocket/conventions.md`.

```
🔎 1 Analysis ──▶ 🧭 2 Findings ──✋──▶ 🛠️ 3 Fix & Verify ──▶ 👀 4 User test ──✋──▶ 🚀 5 Done
                                              ▲                      │ corrections
                                              └── fix + 🔁 retest ───┘
```

## 🔎 Stage 1 — Analysis (autonomous)

State: `stage 1, status working, requires_interactive_test false`.

1. **Baseline** (conventions §7). Read the issue or the user's description completely.
2. **Reproduce it yourself** in the real environment (conventions §8). Use a `rocket:test` subagent or do it directly. Record the device you use in `dev_device` and reuse it for every later test. Capture screenshots, logs and exact steps. If it does not reproduce, record what you tried.
3. **Find the root cause.** Use superpowers:systematic-debugging if available. Trace the cause back to its source, not just the symptom. Rate your certainty (high / medium / low) and say what would raise it.
4. **No code changes** in this stage, except throwaway diagnostics, which you remove again.

## 🧭 Stage 2 — Findings & approval

1. **Write the plan file** (`docs/rocket/plans/YYYY-MM-DD-fix-<slug>.md`): reproduction, evidence, root cause, fix approach, files, and **test cases** with expected results. Always include the failing regression test, the original bug's steps as an interactive case, and neighbouring flows that could break.
2. **Questions** (conventions §4): at most 2 per round, clickable, recommendation first. Update the plan with the answers.
3. **Present**, exactly this shape. The test groups and counts come from the plan's test table:

```
## 🧭 Stage 2 — Findings

**🐞 Cause** (<high|medium|low> certainty)
- <root cause in 1–2 bullets>

**🔬 What I tested**
- <reproduction steps / result, with screenshot path>

**💡 Fix**
- <approach>

**📍 Affected areas**
- <area>: <change>

**🧪 Tests**
- <group> (<n>)
- **Total: <N> tests**

**⚠️ Risks / open**
- <only if any>

📄 Plan: `<plan path>`
✋ Waiting for your approval to fix.
```

State: `status waiting_for_user, gate plan_approval`. **Stop and wait.**

## 🛠️ Stage 3 — Fix & Verify

State: `stage 3, status working, requires_interactive_test true`. Work autonomously until the handoff is ready.

1. **Failing test first:** write a test that reproduces the bug and watch it fail. Then fix the root cause, not the symptom. Watch the test pass.
2. **Verify:** builds for all profile platforms, the full automated suite, code review.
3. **Interactive test loop:** exactly as in `rocket:launch` Stage 2, step 3. One test subagent with `rocket:test` and all plan cases, wait, fix all FAILs, 🔁 targeted retest, repeat until all ✅, set `test_report`.
4. **Handoff:** fresh install, load the data that reproduces the original bug situation, open the app at the place where the bug appeared. Same handoff shape as `rocket:launch`, with the heading `## 👀 Stage 4 — Your test`. The 3–4 steps include "do what used to fail → now <expected>".

State: `status waiting_for_user, gate handoff`.

The same "may NOT end" list and excuses table as `rocket:launch` Stage 2 apply. In short: no handoff without a complete, all-✅ interactive report and the app open for the user.

## 👀 Stage 4 — User test

- **Corrections:** back to Stage 3, fix, 🔁 retest **only** the affected cases, hand off again.
- **Approval** for commit, push and PR: `ship_approved true`, go to Stage 5.

## 🚀 Stage 5 — Done

Identical to `rocket:launch` Stage 4: final check, commit, push and PR as in conventions §5 (link the issue, e.g. "Fixes #N"), 🧹 cleanup, `## 🚀 Done` summary, delete the state file.

## Red flags

| Thought | Reality |
|---|---|
| "I see the bug in the code, no need to reproduce" | Reproduce it. Unreproduced fixes hide wrong root causes. |
| "Fix is obvious, skip Stage 2" | The user approves the fix before you write it. |
| "Test after the fix is the same" | A test that never failed proves nothing. |
| "Fixed the crash by catching the error" | That is a symptom fix. Find why the error happens. |

---
name: launch
description: Use when the rocket router selects launch, or the user asks for a new feature, new screen, new behaviour, or a refactor/cleanup that keeps behaviour unchanged.
---

# rocket:launch — feature & refactor

Four stages. The agent works autonomously from approval to handoff. The user is needed exactly twice: approve the plan, and validate the result.

**REQUIRED:** Follow `../rocket/conventions.md` (profile, docs folder, emojis, questions, approvals, state file, test environment, test data, evidence).

```
🧭 1 Plan ──✋ approval──▶ 🛠️ 2 Build & Verify ──▶ 👀 3 User test ──✋ approval──▶ 🚀 4 Done
                                    ▲                       │ corrections
                                    └──── fix + 🔁 retest ──┘
```

**Violating the letter of a stage is violating its spirit.** Do not merge stages or skip ahead.

## 🧭 Stage 1 — Plan

State: `stage 1, status working`.

1. **Baseline** (conventions §7): status, fetch, worktree from fresh default branch, record the commit IDs.
2. **Analyse** the request and the relevant code on that baseline. Read the project's architecture rules.
3. **Write the plan file** (`docs/rocket/plans/YYYY-MM-DD-<slug>.md`). Use superpowers:writing-plans if available. It contains:
   - Goal, baseline commits, approach, files to touch, step-by-step tasks
   - **Test cases**, written now, before any code, in a table. Each one has an ID (`TC1`…), a group, the user-level steps, the **expected result** and how it is verified (unit, interactive, both). Cover the main flow, edge cases (empty or invalid input, cancel and reopen, repeated actions, fast switching, unusual order) and regressions. For a refactor, the cases state that behaviour stays **unchanged**.
4. **Questions** (conventions §4): at most 2 per round, clickable, recommendation first. Repeat until nothing blocks the plan. Update the plan with the answers.
5. **Present the summary**, exactly this shape, short phrases, not full prose. The test groups and counts are taken from the plan's test table:

```
## 🧭 Stage 1 — Plan

**🎯 Feature** (or **🎯 Refactor**)
- <what is missing / what changes for the user>

**💡 Solution**
- <approach in 1–2 bullets>

**📍 Affected areas**
- <area / file group>: <what changes>

**🧪 Tests**
- <group, e.g. Open, button action, collapse> (<n>)
- **Total: <N> tests**

**⚠️ Risks / open**
- <only if any; omit the heading when empty>

📄 Plan: `<plan path>`
✋ Waiting for your approval.
```

State: `status waiting_for_user, gate plan_approval`. **Stop and wait.** No implementation before the user approves in chat.

## 🛠️ Stage 2 — Build & Verify

State: `stage 2, status working, requires_interactive_test true` (false only if the change has no runtime behaviour the profile can test, which is rare for a feature).

From here, work **autonomously until the handoff is ready**. Do not ask permission for builds, tests, simulators, subagents or edits.

1. **Implement** the approved plan in the worktree. Record the device or simulator you run it on in `dev_device`. Follow the project's architecture, components, style and demo-data rules. Test-first for logic (superpowers:test-driven-development if available).
2. **Verify:** builds for every platform in the profile, the full automated test suite, and a code review (superpowers:requesting-code-review or the harness's code review). Fix what they find.
3. **Interactive test loop** (conventions §8, §11):
   1. **Full test:** dispatch **one** test subagent with `rocket:test`. Give it `dev_device` (the device you developed on) and the device rules, the build, **all test cases from the plan** and the instruction to add its own edge cases. The plan's test cases are the contract. The subagent may add cases but not drop or soften any.
   2. **Wait** until it has finished completely. While it runs: no code changes, no second test subagent.
   3. **Fix all FAILs**, one after another. Re-run builds and automated tests, and add unit tests for each fix.
   4. **🔁 Targeted retest:** a new test subagent tests **only** the fixed cases. It also re-tests a PASS case only if a fix changed the code that case depends on, and says why.
   5. Repeat 2–4 until every case is ✅. Record the report path in `test_report`.
4. **Prepare the handoff.** The user only validates. They do no setup:
   - Fresh install of the final build on `dev_device` (conventions §8). The profile's macOS-only or non-testable targets are listed instead.
   - Load the test data relevant to this change (temporary, or persistent demo data if the profile says so). Record temporary data in `temp_data`.
   - Launch the app and **leave it open on the screen where testing starts**.
5. **Hand off**, exactly this shape:

```
## 👀 Stage 3 — Your test

**📱 Ready on:** <device, OS + build>, build <commit>, opened at <screen>
**🧪 Test data:** <what is loaded and where>

**👉 Steps**
1. <action> → <expected>
2. …   (3–4 steps)

**🖥️ Not tested interactively:** <platforms/aspects, or "nothing">
**📋 Agent test:** <passed>/<total> ✅ — `<report path>`

✋ Waiting for your feedback.
```

State: `status waiting_for_user, gate handoff`.

### You may NOT end Stage 2 while

- any test case is unexecuted or ❌
- no interactive test report exists (the stop hook enforces this)
- the app is not installed and open for the user
- you only built and ran unit tests

| Excuse | Reality |
|---|---|
| "Build passes, the user can test it" | The user validates, they do not test for you. Run the loop. |
| "Simulator is busy" | Use the next free device or create an overflow device (conventions §8). |
| "The tool was refused" | Take another route (CLI screenshots, recordings, UI tests). Only if every route fails: `blocked` with reasons, and report all blockers in one message. |
| "I tested it in my head / from source" | Source review is not an interactive test. |
| "Quick question to the user first" | Only real requirement questions, marked ⚠️ Exception question. Keep working meanwhile. |

## 👀 Stage 3 — User test

The user tests. On feedback:
- **Corrections:** state back to `stage 2, working`. Fix them, run builds and automated tests, then 🔁 retest **only** the affected cases plus new cases for the correction. Hand off again in the same shape.
- **Approval** (for commit, push and PR): set `ship_approved true`, go to Stage 4.

A successful agent test or the Stage-1 approval never replaces this approval.

## 🚀 Stage 4 — Done

State: `stage 4, status working`.

1. **Final check:** builds and the full automated suite on the final state. Interactive test only for cases whose code changed since the last pass. On failure, go back to the loop. New substantive changes go to the user again.
2. **Commit, push, PR:** commit in the profile's format. By default push the **feature branch** and open a PR with test results and evidence links. If the user asked for a direct push to `main` or a merge, do exactly that (conventions §5).
3. **🧹 Cleanup:** remove `temp_data`, delete `created_devices`, shut down used pool devices, quit test apps, remove your temp logs and build output from the project. Keep the reports and screenshots referenced in the PR. Remove the worktree only when everything is pushed and the evidence is safe.
4. **Final summary**, then delete `.rocket/state.json`:

```
## 🚀 Done
**✅ Changed:** <1–2 bullets>
**🔗 PR:** <link>
**🧪 Evidence:** <tests passed, report link>
**🧹 Cleaned up:** <devices, data, worktree>
**⚠️ Open:** <only if any>
```

## Variants

- **Refactor:** test cases capture current behaviour **before** changing code, as characterisation tests. Behaviour must stay identical. No new demo data unless behaviour visibly changes.
- **Autonomous PRs** (conventions §5, `pr_autonomy`): skip Stage 3 per PR. Push branches and open (stacked) PRs freely. Run one combined Stage 3 handoff at the end on the state that contains everything. Merge or push to the default branch only if the user asks for it (conventions §5).

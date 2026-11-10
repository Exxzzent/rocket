---
name: rocket
description: Use at the start of every new task in a project whose instructions say to use rocket, or when the user types /rocket — before any analysis, planning, review, testing or editing — to pick the workflow that fits the request (feature, refactor, bug, review, test, small change, question).
---

# rocket — router

Pick exactly one workflow for the request, announce it, then load and follow that workflow skill. The router does no work of its own.

**REQUIRED:** Read `conventions.md` in this skill's folder once per session. Every workflow uses it.

## Classify

| The user wants… | Workflow | Skill |
| --- | --- | --- |
| New behaviour, a new screen, a feature, or a restructuring with unchanged behaviour (refactor, cleanup) | Launch | `rocket:launch` |
| Something broken fixed: bug report, issue describing wrong behaviour, crash, failing test | Fix | `rocket:fix` |
| An assessment of existing code, a PR, a diff or a design, with no changes | Review | `rocket:review` |
| Something tested or verified, with no code changes | Test | `rocket:test` |
| A tiny, low-risk edit: copy, typo, docs, config value, one-line tweak, rule file | Small | `rocket:small` |
| An answer, an explanation or research, nothing changed | What | `rocket:what` |

Invoke the chosen skill with the harness's skill tool. If it is not listed there, read `../<name>/SKILL.md` next to this file and follow it the same way.

**Tie-breakers:**
- The request is only a pointer to an issue or PR (for example "Issue #106"): read it first, then classify by what it asks for.
- Two independent tasks in one message (for example "add X and fix Y"): ask **one** clickable question (*X first*, *Y first*, *two separate sessions*), then announce the workflow for the first one.
- An opinion on an idea or proposal that does not exist yet: **What**. An assessment of existing code, PRs, diffs or designs: **Review**.
- "Review and fix": use **Review**. Its report ends by offering a fix.
- Unsure between Small and Launch: if behaviour that a user can see changes, or more than a handful of lines across files, use **Launch**.
- Unsure between Fix and Launch: if existing behaviour is wrong, use **Fix**. If wanted behaviour is missing, use **Launch**.
- Still ambiguous: ask **one** clickable question (conventions §4), with your best guess first.

## Announce

This is the first line of your reply, after any greeting the project profile requires. Write it in the profile's output language, otherwise in the user's language:

```
🚀 **rocket → <skill>** (<workflow>)
```

Nothing else on that line: no reason, no explanation, no hint about corrections.

Then invoke the skill and follow it exactly. Do not run another workflow's stages. A Review never produces a Stage-1 plan. A Question never creates a worktree.

## Switching

- The user corrects the choice: switch immediately, announce the new line, keep what was already learned.
- The task changes nature mid-way (a review finds a bug and the user says "fix it"): finish or close the current workflow's report, then announce the new workflow.
- A new, unrelated request arrives: classify it from scratch.

## Red flags

| Thought | Reality |
|---|---|
| "It's obviously a feature, skip the announce line" | The announce line is how the user catches misclassification. Always write it. |
| "A review, but I'll also prepare a plan" | Review means no plan, no gates, no edits. |
| "Too small for rocket" | That is what `rocket:small` and `rocket:what` are for. Route it anyway. |

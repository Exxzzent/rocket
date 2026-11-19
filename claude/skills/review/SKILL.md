---
name: review
description: Use when the rocket router selects review, or the user asks to review, audit, assess or check a PR, branch, diff, files, plan or design without asking for changes.
---

# rocket:review — review only

Two stages. **No code changes, no plan file, no approval gates, no worktree setup, no simulator** unless the review itself is about runtime behaviour.

**REQUIRED:** Follow `../rocket/conventions.md` §1 (profile), §3 (emojis), §4 (questions).

## 🔍 Stage 1 — Review

1. **Scope:** identify exactly what is reviewed: PR number, branch vs base, diff, files or document. Read-only commands are fine. Run `git fetch` first so the comparison uses the fresh `origin/<base>`, not a stale local branch. Record the commit IDs you reviewed. If the scope is unclear, ask **one** clickable question.
2. **Review:** use the harness's review skill if available (for example `code-review`, superpowers:requesting-code-review). Check correctness, edge cases, project rules (architecture, style, commit format) and test coverage.
3. **Verify every finding** before reporting: re-read the code path, construct the concrete failing scenario, and drop what does not hold. Mark each one CONFIRMED or PLAUSIBLE.

State file: not needed. Reviews do not use the stop guard.

## 📋 Stage 2 — Report

```
## 📋 Review — <target>

**Verdict:** <one line>

🔴 **<title>** — `<file>:<line>`
- Scenario: <inputs/state → wrong result>
- Fix idea: <one line>

🟠 **<title>** — …
🟡 **<title>** — …

**✅ Looks good:** <short list, optional>
```

🔴 = bug or data loss, 🟠 = likely problem or rule violation, 🟡 = cleanup or nit. Most severe first.

If there are 🔴 or 🟠 findings, ask **one** clickable question: "Fix these findings?" with options: *Fix all (rocket:fix)*, *Fix selected*, *No*. With no findings, the report ends without a question. On yes, announce and switch to `rocket:fix`. The findings serve as its Stage-1 analysis: it reproduces them, then presents the Stage-2 findings and **still waits for plan approval**. "Fix all" starts the fix workflow. It does not approve a fix plan.

If a different review skill was used for the analysis, keep its findings but present them in this report shape.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just fix this typo while reviewing" | Review changes nothing. Report it. |
| "I'll write a Stage-1 plan first" | Reviews have no plan or approval gates. |
| "This looks wrong, report it" | Verify it first. Unverified findings waste the user's time. |

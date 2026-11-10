---
name: small
description: Use when the rocket router selects small, or the user asks for a tiny low-risk edit such as copy text, a typo, docs, a config value, an instruction or rule file, or a one-line tweak.
---

# rocket:small — small change

Three short stages with two approvals. Use `rocket:launch` instead when behaviour a user can see changes beyond a trivial tweak.

**REQUIRED:** Follow `../rocket/conventions.md` (§1–§7).

## 🧭 Stage 1 — Mini plan

Baseline (conventions §7, a worktree as the project requires). Then:

```
## 🧭 Mini plan
- **🎯** <what changes>
- **📍** <file(s)>
- **🧪** <how it is checked: build / tests / quick interactive check>
✋ OK?
```

At most 1 question, clickable. State: `waiting_for_user, gate plan_approval`. Wait.

## 🛠️ Stage 2 — Change & check

State: `working`. Make the change, run the relevant build and tests. If runtime behaviour changes at all, set `requires_interactive_test true` and run one `rocket:test` subagent on the affected case. Then show:

```
## 🛠️ Done locally
- <diff summary>
- 🧪 <build/tests result>
✋ Commit, push and PR?
```

State: `waiting_for_user, gate ship_approval`.

## 🚀 Stage 3 — PR

On approval: `ship_approved true`, commit in the profile format, push and open a PR as in conventions §5 (or push to `main` / merge if the user asked for it), 🧹 cleanup, then one line: `🚀 Done — <PR link or commit>`. Delete the state file.

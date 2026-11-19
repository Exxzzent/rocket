---
name: test
description: Use when the rocket router selects test, when the user asks to test or verify something without code changes, or when dispatched as the interactive test subagent of rocket:launch or rocket:fix.
---

# rocket:test — interactive test

Operate the real app **like a real user** (tap, click, type, navigate) and prove every result with evidence. Reading source code is not testing. **Never fix anything.** Test to the end, then report.

**REQUIRED:** Follow `../rocket/conventions.md` §1, §2, §8–§11.

Two modes:
- **Subagent mode:** dispatched by `rocket:launch` or `rocket:fix` with a build, a device and test cases. Return the report to the main session. Do **not** clean up devices or data. The main session owns them.
- **Standalone mode:** the user asked for a test. Run both stages, including cleanup.

## 🧪 Stage 1 — Test

1. **Define before executing.** Build a case table first: given cases, plus your own edge cases (empty or invalid input, cancel and reopen, repeated actions, fast switching, unexpected order, rotation or resize, relaunch for persistence). Every case states its **expected result before you run it**. Given cases must not be dropped or reworded into easier ones.
2. **Environment** (conventions §8): use the device from the brief (`dev_device`). Only if it is unavailable, pick a free pool device or create an overflow device, record it, and say why in the report. Uninstall the old app, install the build, verify the binary matches, launch it for real (catches startup crashes that unit tests miss).
3. **Execute** each case like a user. Per case: screenshot of the result, and on FAIL, steps, expected vs actual plus a screenshot. Watch for crashes, lost input, wrong states and noticeable delays. Use logs or video for timing problems.
4. Run **every** case, even after failures, unless a crash makes the rest impossible. Then relaunch and continue.

## 📋 Stage 2 — Report (+ 🧹 cleanup in standalone mode)

Write `docs/rocket/reports/YYYY-MM-DD-<slug>/report.md` and return it. Keep it short (conventions §3a): the table carries the detail, text outside it is one line per point.

```
## 📋 Test report — <feature>
**Environment:** <device>, <OS + build>, build <commit>, binary checksum <ok>
**Result:** <passed>/<total> ✅

| ID | Case | Expected | Result | Evidence |
|---|---|---|---|---|
| TC1 | … | … | ✅ | `TC1-open.webp` |
| TC2 | … | … | ❌ | `TC2-collapse.webp` |

### ❌ TC2 — <title>
- Steps: <one line>
- Expected → actual: <one line>

**Not covered:** <1–2 bullets, or "nothing">
**Interactive vs other evidence:** <one line>
```

Standalone mode then runs 🧹 cleanup: remove temporary data, delete created overflow devices, shut down the pool device, quit the app.

## Red flags

| Thought | Reality |
|---|---|
| "I'll fix this small bug while I'm here" | Never. Report it as ❌. |
| "Case passed in the code" | Only on-screen behaviour counts. |
| "Device is busy, I'll wait" | Create an overflow device. |
| "This case is redundant, skip it" | Every given case is run. |
| "Mostly worked → PASS" | Partial = ❌, with details. |

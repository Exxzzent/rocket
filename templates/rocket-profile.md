# Rocket profile template

Copy this section into your project's `CLAUDE.md` (and point `AGENTS.md` at it). Delete lines you do not need, because rocket falls back to its defaults. Everything here overrides `skills/rocket/conventions.md`.

```markdown
## Workflow

**Start every new task with the `rocket` skill (`/rocket`).** It picks the workflow (launch, fix, review, test, small, what) and its stages.

### Rocket profile

- **Output language:** English
- **Address the user as:** <name or "neutral">
- **Docs folder:** docs/rocket/
- **Test environments:**
  - <platform>: interactive, <device/browser>, <OS/version rule>
  - <platform>: build + automated tests only (user checks it in the user test)
- **Device pool:** "<Device A>", "<Device B>". All busy → create "<Project> Test <next letter>" (same class and OS), delete it after Done.
- **Build:** `<command>`
- **Automated tests:** `<command>` (how to count results)
- **Fresh install check:** <how to verify the installed binary matches the build>
- **Test data:** temporary (default) | persistent demo data for new features via <mechanism>
- **Screenshots:** WebP
- **Commits:** see section "Commit messages"
```

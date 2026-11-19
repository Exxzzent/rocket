# Changelog

All notable changes to rocket are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Codex: the iOS simulator is shown in the Codex in-app browser for the user test, with the native simulator app as fallback. Agent tests run headless (#1).
- Codex: rocket skill instructions take precedence over Codex's default response and execution behaviour (#4).
- PRs for tasks based on a GitHub issue reference it with `Closes #N` or `Fixes #N`, and only when the issue is fully resolved (#3).

### Changed
- Every ambiguity and missing requirement is clarified in the planning stage. The build stage does not start while a question is open (#2).
- Question rounds allow up to 3 questions instead of 2.
- Skills are split into `claude/skills/` and `codex/skills/`, so each agent loads only its own rules.

## [0.1.0] - 2026-11-10

First public release for Claude Code and Codex.

### Added
- Router skill `rocket` that picks one workflow per request and announces it.
- Workflow skills: `launch` (feature, refactor), `fix` (bugfix), `review`, `test`, `small`, `what`.
- Shared conventions: project profile, docs folder, approval gates, state file, test environment and evidence rules.
- Safety hooks: stop guard (no quitting mid-stage or before the interactive test) and git guard (no push or PR before ship approval).
- Plugin and marketplace manifests for Claude Code and Codex, with icon.
- Install notes for Codex, including the one-time hook trust in `/hooks`.
- Rocket profile template for projects.

[Unreleased]: https://github.com/Exxzzent/rocket/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Exxzzent/rocket/releases/tag/v0.1.0

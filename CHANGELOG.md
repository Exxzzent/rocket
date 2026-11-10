# Changelog

All notable changes to rocket are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

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

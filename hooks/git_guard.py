#!/usr/bin/env python3
"""rocket PreToolUse(Bash) hook: keep the ship approval gate.

While a rocket state exists, block `git push` and `gh pr create` unless
ship_approved or pr_autonomy is set. Without a state nothing is blocked.

Where to push and whether to merge is decided by the skills (conventions §5),
not by this hook: when the user asks for it in chat, the agent does it.

Blocking = exit code 2 with the reason on stderr.
"""
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rocket_state import input_cwd, load_state, read_input  # noqa: E402

GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}


def segments(command):
    for part in re.split(r"&&|\|\||;|\||\n", command):
        part = part.strip()
        if not part:
            continue
        try:
            yield shlex.split(part)
        except ValueError:
            yield part.split()


def strip_env(tokens):
    while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
        tokens = tokens[1:]
    while tokens and tokens[0] in {"sudo", "env", "command", "exec"}:
        tokens = tokens[1:]
    return tokens


def git_subcommand(tokens):
    """Return (subcommand, args, git_dir_override) for a git invocation."""
    i, cdir = 1, None
    while i < len(tokens):
        tok = tokens[i]
        if tok in GIT_OPTS_WITH_VALUE:
            if tok == "-C" and i + 1 < len(tokens):
                cdir = tokens[i + 1]
            i += 2
            continue
        if tok.startswith("-"):
            i += 1
            continue
        return tok, tokens[i + 1:], cdir
    return None, [], cdir


def shipping_ok(directory):
    """True when the rocket state governing `directory` allows push and PR."""
    _, state = load_state(directory)
    return state is None or bool(state.get("ship_approved") or state.get("pr_autonomy"))


BLOCK_REASON = (
    "rocket: {action} needs the user's ship approval. If the user already asked for it in chat "
    "(for example \"open a PR\", \"push\", \"push to main\"), set ship_approved true in "
    ".rocket/state.json and run the command again. Never ask the user to do it themselves."
)


def resolve(base, target):
    return os.path.normpath(os.path.join(base, os.path.expanduser(target)))


def check(command, cwd):
    """Judge each segment by the state of the directory it actually runs in.

    `cd`/`pushd` segments move the effective directory and `git -C <dir>` names
    one explicitly, so a push in another repository is judged by that
    repository's state, not by the session's working directory.
    """
    for raw in segments(command):
        tokens = strip_env(raw)
        if not tokens:
            continue
        exe = os.path.basename(tokens[0])

        if exe in {"cd", "pushd"}:
            cwd = resolve(cwd, tokens[1] if len(tokens) > 1 else "~")
            continue

        if exe == "gh" and len(tokens) >= 3 and tokens[1] == "pr" and tokens[2] == "create":
            if not shipping_ok(cwd):
                return BLOCK_REASON.format(action="creating a PR")

        if exe == "git":
            sub, _, cdir = git_subcommand(tokens)
            if sub == "push" and not shipping_ok(resolve(cwd, cdir) if cdir else cwd):
                return BLOCK_REASON.format(action="pushing")
    return None


def main():
    payload = read_input()
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command") or ""
    if not command:
        return 0
    reason = check(command, input_cwd(payload))
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

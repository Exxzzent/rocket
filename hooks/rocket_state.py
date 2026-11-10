"""Shared helpers for rocket hooks: locate and read .rocket/state.json."""
import json
import os

STATE_DIR = ".rocket"
STATE_FILE = "state.json"


def read_input():
    import sys
    raw = sys.stdin.read()
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def find_state_root(start):
    """Walk up from `start` to the first directory containing .rocket/state.json."""
    path = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.isfile(os.path.join(path, STATE_DIR, STATE_FILE)):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def load_state(start):
    """Return (root, state) or (None, None). A corrupt state file yields an empty dict."""
    root = find_state_root(start)
    if root is None:
        return None, None
    try:
        with open(os.path.join(root, STATE_DIR, STATE_FILE), encoding="utf-8") as fh:
            data = json.load(fh)
        return root, data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return root, {}


def input_cwd(payload):
    return payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

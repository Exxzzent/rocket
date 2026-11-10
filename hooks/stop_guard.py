#!/usr/bin/env python3
"""rocket Stop hook: keep the agent working until its stage is really finished.

Blocks ending the turn when .rocket/state.json says
  - status == "working"                      (stage still in progress)
  - gate == "handoff" without a test report  (handoff before interactive test)
  - status == "blocked" without a reason
Without a state file the hook does nothing. After MAX_BLOCKS consecutive
blocks it lets the agent stop, so a broken state can never trap a session.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rocket_state import STATE_DIR, input_cwd, load_state, read_input  # noqa: E402

MAX_BLOCKS = 5
COUNTER = "stop_blocks"


def reason_for(root, state):
    status = state.get("status")
    stage = state.get("stage")
    name = state.get("stage_name") or ""
    skill = state.get("skill") or "workflow"
    where = f"rocket:{skill} Stage {stage}{f' ({name})' if name else ''}"

    if status == "working":
        return (
            f"{where} is still in progress (.rocket/state.json status=working). "
            "Continue the stage until its exit criteria are met. If you are waiting "
            "for the user, set status=waiting_for_user with the right gate first. If "
            "you are truly stuck after trying every route, set status=blocked with a "
            "concrete blocked_reason."
        )
    if status == "waiting_for_user" and state.get("gate") == "handoff" and state.get("requires_interactive_test", True):
        report = state.get("test_report")
        if not report or not os.path.isfile(os.path.join(root, report)):
            return (
                f"{where}: handoff without an interactive test report. Run the "
                "interactive test loop (rocket:test subagent) until all cases pass, "
                "write the report and set test_report to its path before handing off."
            )
    if status == "blocked" and not (state.get("blocked_reason") or "").strip():
        return f"{where}: status=blocked needs a concrete blocked_reason in .rocket/state.json."
    return None


def main():
    payload = read_input()
    root, state = load_state(input_cwd(payload))
    if root is None:
        return 0

    counter_path = os.path.join(root, STATE_DIR, COUNTER)
    reason = reason_for(root, state or {})
    if reason is None:
        if os.path.exists(counter_path):
            os.remove(counter_path)
        return 0

    try:
        count = int(open(counter_path).read().strip() or 0)
    except (OSError, ValueError):
        count = 0
    if count >= MAX_BLOCKS:
        os.remove(counter_path)
        return 0
    with open(counter_path, "w") as fh:
        fh.write(str(count + 1))

    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

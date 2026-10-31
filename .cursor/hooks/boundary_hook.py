import json
import subprocess
import sys

payload = json.load(sys.stdin)
file_path = payload.get("file_path") or payload.get("path", "")

# Only run boundary checks on Python files
if file_path.endswith(".py"):
    res = subprocess.run(
        [sys.executable, "acme_platform/ci_guardrails/check_boundaries.py", file_path],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print(json.dumps({
            "decision": "block",
            "agent_message": f"Acme Boundary Violation:\n{res.stdout.strip()}"
        }))
        sys.exit(2)

print(json.dumps({"decision": "allow"}))
sys.exit(0)

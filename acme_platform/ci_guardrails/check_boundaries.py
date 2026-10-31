"""
Acme Platform Local CI Guardrail Runner (Mocked CI Step)
Scans target Python files for architectural boundary violations,
banned imports, and missing conventions before PR approval.
"""
import ast
import sys
from pathlib import Path

BANNED_MODULES = {
    "acme_platform.legacy_deprecated",
    "requests",
    "httpx",
    "urllib",
    "dotenv",
}

def check_file(filepath: str) -> list[str]:
    path = Path(filepath)
    if not path.exists():
        return [f"File not found: {filepath}"]

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=filepath)
    violations = []

    # 1. Check imports against Acme boundaries
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for banned in BANNED_MODULES:
                    if alias.name == banned or alias.name.startswith(f"{banned}."):
                        violations.append(f"Line {node.lineno}: Banned import '{alias.name}'")
        elif isinstance(node, ast.ImportFrom) and node.module:
            for banned in BANNED_MODULES:
                if node.module == banned or node.module.startswith(f"{banned}."):
                    violations.append(f"Line {node.lineno}: Banned import from '{node.module}'")

    # 2. Check public functions for NumPy docstrings & float support conventions
    for node in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        if not node.name.startswith("_"):
            doc = ast.get_docstring(node) or ""
            if "Parameters" not in doc or "Returns" not in doc:
                violations.append(
                    f"Function '{node.name}' (Line {node.lineno}): Missing standard NumPy docstring ('Parameters'/'Returns' sections)."
                )

    return violations

if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        print("Usage: python acme_platform/ci_guardrails/check_boundaries.py <file1.py> ...")
        sys.exit(1)

    all_passed = True
    for target in targets:
        issues = check_file(target)
        if issues:
            all_passed = False
            print(f"❌ [ACME CI] Boundary violations in {target}:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ [ACME CI] {target} passed all boundary and convention checks.")

    sys.exit(0 if all_passed else 1)

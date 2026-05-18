#!/usr/bin/env python3
"""
generate_policy_matrix.py
Generate a policy-to-agent assignment matrix and CI test mapping.

Usage:
    uv run python scripts/generate_policy_matrix.py \
        --policies policies/ \
        --tests tests/ \
        --output matrix.md

Outputs a Markdown table showing:
- Which policies apply to which OpenClaw agents (Arty, Brodie, Emily, Jack, Professor)
- Which test files should run in CI
- Whether a rule belongs in the agent prompt vs runtime enforcement
- Whether it needs WAL/evidence logging
- Feature-flag gating requirements
"""
import argparse
import re
import sys
from pathlib import Path


AGENTS = ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"]
POLICY_DIR = Path(__file__).resolve().parent.parent / "policies"
TESTS_DIR = Path(__file__).resolve().parent.parent / "tests"
OUTPUT_DEFAULT = Path(__file__).resolve().parent.parent / "matrix.md"

# Policy → agent applicability (heuristic based on policy name)
POLICY_AGENT_MAP: dict[str, list[str]] = {
    "agent_loop_policy.md":      ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"],
    "coding_agent_policy.md":    ["Arty", "Brodie", "Jack Mercer"],
    "database_safety_policy.md": ["Arty", "Brodie", "Emily"],
    "destructive_action_policy.md": ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"],
    "edit_policy.md":            ["Arty", "Brodie", "Jack Mercer"],
    "evidence_logging_policy.md": ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"],
    "frontend_generation_policy.md": ["Arty", "Brodie", "Jack Mercer"],
    "progress_reporting_policy.md": ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"],
    "rollback_policy.md":        ["Arty", "Brodie", "Jack Mercer", "Professor Emily"],
    "secret_handling_policy.md": ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"],
    "tool_use_policy.md":        ["Arty", "Brodie", "Emily", "Jack Mercer", "Professor Emily"],
    "verification_policy.md":    ["Arty", "Brodie", "Jack Mercer"],
}

# Policy → where the rule lives (prompt vs runtime vs WAL)
POLICY_RULE_LOC: dict[str, dict[str, str]] = {
    "agent_loop_policy.md": {"prompt": "One tool per turn, terminal states", "runtime": "Retry limits, state transitions", "wal": "Loop iteration logs"},
    "coding_agent_policy.md": {"prompt": "Read before edit, minimal changes", "runtime": "Batching enforcement", "wal": "Edit audit trail"},
    "database_safety_policy.md": {"prompt": "Read-only by default, use ORM", "runtime": "Query gating, approval flows", "wal": "Query intent + result logs"},
    "destructive_action_policy.md": {"prompt": "Describe consequences", "runtime": "Approval gate, dry-run", "wal": "Intent + approval + result"},
    "edit_policy.md": {"prompt": "Exact match, atomicity", "runtime": "Edit validation", "wal": "Pre/post file hashes"},
    "evidence_logging_policy.md": {"prompt": "Log significant actions", "runtime": "Structured log emission", "wal": "WAL entries, audit trail"},
    "frontend_generation_policy.md": {"prompt": "Framework defaults, component rules", "runtime": "Build lint, preview gate", "wal": "Deploy logs"},
    "progress_reporting_policy.md": {"prompt": "Concise updates, evidence attachments", "runtime": "Notification routing", "wal": "Status change logs"},
    "rollback_policy.md": {"prompt": "Undo capability, git best practices", "runtime": "Revert tool execution", "wal": "Rollback records"},
    "secret_handling_policy.md": {"prompt": "Never hardcode, redact logs", "runtime": "Secret scanner, redaction filter", "wal": "Access logs (without values)"},
    "tool_use_policy.md": {"prompt": "Schema verification, one tool per turn", "runtime": "Tool call validation", "wal": "Tool invocation logs"},
    "verification_policy.md": {"prompt": "Run tests, fix lint errors", "runtime": "CI gate, test runner", "wal": "Test result logs"},
}

# Feature flags for high-risk policies
FEATURE_FLAGS: dict[str, str] = {
    "database_safety_policy.md": "ENABLE_DB_WRITE_APPROVAL",
    "destructive_action_policy.md": "ENABLE_DESTRUCTIVE_ACTIONS",
    "secret_handling_policy.md": "ENABLE_SECRET_INJECTION",
    "frontend_generation_policy.md": "ENABLE_AUTO_DEPLOY",
}


def find_test_for_policy(policy_file: str, tests_dir: Path) -> str:
    stem = policy_file.replace("_policy.md", "")
    candidates = [
        tests_dir / f"{stem}_cases.yaml",
        tests_dir / f"{stem}_cases.yml",
    ]
    for c in candidates:
        if c.exists():
            return str(c.name)
    return "—"


def generate_matrix(policies_dir: Path, tests_dir: Path) -> str:
    lines: list[str] = []
    lines.append("# OpenClaw Policy-to-Agent Assignment Matrix")
    lines.append("")
    lines.append("| Policy | Tests | Agents | Prompt Rules | Runtime Rules | WAL Rules | Feature Flag |")
    lines.append("|--------|-------|--------|--------------|---------------|-----------|--------------|")

    for policy_file in sorted(policies_dir.glob("*.md")):
        name = policy_file.name
        agents = ", ".join(POLICY_AGENT_MAP.get(name, ["TBD"]))
        test_file = find_test_for_policy(name, tests_dir)
        loc = POLICY_RULE_LOC.get(name, {})
        prompt = loc.get("prompt", "—")
        runtime = loc.get("runtime", "—")
        wal = loc.get("wal", "—")
        flag = FEATURE_FLAGS.get(name, "—")
        lines.append(f"| {name} | {test_file} | {agents} | {prompt} | {runtime} | {wal} | {flag} |")

    lines.append("")
    lines.append("## CI Test Mapping")
    lines.append("")
    lines.append("All `*_cases.yaml` files in `tests/` should run in CI.")
    lines.append("")
    lines.append("| Test File | Policy Covered | Priority |")
    lines.append("|-----------|----------------|----------|")

    for test_file in sorted(tests_dir.glob("*_cases.yaml")):
        stem = test_file.name.replace("_cases.yaml", "")
        policy_match = stem + "_policy.md"
        priority = "Critical" if "secret" in stem or "destructive" in stem or "database" in stem else "Standard"
        lines.append(f"| {test_file.name} | {policy_match} | {priority} |")

    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("- **Prompt Rules**: Injected into the agent's system prompt at runtime.")
    lines.append("- **Runtime Rules**: Enforced by the OpenClaw executor / gatekeeper layer.")
    lines.append("- **WAL Rules**: Logged to the Write-Ahead Log for audit and replay.")
    lines.append("- **Feature Flag**: Must be enabled explicitly; disables the policy's risky paths by default.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate policy-to-agent matrix")
    parser.add_argument("--policies", type=Path, default=POLICY_DIR, help="Policies directory")
    parser.add_argument("--tests", type=Path, default=TESTS_DIR, help="Tests directory")
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT, help="Output markdown file")
    args = parser.parse_args()

    if not args.policies.exists():
        print(f"ERROR: policies directory not found: {args.policies}", file=sys.stderr)
        return 1
    if not args.tests.exists():
        print(f"ERROR: tests directory not found: {args.tests}", file=sys.stderr)
        return 1

    matrix_md = generate_matrix(args.policies, args.tests)
    args.output.write_text(matrix_md, encoding="utf-8")
    print(f"Matrix written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

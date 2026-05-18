#!/usr/bin/env python3
"""
build_pattern_index.py
Build a searchable index of behavioral patterns extracted from the 7 vendor sources.

Usage:
    uv run python scripts/build_pattern_index.py [--source-dir policies/] [--output index.json]

The index maps each policy file to its extracted rules, risk levels, and
source provenance, enabling downstream search and deduplication.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


POLICY_DIR = Path(__file__).resolve().parent.parent / "policies"
OUTPUT_DEFAULT = Path(__file__).resolve().parent.parent / "index.json"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def parse_policy_markdown(path: Path) -> dict[str, Any]:
    """Parse a policy markdown file into structured fields."""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    record: dict[str, Any] = {
        "file": str(path.name),
        "title": None,
        "purpose": None,
        "rules": [],
        "risks": [],
        "references": [],
    }

    in_purpose = False
    in_rule = False
    current_rule: dict[str, Any] | None = None
    current_block: list[str] = []

    def flush_block():
        nonlocal current_block
        if current_block:
            text = "\n".join(current_block).strip()
            current_block = []
            return text
        return ""

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            record["title"] = line[2:].strip()
            continue
        if line.lower().startswith("## purpose"):
            in_purpose = True
            in_rule = False
            continue
        if line.lower().startswith("## policy"):
            in_purpose = False
            in_rule = False
            continue
        if line.lower().startswith("## risk assessment"):
            in_purpose = False
            in_rule = False
            # Flush any pending rule
            if current_rule:
                current_rule["description"] = flush_block()
                record["rules"].append(current_rule)
                current_rule = None
            continue
        if line.lower().startswith("## references"):
            in_purpose = False
            in_rule = False
            if current_rule:
                current_rule["description"] = flush_block()
                record["rules"].append(current_rule)
                current_rule = None
            continue

        # Rule headers inside Policy section: "### 1. Title"
        m = re.match(r"^###\s+\d+\.\s+(.*)", line)
        if m and not in_purpose:
            if current_rule:
                current_rule["description"] = flush_block()
                record["rules"].append(current_rule)
            current_rule = {"id": f"{slugify(path.stem)}_{len(record['rules']) + 1:03d}", "title": m.group(1).strip()}
            in_rule = True
            continue

        # Risk bullets
        if line.strip().startswith("- **") and "risk" in line.lower():
            risk_match = re.search(r"\*\*(.*?)\*\*:\s*(.*)", line)
            if risk_match:
                record["risks"].append({
                    "level": risk_match.group(1).strip(),
                    "description": risk_match.group(2).strip(),
                })
            continue

        # Reference bullets
        if line.strip().startswith("- ") and ("openclaw" in line.lower() or "guideline" in line.lower()):
            record["references"].append(line.strip()[2:])
            continue

        # Accumulate block text
        if in_purpose:
            if line.strip():
                current_block.append(line)
            else:
                record["purpose"] = flush_block()
        elif in_rule and current_rule is not None:
            current_block.append(line)

    # Final flushes
    if in_purpose:
        record["purpose"] = flush_block()
    if current_rule:
        current_rule["description"] = flush_block()
        record["rules"].append(current_rule)

    return record


def build_index(source_dir: Path) -> dict[str, Any]:
    index: dict[str, Any] = {"policies": [], "by_risk": {}, "by_source": {}}
    for md in sorted(source_dir.glob("*.md")):
        rec = parse_policy_markdown(md)
        index["policies"].append(rec)
        # bucket by risk level
        for risk in rec.get("risks", []):
            level = risk.get("level", "Unknown")
            index["by_risk"].setdefault(level, []).append({
                "policy": rec["file"],
                "rule_title": rec["title"],
                "description": risk["description"],
            })
        # bucket by source keyword in references
        for ref in rec.get("references", []):
            src = "OpenClaw" if "openclaw" in ref.lower() else "Industry"
            index["by_source"].setdefault(src, []).append({
                "policy": rec["file"],
                "reference": ref,
            })
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build policy pattern index")
    parser.add_argument("--source-dir", type=Path, default=POLICY_DIR, help="Directory containing policy .md files")
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT, help="Output JSON path")
    args = parser.parse_args()

    if not args.source_dir.exists():
        print(f"ERROR: source directory not found: {args.source_dir}", file=sys.stderr)
        return 1

    index = build_index(args.source_dir)
    args.output.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Indexed {len(index['policies'])} policies → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Extract Tool Schemas from Vendor System Prompts

Reads tool schema files from the source repo and catalogs them
for security analysis and capability enumeration.

Usage:
    python extract_tool_schemas.py /path/to/source/repo

Output:
    Creates tool_schema_catalog.json
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


def parse_json_tools(file_path):
    """Parse JSON tool schema files."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading {file_path}: {e}")
        return []

    tools = []

    # Handle different JSON structures
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                tools.append(extract_tool_info(item))
    elif isinstance(data, dict):
        if "tools" in data:
            for tool in data["tools"]:
                tools.append(extract_tool_info(tool))
        elif "functions" in data:
            for func in data["functions"]:
                tools.append(extract_tool_info(func))
        else:
            # Single tool object
            tools.append(extract_tool_info(data))

    return tools


def extract_tool_info(tool_obj):
    """Extract standardized tool information."""
    name = tool_obj.get("name", tool_obj.get("function", "unknown"))
    description = tool_obj.get("description", "No description")
    parameters = tool_obj.get("parameters", tool_obj.get("input", {}))

    # Determine risk level based on tool name/function
    risk = classify_risk(name, description)

    return {
        "name": name,
        "description": description,
        "parameters": parameters,
        "risk_level": risk["level"],
        "risk_category": risk["category"],
        "risk_reason": risk["reason"]
    }


def classify_risk(name, description):
    """Classify tool risk level."""
    name_lower = name.lower()
    desc_lower = description.lower() if description else ""
    combined = f"{name_lower} {desc_lower}"

    high_risk_keywords = [
        "shell", "exec", "execute", "run_command", "system",
        "delete", "remove", "rm", "drop", "truncate",
        "deploy", "production", "push", "publish",
        "sudo", "root", "admin", "superuser",
        "browser_console", "eval", "javascript"
    ]

    medium_risk_keywords = [
        "write", "edit", "modify", "update", "create",
        "file", "filesystem", "path", "directory",
        "database", "sql", "query", "migration",
        "git", "commit", "merge", "rebase",
        "api", "http", "request", "curl"
    ]

    for keyword in high_risk_keywords:
        if keyword in combined:
            return {
                "level": "high",
                "category": "destructive_or_privileged",
                "reason": f"Contains high-risk keyword: {keyword}"
            }

    for keyword in medium_risk_keywords:
        if keyword in combined:
            return {
                "level": "medium",
                "category": "state_changing",
                "reason": f"Contains medium-risk keyword: {keyword}"
            }

    return {
        "level": "low",
        "category": "read_only",
        "reason": "No risky keywords detected"
    }


def parse_text_tools(file_path):
    """Parse tool definitions from text files."""
    tools = []

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"Error reading {file_path}: {e}")
        return tools

    # Look for tool definitions in various formats
    # Simple heuristic: look for tool/function names in code blocks
    import re

    # Match patterns like function declarations, tool descriptions, etc.
    patterns = [
        r'function\s+(\w+)\s*\(',
        r'tool\s*:\s*(\w+)',
        r'##?\s+(\w+).*tool',
        r'"name"\s*:\s*"(\w+)"',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if len(match) > 2:  # Filter out short/invalid names
                risk = classify_risk(match, "")
                tools.append({
                    "name": match,
                    "description": "Extracted from text file",
                    "parameters": {},
                    "risk_level": risk["level"],
                    "risk_category": risk["category"],
                    "risk_reason": risk["reason"]
                })

    return tools


def build_catalog(source_repo):
    """Build the complete tool schema catalog."""
    source_path = Path(source_repo)

    if not source_path.exists():
        print(f"Error: Source repo not found: {source_repo}")
        sys.exit(1)

    catalog = {
        "metadata": {
            "source_repo": str(source_path),
            "extracted_at": str(Path(__file__).stat().st_mtime),
            "total_tools": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0
        },
        "tools": [],
        "by_vendor": defaultdict(list),
        "by_category": defaultdict(list)
    }

    # Find all tool/schema files
    tool_files = []
    for ext in ["*.json", "*.txt"]:
        tool_files.extend(source_path.rglob(ext))

    for file_path in tool_files:
        if "tools" in file_path.name.lower() or "schema" in file_path.name.lower():
            print(f"Processing: {file_path.relative_to(source_path)}")

            if file_path.suffix == ".json":
                tools = parse_json_tools(file_path)
            else:
                tools = parse_text_tools(file_path)

            for tool in tools:
                tool["source_file"] = str(file_path.relative_to(source_path))
                catalog["tools"].append(tool)

                # Determine vendor from path
                vendor = "unknown"
                parts = file_path.relative_to(source_path).parts
                if parts:
                    vendor = parts[0].split()[0].lower()

                catalog["by_vendor"][vendor].append(tool["name"])
                catalog["by_category"][tool["risk_category"]].append(tool["name"])

                # Update counts
                catalog["metadata"]["total_tools"] += 1
                if tool["risk_level"] == "high":
                    catalog["metadata"]["high_risk"] += 1
                elif tool["risk_level"] == "medium":
                    catalog["metadata"]["medium_risk"] += 1
                else:
                    catalog["metadata"]["low_risk"] += 1

    # Convert defaultdicts to regular dicts for JSON serialization
    catalog["by_vendor"] = dict(catalog["by_vendor"])
    catalog["by_category"] = dict(catalog["by_category"])

    # Write catalog
    output_file = Path(__file__).parent.parent / "tool_schema_catalog.json"
    with open(output_file, "w") as f:
        json.dump(catalog, f, indent=2)

    print(f"\nTool schema catalog built: {output_file}")
    print(f"  Total tools: {catalog['metadata']['total_tools']}")
    print(f"  High risk: {catalog['metadata']['high_risk']}")
    print(f"  Medium risk: {catalog['metadata']['medium_risk']}")
    print(f"  Low risk: {catalog['metadata']['low_risk']}")
    print(f"  Vendors: {list(catalog['by_vendor'].keys())}")

    return catalog


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_tool_schemas.py /path/to/source/repo")
        sys.exit(1)

    build_catalog(sys.argv[1])

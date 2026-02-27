#!/usr/bin/env python3
"""
Skill Validation Script for Fitness Tools Plugin

Validates skill structure, YAML frontmatter, and count consistency.

Usage:
    python scripts/validate-skills.py              # Run all checks
    python scripts/validate-skills.py --skill body-composition  # Single skill
    python scripts/validate-skills.py --format json  # JSON for CI

Exit codes:
    0 = Success (warnings allowed)
    1 = Errors found
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

try:
    import yaml

    HAS_PYYAML = True
except ImportError:
    HAS_PYYAML = False


def simple_yaml_parse(yaml_str: str) -> dict:
    """Simple YAML frontmatter parser when PyYAML is not available."""
    result: dict = {}
    current_key = None
    current_collection: dict | list | None = None
    collection_type = None

    def _save_current():
        nonlocal current_key, current_collection, collection_type
        if current_key and current_collection is not None:
            result[current_key] = current_collection
        current_key = None
        current_collection = None
        collection_type = None

    for line in yaml_str.strip().split("\n"):
        if not line.strip():
            continue

        if line.startswith("  - ") or line.startswith("    - "):
            if current_key is not None:
                if collection_type is None:
                    current_collection = []
                    collection_type = "list"
                if collection_type == "list":
                    assert isinstance(current_collection, list)
                    item = line.strip().lstrip("- ").strip()
                    current_collection.append(item)
            continue

        if line.startswith("  ") and ":" in line and not line.startswith("  - "):
            if current_key is not None:
                if collection_type is None:
                    current_collection = {}
                    collection_type = "dict"
                if collection_type == "dict":
                    assert isinstance(current_collection, dict)
                    nested_parts = line.strip().split(":", 1)
                    nested_key = nested_parts[0].strip()
                    nested_value = nested_parts[1].strip() if len(nested_parts) > 1 else ""
                    if nested_value.startswith('"') and nested_value.endswith('"'):
                        nested_value = nested_value[1:-1]
                    current_collection[nested_key] = nested_value
            continue

        if ":" in line and not line.startswith(" "):
            _save_current()
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            if value:
                result[key] = value
            else:
                current_key = key
                current_collection = None
                collection_type = None

    _save_current()
    return result


def parse_yaml_frontmatter(content: str) -> tuple[dict, str]:
    """Extract and parse YAML frontmatter from markdown content."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    yaml_str = match.group(1)
    body = match.group(2)

    if HAS_PYYAML:
        data = yaml.safe_load(yaml_str)
    else:
        data = simple_yaml_parse(yaml_str)

    return data or {}, body


class Severity(IntEnum):
    WARNING = 1
    ERROR = 2


@dataclass
class Issue:
    severity: Severity
    skill: str
    check: str
    message: str

    def __str__(self) -> str:
        prefix = "ERROR" if self.severity == Severity.ERROR else "WARN"
        return f"  [{prefix}] {self.skill}: {self.check} - {self.message}"


REQUIRED_FRONTMATTER_FIELDS = ["name", "description", "license"]
REQUIRED_METADATA_FIELDS = ["author", "version", "domain", "triggers", "role", "scope", "output-format"]


def validate_skill(skill_dir: Path) -> list[Issue]:
    """Validate a single skill directory."""
    issues: list[Issue] = []
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.exists():
        issues.append(Issue(Severity.ERROR, skill_name, "structure", "Missing SKILL.md"))
        return issues

    content = skill_file.read_text(encoding="utf-8")
    data, body = parse_yaml_frontmatter(content)

    if not data:
        issues.append(Issue(Severity.ERROR, skill_name, "frontmatter", "No YAML frontmatter found"))
        return issues

    # Check required top-level fields
    for f in REQUIRED_FRONTMATTER_FIELDS:
        if f not in data:
            issues.append(Issue(Severity.ERROR, skill_name, "frontmatter", f"Missing required field: {f}"))

    # Check name matches directory
    if data.get("name") and data["name"] != skill_name:
        issues.append(
            Issue(Severity.ERROR, skill_name, "frontmatter", f"name '{data['name']}' != directory '{skill_name}'")
        )

    # Check metadata block
    metadata = data.get("metadata", {})
    if not metadata:
        issues.append(Issue(Severity.ERROR, skill_name, "frontmatter", "Missing metadata block"))
    else:
        for f in REQUIRED_METADATA_FIELDS:
            if f not in metadata:
                issues.append(Issue(Severity.WARNING, skill_name, "metadata", f"Missing metadata field: {f}"))

    # Check references exist
    refs_dir = skill_dir / "references"
    if refs_dir.exists():
        ref_files = list(refs_dir.glob("*.md"))
        if not ref_files:
            issues.append(Issue(Severity.WARNING, skill_name, "references", "references/ exists but is empty"))
    else:
        issues.append(Issue(Severity.WARNING, skill_name, "references", "No references/ directory"))

    # Check body has required sections
    required_sections = ["Role Definition", "When to Use This Skill", "Core Workflow", "Constraints"]
    for section in required_sections:
        if f"## {section}" not in body:
            issues.append(Issue(Severity.WARNING, skill_name, "body", f"Missing section: ## {section}"))

    return issues


def validate_version_json(skills_dir: Path) -> list[Issue]:
    """Validate version.json counts match actual files."""
    issues: list[Issue] = []
    version_file = skills_dir.parent / "version.json"

    if not version_file.exists():
        issues.append(Issue(Severity.ERROR, "version.json", "structure", "Missing version.json"))
        return issues

    data = json.loads(version_file.read_text(encoding="utf-8"))

    actual_skills = len(
        [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    )
    if data.get("skillCount") != actual_skills:
        issues.append(
            Issue(
                Severity.ERROR,
                "version.json",
                "count",
                f"skillCount={data.get('skillCount')} but found {actual_skills} skills",
            )
        )

    actual_refs = sum(
        len(list((d / "references").glob("*.md")))
        for d in skills_dir.iterdir()
        if d.is_dir() and (d / "references").exists()
    )
    if data.get("referenceFileCount") != actual_refs:
        issues.append(
            Issue(
                Severity.ERROR,
                "version.json",
                "count",
                f"referenceFileCount={data.get('referenceFileCount')} but found {actual_refs} references",
            )
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Fitness Tools skill files")
    parser.add_argument("--skill", type=str, help="Validate a single skill by name")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--path", type=Path, default=Path("skills"), help="Skills directory")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Skills directory not found: {args.path}", file=sys.stderr)
        return 1

    all_issues: list[Issue] = []

    if args.skill:
        skill_dir = args.path / args.skill
        if not skill_dir.exists():
            print(f"Error: Skill not found: {args.skill}", file=sys.stderr)
            return 1
        all_issues.extend(validate_skill(skill_dir))
    else:
        for skill_dir in sorted(args.path.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                all_issues.extend(validate_skill(skill_dir))
        all_issues.extend(validate_version_json(args.path))

    errors = [i for i in all_issues if i.severity == Severity.ERROR]
    warnings = [i for i in all_issues if i.severity == Severity.WARNING]

    if args.format == "json":
        output = [
            {"severity": "error" if i.severity == Severity.ERROR else "warning", "skill": i.skill, "check": i.check, "message": i.message}
            for i in all_issues
        ]
        print(json.dumps(output, indent=2))
    else:
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for issue in errors:
                print(str(issue))
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for issue in warnings:
                print(str(issue))
        if not all_issues:
            print("All skill validations passed.")
        else:
            print(f"\nTotal: {len(errors)} errors, {len(warnings)} warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

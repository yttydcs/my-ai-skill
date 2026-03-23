#!/usr/bin/env python3
"""Create the recommended docs tree for a target project."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT_README = """# Documentation

## Reading Order
- Start with requirements for long-lived needs and acceptance criteria.
- Read specs for technical contracts and architecture constraints.
- Read plan for workflow execution history.
- Read change for completed results and verification.
- Read lessons for recurring issues and prevention guidance.

## Troubleshooting Order
- Start with lessons when the request is about a symptom, outage, or repeated confusion.
- Read change only when the lesson doc is missing or insufficient.
- Confirm stable truth in specs and requirements before changing behavior.

## Sections
- [requirements/README.md](requirements/README.md)
- [specs/README.md](specs/README.md)
- [plan/README.md](plan/README.md)
- [change/README.md](change/README.md)
- [lessons/README.md](lessons/README.md)
"""


REQUIREMENTS_README = """# Requirements

Store long-lived user, product, or module requirements here.

## Rules
- Use stable names without dates.
- Group by module or domain when useful.
- Keep acceptance criteria here, not only in change logs.
"""


SPECS_README = """# Specs

Store technical contracts, architecture constraints, protocol rules, and generated-doc guardrails here.

## Rules
- Use stable names without dates.
- Group by module or domain when useful.
- Update specs when behavior-changing work alters technical contracts.
"""


PLAN_README = """# Plan Archive

Store workflow planning documents here.

## Rules
- Prefer `YYYY-MM-DD_topic.md`.
- Record related requirements and specs.
- Record requirement/spec impact before implementation.
"""


CHANGE_README = """# Change Archive

Store completed workflow result documents here.

## Rules
- Prefer `YYYY-MM-DD_topic.md`.
- Record related requirements and specs.
- Record whether requirements or specs changed.
- Promote reusable troubleshooting knowledge into `lessons` instead of leaving it only here.
"""


LESSONS_README = """# Lessons

Store reusable lessons, root-cause analyses, and prevention guidance here.

## Rules
- Use stable names without dates when the lesson is long-lived.
- Group by module or domain when useful.
- Capture lookup hints such as symptoms, trigger conditions, keywords, and quick checks.
- Link lessons back to relevant requirements, specs, and changes.
"""


MODULE_REQUIREMENTS = """# {module} Requirements

Store long-lived requirements for `{module}` here.
"""


MODULE_SPECS = """# {module} Specs

Store technical contracts and constraints for `{module}` here.
"""


MODULE_LESSONS = """# {module} Lessons

Store recurring problems, query-friendly troubleshooting notes, and prevention guidance for `{module}` here.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a governed docs tree.")
    parser.add_argument("project_root", help="Project root where docs/ should be created")
    parser.add_argument(
        "--module",
        action="append",
        default=[],
        help="Optional module bucket name. Repeatable.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Show planned actions only")
    return parser.parse_args()


def ensure_directory(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"[mkdir] {path}")
        return
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, force: bool, dry_run: bool) -> str:
    if path.exists() and not force:
        return f"[skip] {path}"
    if dry_run:
        return f"[write] {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return f"[write] {path}"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    docs_root = project_root / "docs"

    base_dirs = [
        docs_root,
        docs_root / "requirements",
        docs_root / "specs",
        docs_root / "plan",
        docs_root / "change",
        docs_root / "lessons",
    ]

    for directory in base_dirs:
        ensure_directory(directory, args.dry_run)

    actions = [
        write_file(docs_root / "README.md", ROOT_README, args.force, args.dry_run),
        write_file(docs_root / "requirements" / "README.md", REQUIREMENTS_README, args.force, args.dry_run),
        write_file(docs_root / "specs" / "README.md", SPECS_README, args.force, args.dry_run),
        write_file(docs_root / "plan" / "README.md", PLAN_README, args.force, args.dry_run),
        write_file(docs_root / "change" / "README.md", CHANGE_README, args.force, args.dry_run),
        write_file(docs_root / "lessons" / "README.md", LESSONS_README, args.force, args.dry_run),
    ]

    for raw_module in args.module:
        module = raw_module.strip()
        if not module:
            continue
        module_dirs = [
            docs_root / "requirements" / module,
            docs_root / "specs" / module,
            docs_root / "lessons" / module,
        ]
        for directory in module_dirs:
            ensure_directory(directory, args.dry_run)
        actions.extend(
            [
                write_file(
                    docs_root / "requirements" / module / "README.md",
                    MODULE_REQUIREMENTS.format(module=module),
                    args.force,
                    args.dry_run,
                ),
                write_file(
                    docs_root / "specs" / module / "README.md",
                    MODULE_SPECS.format(module=module),
                    args.force,
                    args.dry_run,
                ),
                write_file(
                    docs_root / "lessons" / module / "README.md",
                    MODULE_LESSONS.format(module=module),
                    args.force,
                    args.dry_run,
                ),
            ]
        )

    for action in actions:
        print(action)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

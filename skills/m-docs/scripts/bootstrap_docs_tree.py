#!/usr/bin/env python3
"""Create the recommended governed docs tree for a target project."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT_README = """# Documentation

## Reading Order
- Start with intake when original request evidence matters.
- Read features for current user-visible behavior.
- Read requirements for durable capability intent and acceptance.
- Read specs for technical contracts and architecture constraints.
- Read decisions for architecturally significant choices.
- Read plan for workflow execution history.
- Read change for completed results and verification.
- Read lessons for recurring issues and prevention guidance.

## Troubleshooting Order
- Start with lessons when the request is about a symptom, outage, or repeated confusion.
- Read change only when the lesson doc is missing or insufficient.
- Confirm stable truth in features, specs, and requirements before changing behavior.

## Private Docs Boundary
- This docs tree may be private and separate from code repositories.
- Remote configuration, push targets, publication, and backup strategy are user-owned decisions.

## Sections
- [intake/README.md](intake/README.md)
- [features/README.md](features/README.md)
- [requirements/README.md](requirements/README.md)
- [specs/README.md](specs/README.md)
- [decisions/README.md](decisions/README.md)
- [plan/README.md](plan/README.md)
- [change/README.md](change/README.md)
- [lessons/README.md](lessons/README.md)
"""


INTAKE_README = """# Intake

Store original request evidence here.

## Rules
- Prefer `YYYY-MM-DD_topic.md` for dated requests.
- Preserve the source and open questions.
- Link to routed feature, requirement, spec, decision, plan, and change docs.
"""


FEATURES_README = """# Features

Store current user-visible feature truth here.

## Rules
- Use stable names without dates.
- Keep CRUD workflows, UI placement, permissions, states, and acceptance scenarios here.
- Link technical contracts to specs instead of duplicating them.
"""


REQUIREMENTS_README = """# Requirements

Store durable user, product, or module requirements here.

## Rules
- Use stable names without dates.
- Group by module or domain when useful.
- Keep capability intent and broad acceptance criteria here, not only in change logs.
"""


SPECS_README = """# Specs

Store technical contracts, architecture constraints, protocol rules, and generated-doc guardrails here.

## Rules
- Use stable names without dates.
- Group by module or domain when useful.
- Update specs when behavior-changing work alters technical contracts.
"""


DECISIONS_README = """# Decisions

Store append-only architecture decision records here.

## Rules
- Prefer `YYYY-MM-DD_topic.md`.
- Record context, options, decision, consequences, and supersession links.
- Do not use decisions as feature specs or technical reference docs.
"""


PLAN_README = """# Plan Archive

Store workflow planning documents here.

## Rules
- Prefer `YYYY-MM-DD_topic.md`.
- Record related intake, features, requirements, specs, and decisions.
- Record stable-doc impact before implementation.
"""


CHANGE_README = """# Change Archive

Store completed workflow result documents here.

## Rules
- Prefer `YYYY-MM-DD_topic.md`.
- Record related intake, features, requirements, specs, decisions, and lessons.
- Record whether stable docs changed.
- Promote reusable troubleshooting knowledge into `lessons` instead of leaving it only here.
"""


LESSONS_README = """# Lessons

Store reusable lessons, root-cause analyses, and prevention guidance here.

## Rules
- Use stable names without dates when the lesson is long-lived.
- Group by module or domain when useful.
- Capture lookup hints such as symptoms, trigger conditions, keywords, and quick checks.
- Link lessons back to relevant stable docs and changes.
"""


MODULE_FEATURES = """# {module} Features

Store current feature behavior for `{module}` here.
"""


MODULE_REQUIREMENTS = """# {module} Requirements

Store durable requirements for `{module}` here.
"""


MODULE_SPECS = """# {module} Specs

Store technical contracts and constraints for `{module}` here.
"""


MODULE_LESSONS = """# {module} Lessons

Store recurring problems, query-friendly troubleshooting notes, and prevention guidance for `{module}` here.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a governed docs tree.")
    parser.add_argument(
        "project_root",
        nargs="?",
        help="Project root where docs/ should be created when --docs-root is not provided.",
    )
    parser.add_argument(
        "--docs-root",
        help="Explicit docs root to create or repair. Use this for private docs outside code repos.",
    )
    parser.add_argument(
        "--module",
        action="append",
        default=[],
        help="Optional module bucket name. Repeatable.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Show planned actions only")
    return parser.parse_args()


def resolve_docs_root(args: argparse.Namespace) -> Path:
    if args.docs_root:
        return Path(args.docs_root).resolve()
    if args.project_root:
        return Path(args.project_root).resolve() / "docs"
    raise ValueError("Pass project_root or --docs-root.")


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

    try:
        docs_root = resolve_docs_root(args)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2

    base_dirs = [
        docs_root,
        docs_root / "intake",
        docs_root / "features",
        docs_root / "requirements",
        docs_root / "specs",
        docs_root / "decisions",
        docs_root / "plan",
        docs_root / "change",
        docs_root / "lessons",
    ]

    for directory in base_dirs:
        ensure_directory(directory, args.dry_run)

    actions = [
        write_file(docs_root / "README.md", ROOT_README, args.force, args.dry_run),
        write_file(docs_root / "intake" / "README.md", INTAKE_README, args.force, args.dry_run),
        write_file(docs_root / "features" / "README.md", FEATURES_README, args.force, args.dry_run),
        write_file(docs_root / "requirements" / "README.md", REQUIREMENTS_README, args.force, args.dry_run),
        write_file(docs_root / "specs" / "README.md", SPECS_README, args.force, args.dry_run),
        write_file(docs_root / "decisions" / "README.md", DECISIONS_README, args.force, args.dry_run),
        write_file(docs_root / "plan" / "README.md", PLAN_README, args.force, args.dry_run),
        write_file(docs_root / "change" / "README.md", CHANGE_README, args.force, args.dry_run),
        write_file(docs_root / "lessons" / "README.md", LESSONS_README, args.force, args.dry_run),
    ]

    for raw_module in args.module:
        module = raw_module.strip()
        if not module:
            continue
        module_dirs = [
            docs_root / "features" / module,
            docs_root / "requirements" / module,
            docs_root / "specs" / module,
            docs_root / "lessons" / module,
        ]
        for directory in module_dirs:
            ensure_directory(directory, args.dry_run)
        actions.extend(
            [
                write_file(
                    docs_root / "features" / module / "README.md",
                    MODULE_FEATURES.format(module=module),
                    args.force,
                    args.dry_run,
                ),
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

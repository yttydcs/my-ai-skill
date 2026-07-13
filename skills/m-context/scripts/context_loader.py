#!/usr/bin/env python3
"""Resolve and load reusable plaintext Agent context files."""

from __future__ import annotations

import argparse
import difflib
import os
from pathlib import Path
import re
import sys
from typing import Mapping, Sequence


HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


class ContextError(Exception):
    """An actionable context loading failure."""


def resolve_context_root(
    environ: Mapping[str, str] | None = None,
    *,
    home: Path | None = None,
) -> Path:
    env = os.environ if environ is None else environ
    configured = env.get("M_CONTEXT_HOME", "").strip()
    if configured:
        return Path(configured).expanduser().resolve(strict=False)

    codex_home = env.get("CODEX_HOME", "").strip()
    if codex_home:
        return (Path(codex_home).expanduser() / "m-contexts").resolve(strict=False)

    user_home = Path.home() if home is None else home
    return (user_home / ".codex" / "m-contexts").resolve(strict=False)


def _require_root(root: Path) -> Path:
    try:
        resolved = root.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ContextError(
            f"Context root does not exist: {root}. "
            "Create it or set M_CONTEXT_HOME/CODEX_HOME."
        ) from exc
    except OSError as exc:
        raise ContextError(f"Cannot resolve context root {root}: {exc}") from exc

    if not resolved.is_dir():
        raise ContextError(f"Context root is not a directory: {resolved}")
    return resolved


def validate_context_name(name: str) -> str:
    value = name.strip()
    if not value:
        raise ContextError("Context name must not be empty.")
    if value in {".", ".."} or "/" in value or "\\" in value or "\x00" in value:
        raise ContextError(f"Unsafe context name: {name!r}")
    if any(character in value for character in '<>:"|?*'):
        raise ContextError(f"Context name contains a Windows-reserved character: {name!r}")
    if value != value.rstrip(" ."):
        raise ContextError(f"Context name must not end with a space or dot: {name!r}")
    if value.casefold().endswith(".md"):
        raise ContextError("Pass the context name without the .md extension.")
    if value.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES:
        raise ContextError(f"Context name is reserved by Windows: {name!r}")
    if Path(value).is_absolute() or os.path.splitdrive(value)[0]:
        raise ContextError(f"Context name must not be an absolute or drive-qualified path: {name!r}")
    return value


def _is_within(path: Path, root: Path) -> bool:
    try:
        return os.path.commonpath((str(path), str(root))) == str(root)
    except ValueError:
        return False


def resolve_context_file(root: Path, name: str) -> Path:
    safe_name = validate_context_name(name)
    resolved_root = _require_root(root)
    candidate = resolved_root / f"{safe_name}.md"
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        suggestions = difflib.get_close_matches(
            safe_name,
            list_contexts(resolved_root),
            n=3,
            cutoff=0.4,
        )
        suffix = f" Nearby names: {', '.join(suggestions)}." if suggestions else ""
        raise ContextError(f"Context not found: {safe_name!r} in {resolved_root}.{suffix}") from exc
    except OSError as exc:
        raise ContextError(f"Cannot resolve context {safe_name!r}: {exc}") from exc

    if not _is_within(resolved, resolved_root):
        raise ContextError(f"Context resolves outside the configured root: {safe_name!r}")
    if not resolved.is_file():
        raise ContextError(f"Context is not a regular file: {resolved}")
    return resolved


def list_contexts(root: Path) -> list[str]:
    resolved_root = _require_root(root)
    names: list[str] = []
    try:
        candidates = resolved_root.glob("*.md")
        for candidate in candidates:
            try:
                resolved = candidate.resolve(strict=True)
            except OSError:
                continue
            if resolved.is_file() and _is_within(resolved, resolved_root):
                names.append(candidate.stem)
    except OSError as exc:
        raise ContextError(f"Cannot list context root {resolved_root}: {exc}") from exc
    return sorted(names, key=str.casefold)


def find_contexts(root: Path, query: str) -> list[str]:
    value = query.strip()
    if not value:
        raise ContextError("Find query must not be empty.")
    folded = value.casefold()
    return [name for name in list_contexts(root) if folded in name.casefold()]


def _read_context(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ContextError(f"Context is not valid UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise ContextError(f"Cannot read context {path}: {exc}") from exc


def _heading_text(raw: str) -> str:
    value = raw.strip()
    closing = re.search(r"[ \t]+#+$", value)
    if closing:
        value = value[: closing.start()].rstrip()
    return value


def extract_section(content: str, section: str) -> str:
    wanted = section.strip()
    if not wanted:
        raise ContextError("Section name must not be empty.")

    lines = content.splitlines(keepends=True)
    headings: list[tuple[int, int, str]] = []
    fence_character: str | None = None
    fence_length = 0
    for index, line in enumerate(lines):
        plain_line = line.rstrip("\r\n")
        fence = FENCE_RE.match(plain_line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            continue
        if fence_character is not None:
            continue

        match = HEADING_RE.match(plain_line)
        if match:
            headings.append((index, len(match.group(1)), _heading_text(match.group(2))))

    matches = [heading for heading in headings if heading[2] == wanted]
    if not matches:
        available = ", ".join(dict.fromkeys(text for _, _, text in headings)) or "none"
        raise ContextError(f"Section not found: {wanted!r}. Available headings: {available}.")
    if len(matches) > 1:
        locations = ", ".join(str(index + 1) for index, _, _ in matches)
        raise ContextError(f"Section is ambiguous: {wanted!r}; matching lines: {locations}.")

    start, level, _ = matches[0]
    end = len(lines)
    for index, next_level, _ in headings:
        if index > start and next_level <= level:
            end = index
            break
    return "".join(lines[start:end])


def load_context(root: Path, name: str, section: str | None = None) -> str:
    content = _read_context(resolve_context_file(root, name))
    return content if section is None else extract_section(content, section)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("root", help="Print the resolved context root.")
    subparsers.add_parser("list", help="List exact context names.")

    find_parser = subparsers.add_parser("find", help="Find context names by substring.")
    find_parser.add_argument("query")

    load_parser = subparsers.add_parser("load", help="Load a complete context or one section.")
    load_parser.add_argument("name")
    load_parser.add_argument("--section")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = resolve_context_root()

    try:
        if args.command == "root":
            print(root)
        elif args.command == "list":
            print("\n".join(list_contexts(root)))
        elif args.command == "find":
            print("\n".join(find_contexts(root, args.query)))
        elif args.command == "load":
            content = load_context(root, args.name, args.section)
            sys.stdout.write(content)
            if content and not content.endswith(("\n", "\r")):
                sys.stdout.write("\n")
        else:  # pragma: no cover - argparse owns command validation
            parser.error(f"Unknown command: {args.command}")
    except ContextError as exc:
        print(f"m-context: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())

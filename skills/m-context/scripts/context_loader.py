#!/usr/bin/env python3
"""Resolve and load reusable plaintext Agent context files."""

from __future__ import annotations

import argparse
import difflib
from enum import Enum
import os
from pathlib import Path
import re
import sys
from typing import Mapping, NamedTuple, Sequence


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


class ContextNotFoundError(ContextError):
    """A missing root or exact context that may permit auto fallback."""


class ContextScope(str, Enum):
    AUTO = "auto"
    LOCAL = "local"
    GLOBAL = "global"


class ContextLocation(NamedTuple):
    scope: ContextScope
    root: Path
    path: Path


class LoadedContext(NamedTuple):
    location: ContextLocation
    content: str


class ContextEntry(NamedTuple):
    scope: ContextScope
    name: str
    root: Path


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


def resolve_local_context_root(docs_root: Path | str | None) -> Path:
    if docs_root is None or (isinstance(docs_root, str) and not docs_root.strip()):
        raise ContextError(
            "Local context scope requires an explicit docs root; "
            "resolve docs_root and pass --docs-root."
        )
    return (Path(docs_root).expanduser().resolve(strict=False) / "context").resolve(
        strict=False
    )


def parse_context_scope(scope: ContextScope | str) -> ContextScope:
    if isinstance(scope, ContextScope):
        return scope
    try:
        return ContextScope(scope.strip().casefold())
    except (AttributeError, ValueError) as exc:
        allowed = ", ".join(item.value for item in ContextScope)
        raise ContextError(f"Invalid context scope {scope!r}; expected one of: {allowed}.") from exc


def _require_root(root: Path) -> Path:
    try:
        resolved = root.resolve(strict=True)
    except FileNotFoundError as exc:
        if os.path.lexists(root):
            raise ContextError(f"Cannot resolve existing context root {root}: {exc}") from exc
        raise ContextNotFoundError(
            f"Context root does not exist: {root}. Create it or configure the intended scope."
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
        if os.path.lexists(candidate):
            raise ContextError(
                f"Cannot resolve existing context {safe_name!r}: {exc}"
            ) from exc
        suggestions = difflib.get_close_matches(
            safe_name,
            list_contexts(resolved_root),
            n=3,
            cutoff=0.4,
        )
        suffix = f" Nearby names: {', '.join(suggestions)}." if suggestions else ""
        raise ContextNotFoundError(
            f"Context not found: {safe_name!r} in {resolved_root}.{suffix}"
        ) from exc
    except OSError as exc:
        raise ContextError(f"Cannot resolve context {safe_name!r}: {exc}") from exc

    if not _is_within(resolved, resolved_root):
        raise ContextError(f"Context resolves outside the configured root: {safe_name!r}")
    if not resolved.is_file():
        raise ContextError(f"Context is not a regular file: {resolved}")
    return resolved


def _list_contexts_in_root(resolved_root: Path) -> list[str]:
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


def list_contexts(root: Path) -> list[str]:
    return _list_contexts_in_root(_require_root(root))


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


def _global_root(global_root: Path | str | None) -> Path:
    if global_root is None:
        return resolve_context_root()
    return Path(global_root).expanduser().resolve(strict=False)


def _location_for_scope(
    scope: ContextScope,
    name: str,
    *,
    docs_root: Path | str | None,
    global_root: Path | str | None,
) -> ContextLocation:
    if scope is ContextScope.LOCAL:
        root = resolve_local_context_root(docs_root)
    elif scope is ContextScope.GLOBAL:
        root = _global_root(global_root)
    else:  # pragma: no cover - callers resolve auto before selecting a root
        raise ContextError("Auto scope must be resolved before selecting a context root.")
    return ContextLocation(scope, root, resolve_context_file(root, name))


def resolve_scoped_context(
    name: str,
    *,
    scope: ContextScope | str = ContextScope.AUTO,
    docs_root: Path | str | None = None,
    global_root: Path | str | None = None,
) -> ContextLocation:
    selected_scope = parse_context_scope(scope)
    validate_context_name(name)

    if selected_scope is not ContextScope.AUTO:
        return _location_for_scope(
            selected_scope,
            name,
            docs_root=docs_root,
            global_root=global_root,
        )

    local_missing: ContextNotFoundError | None = None
    local_root: Path | None = None
    if docs_root is not None:
        local_root = resolve_local_context_root(docs_root)
        try:
            return _location_for_scope(
                ContextScope.LOCAL,
                name,
                docs_root=docs_root,
                global_root=global_root,
            )
        except ContextNotFoundError as exc:
            local_missing = exc

    try:
        return _location_for_scope(
            ContextScope.GLOBAL,
            name,
            docs_root=docs_root,
            global_root=global_root,
        )
    except ContextNotFoundError as global_missing:
        if local_missing is None:
            raise
        raise ContextNotFoundError(
            f"Context not found in local or global scope: {name!r}. "
            f"Tried local root {local_root} and global root {_global_root(global_root)}."
        ) from global_missing


def load_scoped_context(
    name: str,
    section: str | None = None,
    *,
    scope: ContextScope | str = ContextScope.AUTO,
    docs_root: Path | str | None = None,
    global_root: Path | str | None = None,
) -> LoadedContext:
    location = resolve_scoped_context(
        name,
        scope=scope,
        docs_root=docs_root,
        global_root=global_root,
    )
    content = _read_context(location.path)
    if section is not None:
        content = extract_section(content, section)
    return LoadedContext(location, content)


def _list_scope(root: Path, scope: ContextScope) -> list[ContextEntry]:
    resolved_root = _require_root(root)
    return [
        ContextEntry(scope, name, resolved_root)
        for name in _list_contexts_in_root(resolved_root)
    ]


def list_scoped_contexts(
    *,
    scope: ContextScope | str = ContextScope.AUTO,
    docs_root: Path | str | None = None,
    global_root: Path | str | None = None,
) -> list[ContextEntry]:
    selected_scope = parse_context_scope(scope)
    if selected_scope is ContextScope.LOCAL:
        return _list_scope(resolve_local_context_root(docs_root), ContextScope.LOCAL)
    if selected_scope is ContextScope.GLOBAL:
        return _list_scope(_global_root(global_root), ContextScope.GLOBAL)

    if docs_root is None:
        return _list_scope(_global_root(global_root), ContextScope.GLOBAL)

    entries: list[ContextEntry] = []
    available_root = False
    local_root = resolve_local_context_root(docs_root)
    try:
        entries.extend(_list_scope(local_root, ContextScope.LOCAL))
        available_root = True
    except ContextNotFoundError:
        pass

    resolved_global_root = _global_root(global_root)
    try:
        entries.extend(_list_scope(resolved_global_root, ContextScope.GLOBAL))
        available_root = True
    except ContextNotFoundError as global_missing:
        if not available_root:
            raise ContextNotFoundError(
                "No context roots exist for auto discovery. "
                f"Tried local root {local_root} and global root {resolved_global_root}."
            ) from global_missing

    return entries


def find_scoped_contexts(
    query: str,
    *,
    scope: ContextScope | str = ContextScope.AUTO,
    docs_root: Path | str | None = None,
    global_root: Path | str | None = None,
) -> list[ContextEntry]:
    value = query.strip()
    if not value:
        raise ContextError("Find query must not be empty.")
    folded = value.casefold()
    return [
        entry
        for entry in list_scoped_contexts(
            scope=scope,
            docs_root=docs_root,
            global_root=global_root,
        )
        if folded in entry.name.casefold()
    ]


def _add_scope_arguments(
    parser: argparse.ArgumentParser,
    *,
    default: ContextScope,
    allow_auto: bool = True,
) -> None:
    choices = [ContextScope.LOCAL.value, ContextScope.GLOBAL.value]
    if allow_auto:
        choices.insert(0, ContextScope.AUTO.value)
    parser.add_argument("--scope", choices=choices, default=default.value)
    parser.add_argument("--docs-root")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    root_parser = subparsers.add_parser("root", help="Print a resolved context root.")
    _add_scope_arguments(
        root_parser,
        default=ContextScope.GLOBAL,
        allow_auto=False,
    )

    list_parser = subparsers.add_parser("list", help="List exact context names and scopes.")
    _add_scope_arguments(list_parser, default=ContextScope.AUTO)

    find_parser = subparsers.add_parser("find", help="Find context names by substring.")
    find_parser.add_argument("query")
    _add_scope_arguments(find_parser, default=ContextScope.AUTO)

    load_parser = subparsers.add_parser("load", help="Load a complete context or one section.")
    load_parser.add_argument("name")
    load_parser.add_argument("--section")
    _add_scope_arguments(load_parser, default=ContextScope.AUTO)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "root":
            if args.scope == ContextScope.LOCAL.value:
                print(resolve_local_context_root(args.docs_root))
            else:
                print(resolve_context_root())
        elif args.command == "list":
            entries = list_scoped_contexts(scope=args.scope, docs_root=args.docs_root)
            print("\n".join(f"{entry.scope.value}:{entry.name}" for entry in entries))
        elif args.command == "find":
            entries = find_scoped_contexts(
                args.query,
                scope=args.scope,
                docs_root=args.docs_root,
            )
            print("\n".join(f"{entry.scope.value}:{entry.name}" for entry in entries))
        elif args.command == "load":
            loaded = load_scoped_context(
                args.name,
                args.section,
                scope=args.scope,
                docs_root=args.docs_root,
            )
            sys.stdout.write(loaded.content)
            if loaded.content and not loaded.content.endswith(("\n", "\r")):
                sys.stdout.write("\n")
            local_note = ""
            if args.scope == ContextScope.AUTO.value and args.docs_root is None:
                local_note = "local lookup unavailable (--docs-root not supplied); "
            print(
                f"m-context: {local_note}loaded {loaded.location.scope.value}:{args.name} "
                f"from {loaded.location.path}",
                file=sys.stderr,
            )
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

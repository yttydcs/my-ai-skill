"""Bound, cache-free Agent Memory client. Requires only Python's standard library."""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import (
    HTTPRedirectHandler,
    HTTPSHandler,
    ProxyHandler,
    Request,
    build_opener,
)
from uuid import UUID


class MemoryError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def uuid(value):
    try:
        return str(UUID(value))
    except (ValueError, TypeError, AttributeError):
        raise MemoryError("binding or request contains an invalid UUID") from None


class MemoryClient:
    def __init__(self, binding):
        self.path = Path(binding).expanduser().resolve()
        try:
            self.config = json.loads(self.path.read_text(encoding="utf-8-sig"))
            c = self.config
            if c.get("version") != 1 or c.get("backend") != "agent-memory":
                raise MemoryError("binding requires version=1 and backend=agent-memory")
            self.url = c["url"].rstrip("/")
            endpoint = urlsplit(self.url)
            if (
                endpoint.scheme not in {"http", "https"}
                or not endpoint.hostname
                or endpoint.username
                or endpoint.password
                or endpoint.query
                or endpoint.fragment
                or endpoint.path
                or (
                    endpoint.scheme == "http"
                    and endpoint.hostname not in {"127.0.0.1", "localhost", "::1"}
                )
            ):
                raise MemoryError(
                    "binding requires an HTTPS origin (HTTP only on loopback)"
                )
            self.read_libraries = [uuid(x) for x in c["read_libraries"]]
            self.write_library = (
                uuid(c["write_library"]) if c.get("write_library") else None
            )
            self.sources = [uuid(x) for x in c["allowed_source_libraries"]]
            if not self.read_libraries or not set(self.sources) <= set(
                self.read_libraries
            ):
                raise MemoryError(
                    "source libraries must be explicitly selected read libraries"
                )
            self.budget = c["budget_bytes"]
            if type(self.budget) is not int or not 256 <= self.budget <= 65536:
                raise MemoryError("budget_bytes must be between 256 and 65536")
            self.token_path = self.resolve_file(c["token_file"])
            self.ca_path = self.resolve_file(c["ca_file"]) if c.get("ca_file") else None
        except (OSError, ValueError, KeyError, TypeError):
            raise MemoryError(
                "invalid or unreadable memory binding; no local fallback"
            ) from None

    def resolve_file(self, value):
        path = Path(value).expanduser()
        return path if path.is_absolute() else self.path.parent / path

    def library(self, selected=None, *, write=False):
        if write and self.write_library is None:
            raise MemoryError(
                "binding is read-only; select an authorized write target explicitly"
            )
        if selected is None:
            if write:
                selected = self.write_library
            elif len(self.read_libraries) == 1:
                selected = self.read_libraries[0]
            else:
                raise MemoryError(
                    "select --library explicitly when reading multiple libraries"
                )
        selected = uuid(selected)
        if (write and selected != self.write_library) or (
            not write and selected not in self.read_libraries
        ):
            raise MemoryError("library is outside the selected binding scope")
        return selected

    def _scope(self, value):
        if isinstance(value, dict):
            for key, item in value.items():
                if (
                    key in {"source_library_id", "target_library_id"}
                    and uuid(item) not in self.sources
                ):
                    raise MemoryError(
                        "dependency/reference library is outside selected sources"
                    )
                if key in {"read_libraries", "allowed_source_libraries", "libraries"}:
                    values = item if isinstance(item, list) else [item]
                    if not {uuid(x) for x in values} <= set(self.sources):
                        raise MemoryError(
                            "request expands the configured library scope"
                        )
                if key == "budget_bytes" and (
                    type(item) is not int or not 256 <= item <= self.budget
                ):
                    raise MemoryError("request exceeds the configured byte budget")
                self._scope(item)
        elif isinstance(value, list):
            for item in value:
                self._scope(item)

    def request(self, method, suffix, *, library=None, body=None, params=None):
        # Only library-relative API paths; no origin overrides or encoded traversal.
        pieces = suffix.split("/")
        if (
            not suffix
            or suffix.startswith("/")
            or any(p in {"", ".", ".."} for p in pieces)
            or any(c in suffix for c in "%?#\\")
            or any(ord(c) < 32 for c in suffix)
        ):
            raise MemoryError("request path must be a library-relative API path")
        search = method == "POST" and pieces[-1] in {"search", "document-search"}
        selected = self.library(library, write=method != "GET" and not search)
        query = dict(params or {})
        self._scope(query)
        self._scope(body)
        if method == "GET":
            query.setdefault("allowed_source_libraries", self.sources)
            query.setdefault("budget_bytes", self.budget)
            if pieces[-1] == "references":
                query.setdefault("libraries", self.sources)
        if search:
            body = dict(body or {})
            body.setdefault("allowed_source_libraries", self.sources)
            body.setdefault("budget_bytes", self.budget)
        try:
            token = self.token_path.read_text(encoding="utf-8").strip()
            if not token:
                raise MemoryError("empty device token")
            context = ssl.create_default_context(
                cafile=str(self.ca_path) if self.ca_path else None
            )
            opener = build_opener(
                ProxyHandler({}), HTTPSHandler(context=context), NoRedirect()
            )
            url = f"{self.url}/v1/libraries/{selected}/{suffix}"
            if query:
                url += "?" + urlencode(query, doseq=True)
            data = (
                None
                if body is None
                else json.dumps(body, ensure_ascii=False).encode("utf-8")
            )
            req = Request(
                url,
                data=data,
                method=method,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )
            with opener.open(req, timeout=30) as response:
                raw = response.read(self.budget + 1)
            if len(raw) > self.budget:
                raise MemoryError(
                    "response exceeds binding budget; narrow the read or explicitly adjust budget; a write may have committed, reconcile before retrying"
                )
            return json.loads(raw) if raw else None
        except HTTPError as exc:
            # Keep structured service errors, but never echo URLs or credential headers.
            raw = exc.read(self.budget)
            try:
                detail = json.loads(raw)
            except (ValueError, UnicodeError):
                detail = "non-JSON service error"
            raise MemoryError(
                f"HTTP {exc.code}: {json.dumps(detail, ensure_ascii=False)}", exc.code
            ) from None
        except (URLError, OSError, ValueError) as exc:
            raise MemoryError(
                f"memory operation unavailable ({type(exc).__name__}); no local fallback; a write may have committed, reconcile before retrying"
            ) from None

    def search(self, query, *, library=None, target="both", category=None, extra=None):
        selected = self.library(library)
        index = self.config.get("indexes", {}).get(selected)
        if not index:
            raise MemoryError("selected library has no configured search index")
        method = index["method"]
        endpoint = "document-search" if method in {"bm25", "bm25_vector"} else "search"
        body = dict(extra or {})
        # Explicit options may add vectors/filters, but cannot replace binding identity.
        reserved = {"method", "expected_index_revision", "query", "target"}
        if reserved & body.keys():
            raise MemoryError(
                "search options cannot override method, index revision, query or target"
            )
        body.update(
            method=method,
            expected_index_revision=uuid(index["revision"]),
            target=target,
        )
        if method != "vector_exact":
            body["query"] = query
        if category:
            body["metadata_filter"] = {
                **body.get("metadata_filter", {}),
                "category": category,
            }
        return self.request(
            "POST",
            f"section-indexes/{uuid(index['id'])}/{endpoint}",
            library=selected,
            body=body,
        )

    def read(self, object_id, *, library=None, revision=None):
        result = self.request("GET", f"objects/{uuid(object_id)}", library=library)
        if revision and result["revision"] != uuid(revision):
            raise MemoryError("object revision changed; reread and reconcile", 409)
        return result

    def commit(self, body, *, library=None, archive=False):
        if (
            not isinstance(body, dict)
            or not body.get("idempotency_key")
            or not body.get("operations")
        ):
            raise MemoryError(
                "commit requires caller-selected idempotency_key and nonempty operations"
            )
        if archive and not body.get("lease_guard"):
            raise MemoryError("archive commit requires lease_guard")
        return self.request("POST", "commits", library=library, body=body)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", default=os.environ.get("M_MEMORY_BINDING"))
    parser.add_argument("--library")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "check", help="Verify selected library access; prints no credentials"
    )
    search = commands.add_parser("search")
    search.add_argument("query")
    search.add_argument(
        "--target", choices=["source", "derived", "both"], default="both"
    )
    search.add_argument("--category")
    search.add_argument(
        "--body-stdin",
        action="store_true",
        help="Extra search options, including caller-generated vectors",
    )
    read = commands.add_parser("read")
    read.add_argument("object_id")
    read.add_argument("--revision")
    commit = commands.add_parser(
        "commit", help="Read the complete CAS bundle from stdin"
    )
    commit.add_argument("--archive", action="store_true")
    request = commands.add_parser(
        "request", help="Library-relative JSON API, including leases and provenance"
    )
    request.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    request.add_argument("path")
    request.add_argument("--body-stdin", action="store_true")
    request.add_argument("--query", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        if not args.binding:
            raise MemoryError(
                "select --binding or project M_MEMORY_BINDING; no implicit library"
            )
        client = MemoryClient(args.binding)
        if args.command == "check":
            # Metadata only; this does not load all documents or build any index.
            result = client.request("GET", "section-indexes", library=args.library)
        elif args.command == "search":
            result = client.search(
                args.query,
                library=args.library,
                target=args.target,
                category=args.category,
                extra=json.load(sys.stdin) if args.body_stdin else None,
            )
        elif args.command == "read":
            result = client.read(
                args.object_id, library=args.library, revision=args.revision
            )
        elif args.command == "commit":
            result = client.commit(
                json.load(sys.stdin), library=args.library, archive=args.archive
            )
        else:
            params = {}
            for item in args.query:
                key, sep, value = item.partition("=")
                if not sep or not key:
                    raise MemoryError("query requires KEY=VALUE")
                params.setdefault(key, []).append(
                    int(value) if key == "budget_bytes" else value
                )
            if "budget_bytes" in params:
                if len(params["budget_bytes"]) != 1:
                    raise MemoryError("provide budget_bytes once")
                params["budget_bytes"] = params["budget_bytes"][0]
            result = client.request(
                args.method,
                args.path,
                library=args.library,
                params=params,
                body=json.load(sys.stdin) if args.body_stdin else None,
            )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (MemoryError, OSError, ValueError, KeyError, TypeError) as exc:
        message = (
            str(exc)
            if isinstance(exc, MemoryError)
            else f"invalid input ({type(exc).__name__})"
        )
        print(f"m-memory: {message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())

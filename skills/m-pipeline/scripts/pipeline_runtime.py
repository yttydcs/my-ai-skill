#!/usr/bin/env python3
"""JSON-file command boundary; no host calls and no shell command evaluation."""

import argparse
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

from pipeline_lib.config import (PipelineError, fields, load_json, plan_ref, state_root,
                                 validate_blueprint)
from pipeline_lib.store import Store
from pipeline_lib.workflow import Engine


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "fingerprint", "apply"))
    parser.add_argument("--input", required=True, help="UTF-8 JSON file; never inline secret-bearing input")
    parser.add_argument("--state-root", help="Shared local state directory outside project repositories")
    args = parser.parse_args(argv)
    try:
        value = load_json(args.input)
        if args.command == "validate":
            config = validate_blueprint(value, Path(args.input).resolve().parent)
            output = {"valid": True, "roles": list(config["roles"]), "stages": [s["id"] for s in config["stages"]]}
        elif args.command == "fingerprint":
            fields(value, ("path", "sections"))
            output = plan_ref(value, Path(value["path"]).resolve().parent)
        else:
            output = Engine(Store(state_root(args.state_root))).apply(value)
        print(json.dumps({"ok": True, "result": output}, ensure_ascii=False))
        return 0
    except PipelineError as exc:
        print(json.dumps({"ok": False, "error": {"code": exc.code, "message": str(exc)}}, ensure_ascii=False))
        return 2
    except (OSError, UnicodeError, sqlite3.Error, subprocess.SubprocessError) as exc:
        print(json.dumps({"ok": False, "error": {"code": "environment_error", "message": type(exc).__name__}}, ensure_ascii=False))
        return 3


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())

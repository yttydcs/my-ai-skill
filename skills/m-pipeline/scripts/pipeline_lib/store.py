"""One transactional authority for cooperating local runs and shared claims."""

from contextlib import closing, contextmanager
from pathlib import Path
import json
import sqlite3

from .config import PipelineError, canonical, require


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
 id TEXT PRIMARY KEY, coordinator TEXT NOT NULL, revision INTEGER NOT NULL,
 data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
 key TEXT PRIMARY KEY, data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS claims (
 resource TEXT PRIMARY KEY, run_id TEXT NOT NULL, assignment TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS operations (
 id TEXT PRIMARY KEY, run_id TEXT NOT NULL, assignment TEXT, kind TEXT NOT NULL,
 state TEXT NOT NULL, data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
 seq INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL,
 action TEXT NOT NULL, revision INTEGER NOT NULL,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
"""


class Store:
    def __init__(self, root):
        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)
        self.path = root / "pipeline.sqlite3"
        with closing(self.connect()) as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            require(version in (0, 1), "Unsupported state database version; use a compatible runtime", "state_version")
            db.executescript(SCHEMA)
            db.execute("PRAGMA user_version=1")

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=10000")
        return db

    @contextmanager
    def transaction(self):
        db = self.connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except sqlite3.OperationalError as exc:
            db.rollback()
            raise PipelineError("store_busy", "Local state is busy/unavailable; retry after inspecting the store") from exc
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def read(self, run_id):
        with closing(self.connect()) as db:
            row = db.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
            require(row is not None, "Unknown run", "not_found")
            return json.loads(row["data"]), row["revision"]

    @staticmethod
    def claim(db, resources, run_id, assignment):
        resources = sorted(set(resources))
        for resource in resources:
            row = db.execute("SELECT * FROM claims WHERE resource=?", (resource,)).fetchone()
            if row is not None and (row["run_id"], row["assignment"]) != (run_id, assignment):
                return False
        for resource in resources:
            db.execute("INSERT OR IGNORE INTO claims VALUES (?,?,?)", (resource, run_id, assignment))
        return True

    @staticmethod
    def release(db, run_id, assignment):
        db.execute("DELETE FROM claims WHERE run_id=? AND assignment=?", (run_id, assignment))

    @staticmethod
    def operation(db, op_id):
        row = db.execute("SELECT * FROM operations WHERE id=?", (op_id,)).fetchone()
        require(row is not None, "Unknown operation ID", "not_found")
        return dict(row) | {"data": json.loads(row["data"])}

    @staticmethod
    def update_operation(db, operation, state, data):
        db.execute("UPDATE operations SET state=?, data=? WHERE id=?",
                   (state, canonical(data), operation["id"]))

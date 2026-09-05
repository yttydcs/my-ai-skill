"""Decision engine. Host calls and semantic phase review stay with the coordinator."""

from __future__ import annotations

import json
from contextlib import closing
from pathlib import Path
import re
import uuid

from .config import (PipelineError, artifact, canonical, digest, fields, inside, label,
                     load_json, path_at, plan_ref, require, session_key, snapshot,
                     string, strings, validate_blueprint, path_key, phase_contract)
from .store import Store


BUSY = {"reserved", "dispatched", "running", "uncertain"}


def stage_of(run, key):
    matches = [s for s in run["config"]["stages"] if s["id"] == key]
    require(len(matches) == 1, "Unknown stage")
    return matches[0]


def roots(run, repositories=None):
    return [run["config"]["docs_root"]] + [v["worktree"] for v in (repositories or {}).values()]


def plan_check(packet, phase):
    required = phase not in ("m-discuss", "m-plan")
    require(isinstance(packet["plans"], dict), "plans must map repository keys to root plans")
    require(not required or packet["plans"].keys() == packet["repositories"].keys(),
            "Every participating repository needs its approved root plan")
    checked = {}
    for key, value in packet["plans"].items():
        require(key in packet["repositories"], "Plan references an undeclared candidate")
        require("revision" in value, "Fingerprint and review the plan definition before admission")
        checked[key] = plan_ref(value, packet["repositories"][key]["worktree"])
    return checked


def write_set(config, value, repositories):
    require(isinstance(value, list), "write_set must be an array")
    result = []
    for item in value:
        fields(item, ("repo", "path"))
        require(item["repo"] in repositories, "Write set references an undeclared candidate")
        relative = string(item["path"], "write path")
        require(not Path(relative).is_absolute() and not re.match(r"^[A-Za-z]:", relative)
                and ".." not in re.split(r"[/\\]", relative), "Use confined relative write paths")
        relative = relative.replace("\\", "/").rstrip("/") or "."
        resolved = path_at(relative, repositories[item["repo"]]["worktree"], exists=False)
        require(inside(resolved, repositories[item["repo"]]["worktree"]), "Write path escapes worktree")
        result.append({"repo": item["repo"], "path": relative})
    require(len({canonical(x) for x in result}) == len(result), "Duplicate write path")
    return result


def overlaps(left, right):
    for a in left:
        for b in right:
            if a["repo"] != b["repo"]:
                continue
            x, y = a["path"].casefold(), b["path"].casefold()
            if x == "." or y == "." or x == y or x.startswith(y + "/") or y.startswith(x + "/"):
                return True
    return False


def candidates(packet):
    return {key: value["commit"] for key, value in packet["repositories"].items()}


class Engine:
    def __init__(self, store):
        self.store = store

    def apply(self, request):
        fields(request, ("action", "run_id", "actor", "payload"))
        action, run_id = label(request["action"]), label(request["run_id"])
        actor = session_key(request["actor"])
        payload = request["payload"]
        if action == "init":
            return self.initialize(run_id, actor, payload)
        run, revision = self.store.read(run_id)
        require(action in ("status", "bootstrap", "authorize", "bind", "observe", "admit", "next", "operation_result",
                           "result", "pause", "resume", "takeover", "retry", "invalidate", "finish", "transfer"),
                "Unknown action")
        if action == "status":
            fields(payload, ())
            return self.status(run, revision)
        require(run["coordinator"] == actor, "Only the current coordinator may mutate this run", "not_owner")
        # Filesystem and Git verification happen before the short write transaction.
        prepared = self.prepare(run, action, payload)
        with self.store.transaction() as db:
            row = db.execute("SELECT revision FROM runs WHERE id=?", (run_id,)).fetchone()
            require(row["revision"] == revision, "Run changed; reload status and retry the decision", "stale_run")
            output = getattr(self, "do_" + action)(db, run, prepared)
            db.execute("UPDATE runs SET data=?,revision=? WHERE id=?",
                       (canonical(run), revision + 1, run_id))
            db.execute("INSERT INTO events(run_id,action,revision) VALUES (?,?,?)", (run_id, action, revision + 1))
            return output | {"run_id": run_id, "revision": revision + 1}

    def initialize(self, run_id, actor, payload):
        fields(payload, ("blueprint",))
        blueprint = path_at(payload["blueprint"], Path.cwd())
        config = validate_blueprint(load_json(blueprint), blueprint.parent)
        require(not inside(self.store.path, config["project_root"]) and not inside(self.store.path, config["docs_root"])
                and not any(inside(self.store.path, r["path"]) or inside(self.store.path, r["worktree_root"])
                            for r in config["repositories"].values()), "Keep runtime state outside project repositories")
        run = {"id": run_id, "coordinator": actor, "status": "draft", "config": config,
               "blueprint_ref": {"path": str(blueprint), "revision": digest(config)},
               "authority": None, "setup_authority": None, "jobs": {}, "sealed": {}, "bindings": {}, "created": 0}
        with self.store.transaction() as db:
            old = db.execute("SELECT data FROM runs WHERE id=?", (run_id,)).fetchone()
            if old:
                previous = json.loads(old[0])
                require(previous["blueprint_ref"] == run["blueprint_ref"] and previous["coordinator"] == actor,
                        "Run ID already belongs to another definition/owner")
                return {"run_id": run_id, "status": previous["status"], "existing": True}
            db.execute("INSERT INTO runs VALUES (?,?,0,?)", (run_id, actor, canonical(run)))
        return {"run_id": run_id, "status": "draft"}

    def prepare(self, run, action, payload):
        require(isinstance(payload, dict), "payload must be an object")
        data = json.loads(canonical(payload))
        config = run["config"]
        if action == "bootstrap":
            fields(data, ("roles", "source_ref", "creation_limit"))
            strings(data["roles"], "bootstrap roles", True)
            require(set(data["roles"]) <= config["roles"].keys(), "Unknown bootstrap role")
            string(data["source_ref"], "actual user team-creation reference")
            require(type(data["creation_limit"]) is int and 0 <= data["creation_limit"] <= config["limits"]["max_created"],
                    "Bootstrap creation limit exceeds configuration")
        elif action == "authorize":
            fields(data, ("source_ref", "brief", "actions", "repositories", "environments",
                          "review_mode", "review_ref", "creation_limit", "write_scope"))
            string(data["source_ref"], "actual user launch reference")
            string(data["review_ref"], "actual user/delegated plan review reference")
            data["brief"] = artifact(data["brief"], roots(run))
            strings(data["actions"], "authorized actions", True)
            require(set(data["actions"]) <= {r["skill"] for r in config["roles"].values()}, "Unknown authorized action")
            strings(data["repositories"], "authorized repositories", True)
            require(set(data["repositories"]) <= config["repositories"].keys(), "Undeclared authorized repository")
            strings(data["environments"], "authorized environments")
            require(data["review_mode"] in ("user", "delegated"), "Record actual user or delegated review")
            require(type(data["creation_limit"]) is int and 0 <= data["creation_limit"] <= config["limits"]["max_created"],
                    "Creation authority exceeds configured limit")
            require(isinstance(data["write_scope"], dict) and data["write_scope"].keys() == set(data["repositories"]),
                    "Declare authorized relative write roots for every repository")
            for paths in data["write_scope"].values():
                strings(paths, "authorized write roots", True)
                for path in paths:
                    require(not Path(path).is_absolute() and not re.match(r"^[A-Za-z]:", path)
                            and ".." not in re.split(r"[/\\]", path), "Invalid authorized write root")
        elif action == "bind":
            fields(data, ("role", "session", "cwd", "observation_ref"))
            require(data["role"] in config["roles"], "Unknown role")
            data["key"] = session_key(data["session"])
            allowed = {session_key(s) for s in config["roles"][data["role"]]["sessions"]}
            require(data["key"] in allowed, "Binding must appear in the explicit blueprint; created tasks use operation_result")
            data["cwd"] = str(path_at(data["cwd"], config["project_root"]))
            string(data["observation_ref"], "host observation reference")
        elif action == "observe":
            fields(data, ("session", "status", "observation_ref"))
            data["key"] = session_key(data["session"])
            require(data["status"] in ("idle", "active", "needs_input", "unknown", "retired"), "Invalid host observation")
            string(data["observation_ref"], "host observation reference")
        elif action == "admit":
            fields(data, ("jobs", "seal_stages"))
            require(isinstance(data["jobs"], list) and data["jobs"], "Admit a nonempty batch")
            strings(data["seal_stages"], "sealed stages", True)
            for packet in data["jobs"]:
                fields(packet, ("id", "stage", "kind", "task_ids", "requires", "parent", "repositories",
                                "plans", "write_set", "resources", "inputs", "review_ref"))
                label(packet["id"], "assignment ID")
                stage = stage_of(run, packet["stage"])
                role = config["roles"][stage["role"]]
                require(packet["kind"] in ("work", "group", "integrate"), "Invalid assignment kind")
                require(packet["kind"] == "work" or role["skill"] == "m-execute", "Groups/integration use m-execute")
                strings(packet["task_ids"], "Task IDs", True)
                for task in packet["task_ids"]:
                    label(task, "Task ID")
                strings(packet["requires"], "assignment dependencies")
                if packet["parent"] is not None:
                    label(packet["parent"], "parent assignment")
                packet["repositories"] = snapshot(config, packet["repositories"])
                packet["plans"] = plan_check(packet, role["skill"])
                packet["write_set"] = write_set(config, packet["write_set"], packet["repositories"])
                strings(packet["resources"], "shared resources")
                require(isinstance(packet["inputs"], list), "inputs must be artifact references")
                packet["inputs"] = [artifact(r, roots(run, packet["repositories"])) for r in packet["inputs"]]
                string(packet["review_ref"], "assignment/plan review reference")
                packet["_contract"] = phase_contract(role["skill"])
        elif action == "next":
            fields(data, ())
            data["checked_jobs"] = []
            for job in run["jobs"].values():
                if job["status"] == "pending" and job["packet"]["kind"] != "group" and self.ready(run, job):
                    self.check_packet(run, job["packet"])
                    data["checked_jobs"].append(job["packet"]["id"])
        elif action == "result":
            fields(data, ("operation_id", "session", "outcome", "task_ids", "plans", "repositories",
                          "report", "evidence", "review_ref", "failure_signature"))
            data["key"] = session_key(data["session"])
            require(data["outcome"] in ("passed", "failed", "blocked"), "Invalid result outcome")
            strings(data["task_ids"], "result Task IDs", True)
            operation = self.read_operation(data["operation_id"])
            require(operation["run_id"] == run["id"] and operation["kind"] == "dispatch", "Wrong result operation")
            job = run["jobs"][operation["assignment"]]
            role = config["roles"][stage_of(run, job["packet"]["stage"])["role"]]
            require(job["packet"]["_contract"] == phase_contract(role["skill"]),
                    "Phase contract changed before acceptance; review compatibility", "skill_drift")
            data["repositories"] = snapshot(config, data["repositories"], allow_removed=role["skill"] == "m-archive")
            data["report"] = artifact(data["report"], roots(run, data["repositories"]))
            require(isinstance(data["evidence"], list) and data["evidence"], "Result requires verification evidence")
            data["evidence"] = [artifact(r, roots(run, data["repositories"])) for r in data["evidence"]]
            string(data["review_ref"], "coordinator semantic review reference")
            if data["outcome"] != "passed":
                label(data["failure_signature"], "non-progress signature")
            else:
                require(data["failure_signature"] is None, "Passed results have no failure signature")
            # Archive may have removed root plans; the dispatched definition is retained as references.
            if role["skill"] != "m-archive":
                plan_check(job["packet"], role["skill"])
        elif action == "operation_result":
            fields(data, ("operation_id", "outcome", "observation_ref"), ("client_thread_id", "session", "cwd"))
            require(data["outcome"] in ("pending", "delivered", "not_delivered", "uncertain", "ready"), "Invalid operation outcome")
            string(data["observation_ref"], "host outcome reference")
            if "session" in data:
                data["key"] = session_key(data["session"])
                data["cwd"] = str(path_at(data.get("cwd"), config["project_root"]))
            if "client_thread_id" in data:
                label(data["client_thread_id"], "pending creation ID")
        elif action in ("pause", "resume", "finish"):
            fields(data, ())
        elif action == "takeover":
            fields(data, ("job_id", "observation_ref"))
            string(data["observation_ref"], "inactive writer verification reference")
        elif action == "transfer":
            fields(data, ("new_coordinator", "observation_ref"))
            data["new_coordinator"] = session_key(data["new_coordinator"])
            string(data["observation_ref"], "coordinator transfer reference")
        elif action == "invalidate":
            fields(data, ("job_ids", "reason_ref"))
            strings(data["job_ids"], "invalidated jobs", True)
            string(data["reason_ref"], "invalidation review reference")
        elif action == "retry":
            fields(data, ("job_id", "repositories", "plans", "review_ref"))
            require(data["job_id"] in run["jobs"], "Unknown assignment")
            packet = run["jobs"][data["job_id"]]["packet"]
            data["repositories"] = snapshot(config, data["repositories"])
            require(data["repositories"].keys() == packet["repositories"].keys(), "Retry cannot expand repositories")
            phase = config["roles"][stage_of(run, packet["stage"])["role"]]["skill"]
            data["plans"] = plan_check(packet | data, phase)
            string(data["review_ref"], "retry review reference")
        return data

    def read_operation(self, operation_id):
        with closing(self.store.connect()) as db:
            return Store.operation(db, operation_id)

    def check_packet(self, run, packet):
        role = run["config"]["roles"][stage_of(run, packet["stage"])["role"]]
        require(packet["_contract"] == phase_contract(role["skill"]),
                "Original phase contract changed; review compatibility before retrying", "skill_drift")
        snapshot(run["config"], packet["repositories"])
        plan_check(packet, role["skill"])
        for ref in packet["inputs"]:
            artifact(ref, roots(run, packet["repositories"]))
        if role["skill"] == "release":
            artifact(role["procedure_ref"], roots(run, packet["repositories"]))

    def status(self, run, revision):
        with closing(self.store.connect()) as db:
            operations = [dict(row) for row in db.execute(
                "SELECT id,assignment,kind,state FROM operations WHERE run_id=? ORDER BY rowid", (run["id"],))]
            claims = [dict(row) for row in db.execute("SELECT resource,assignment FROM claims WHERE run_id=?", (run["id"],))]
        return {"run_id": run["id"], "status": run["status"], "revision": revision,
                "coordinator": run["coordinator"], "created": run["created"], "bindings": run["bindings"],
                "jobs": {key: {"status": job["status"], "generation": job["generation"],
                                "stage": job["packet"]["stage"], "task_ids": job["packet"]["task_ids"],
                                "operation_id": job.get("operation_id"), "result": job.get("result")}
                         for key, job in run["jobs"].items()}, "operations": operations, "claims": claims}

    def do_authorize(self, db, run, data):
        require(run["status"] == "draft", "Launch authority is immutable after starting; use a new reviewed run for expanded scope")
        run["authority"], run["status"] = data, "ready"
        return {"status": "ready"}

    def do_bootstrap(self, db, run, data):
        require(run["status"] in ("draft", "ready"), "Bootstrap the team before admitting workflow work")
        require(run["setup_authority"] in (None, data), "Setup scope changed; review the definition instead of silently expanding it")
        run["setup_authority"] = data
        outstanding = [Store.operation(db, row[0]) for row in db.execute(
            "SELECT id FROM operations WHERE run_id=? AND kind='create' AND state IN ('intent','pending','uncertain')", (run["id"],))]
        sessions = {s for pool in run["bindings"].values() for s in pool}
        live = sum(json.loads(db.execute("SELECT data FROM sessions WHERE key=?", (s,)).fetchone()[0])["status"] != "retired" for s in sessions)
        for role_id in data["roles"]:
            role = run["config"]["roles"][role_id]
            count = len(run["bindings"].get(role_id, {}))
            pending = [op for op in outstanding if op["data"]["role"] == role_id]
            if count >= role["initial"]:
                continue
            if pending:
                return {"action": "wait", "reason": "creation_pending_or_uncertain", "operation_ids": [op["id"] for op in pending]}
            require(role["create"] is not None, "Bind explicitly configured existing sessions for this role")
            if run["created"] >= data["creation_limit"] or live + len(outstanding) >= run["config"]["limits"]["max_live"]:
                return {"action": "wait", "reason": "creation_capacity_exhausted"}
            target = role["create"]["target"]
            op_id = self.new_operation(db, run, "create", None, {"role": role_id, "target": target})
            run["created"] += 1
            return {"action": "create", "operation_id": op_id, "role": role_id, "target": target}
        return {"action": "ready", "status": run["status"], "launch_authorized": run["authority"] is not None}

    def bind_session(self, db, run, role, key, cwd, observation_ref, created=False):
        old = db.execute("SELECT data FROM sessions WHERE key=?", (key,)).fetchone()
        if old:
            require(json.loads(old[0])["cwd"] == cwd, "Session working directory changed; reconcile instead of rebinding")
        else:
            session = {"cwd": cwd, "status": "unknown", "observation_ref": observation_ref, "completed": 0}
            db.execute("INSERT INTO sessions VALUES (?,?)", (key, canonical(session)))
        binding = run["bindings"].setdefault(role, {})
        binding[key] = {"created": created}

    def do_bind(self, db, run, data):
        self.bind_session(db, run, data["role"], data["key"], data["cwd"], data["observation_ref"])
        return {"status": "bound", "session": data["key"], "observation_required": True}

    def do_observe(self, db, run, data):
        require(any(data["key"] in pool for pool in run["bindings"].values()), "Session is not bound to this run")
        row = db.execute("SELECT data FROM sessions WHERE key=?", (data["key"],)).fetchone()
        session = json.loads(row[0])
        if data["status"] == "retired":
            require(db.execute("SELECT 1 FROM claims WHERE resource=?", ("session:" + data["key"],)).fetchone() is None,
                    "Cannot retire a claimed session")
            require(session["status"] == "idle", "Verify inactive/idle before retiring a session")
        session.update(status=data["status"], observation_ref=data["observation_ref"])
        db.execute("UPDATE sessions SET data=? WHERE key=?", (canonical(session), data["key"]))
        return {"status": "observed", "claims_released": False}

    def authorized(self, run, packet):
        authority = run["authority"]
        require(authority is not None, "Record actual launch authorization first", "authorization_required")
        role = run["config"]["roles"][stage_of(run, packet["stage"])["role"]]
        require(role["skill"] in authority["actions"], "Phase is outside launch authority", "authorization_required")
        require(packet["repositories"].keys() <= set(authority["repositories"]), "Repository is outside launch authority")
        for item in packet["write_set"]:
            allowed = [{"repo": item["repo"], "path": p.replace("\\", "/").rstrip("/") or "."}
                       for p in authority["write_scope"][item["repo"]]]
            require(any(p["path"] == "." or item["path"] == p["path"]
                        or item["path"].startswith(p["path"] + "/") for p in allowed), "Write scope exceeds launch authority")
        if role["skill"] == "release":
            require(role["environment"] in authority["environments"], "Release environment is not authorized")

    def do_admit(self, db, run, data):
        require(run["status"] in ("ready", "running", "waiting"), "Run is not admitting work")
        packets = {p["id"]: p for p in data["jobs"]}
        require(len(packets) == len(data["jobs"]), "Duplicate assignment IDs")
        require(not packets.keys() & run["jobs"].keys(), "Assignment already exists; use retry for failed work")
        all_packets = {key: j["packet"] for key, j in run["jobs"].items()} | packets
        for packet in packets.values():
            self.authorized(run, packet)
            require(packet["stage"] not in run["sealed"], "Stage already sealed; its required set is immutable")
            require(packet["stage"] in data["seal_stages"], "Seal the complete required set with admission")
            require(set(packet["requires"]) <= all_packets.keys() and packet["id"] not in packet["requires"], "Unknown/self dependency")
            if packet["parent"]:
                require(run["config"]["limits"]["max_depth"] == 1, "Execution children are disabled")
                parent = all_packets.get(packet["parent"])
                require(parent and parent["kind"] == "group" and parent["parent"] is None
                        and parent["stage"] == packet["stage"], "Children need a same-stage root group")
                require(set(packet["task_ids"]) <= set(parent["task_ids"]), "Child tasks exceed parent admission")
            if packet["kind"] == "group":
                children = [p for p in packets.values() if p["parent"] == packet["id"]]
                require(children and packet["write_set"] == [] and set(packet["requires"]) == {p["id"] for p in children},
                        "A group only joins its declared children and never writes")
                require(set(packet["task_ids"]) == {t for p in children for t in p["task_ids"]}, "Child tasks must cover the group")
            for other in all_packets.values():
                if other["id"] == packet["id"] or other["stage"] != packet["stage"] or "group" in (other["kind"], packet["kind"]):
                    continue
                require(not set(packet["task_ids"]) & set(other["task_ids"]), "A Task ID has competing writers in this stage")
                require(not overlaps(packet["write_set"], other["write_set"]), "Parallel write sets overlap")
        def visit(key, visiting, done):
            require(key not in visiting, "Assignment dependency cycle")
            if key in done:
                return
            for dependency in all_packets[key]["requires"]:
                visit(dependency, visiting | {key}, done)
            done.add(key)
        completed = set()
        for key in all_packets:
            visit(key, set(), completed)
        for stage_id in data["seal_stages"]:
            stage = stage_of(run, stage_id)
            members = [p for p in packets.values() if p["stage"] == stage_id]
            require(members, "Cannot seal an empty stage")
            require(stage_id not in run["sealed"], "Stage already sealed")
            require(stage["routing"] == "split" or len(members) == 1, "Any/join stages admit one assignment")
            run["sealed"][stage_id] = [p["id"] for p in members]
        for key, packet in packets.items():
            run["jobs"][key] = {"packet": packet, "status": "pending", "generation": 1,
                                "failures": {}, "result": None, "operation_id": None}
        run["status"] = "running"
        return {"status": "admitted", "job_ids": list(packets)}

    def stage_passed(self, run, stage_id):
        return bool(run["sealed"].get(stage_id)) and all(run["jobs"][key]["status"] == "passed" for key in run["sealed"][stage_id])

    def ready(self, run, job):
        packet = job["packet"]
        stage = stage_of(run, packet["stage"])
        return all(self.stage_passed(run, previous) for previous in stage["after"]) and all(
            run["jobs"][key]["status"] == "passed" for key in packet["requires"])

    def join_check(self, run, packet):
        stage = stage_of(run, packet["stage"])
        phase = run["config"]["roles"][stage["role"]]["skill"]
        previous = [run["jobs"][key] for s in stage["after"] for key in run["sealed"].get(s, [])]
        previous += [run["jobs"][key] for key in packet["requires"]]
        previous = [j for j in previous if j["packet"]["kind"] != "group"]
        if packet["kind"] == "integrate":
            require(previous and all(j["status"] == "passed" for j in previous), "Integration needs all required outputs")
            return
        if phase in ("m-test", "m-archive", "release"):
            require(previous, "Validation/closeout requires predecessor evidence")
            expected = {}
            for job in previous:
                require(job["result"] is not None, "Missing predecessor receipt")
                for key, commit in candidates(job["result"]).items():
                    require(key not in expected or expected[key] == commit,
                            "Branches have different candidates; admit explicit integration first", "integration_required")
                    expected[key] = commit
            require(candidates(packet) == expected, "Validate the exact complete integrated candidate", "stale_candidate")
        if phase == "m-continue":
            require(previous and any(run["config"]["roles"][stage_of(run, j["packet"]["stage"])["role"]]["skill"]
                                     in ("m-execute", "m-test") for j in previous), "m-continue needs an existing execute/test pass")

    def new_operation(self, db, run, kind, assignment, data):
        op_id = str(uuid.uuid4())
        db.execute("INSERT INTO operations VALUES (?,?,?,?,?,?)",
                   (op_id, run["id"], assignment, kind, "intent", canonical(data)))
        return op_id

    def do_next(self, db, run, data):
        require(run["status"] in ("ready", "running", "waiting"), "Resume/resolve the run before dispatch")
        reasons = []
        for key, job in run["jobs"].items():
            if job["status"] != "pending" or not self.ready(run, job):
                continue
            packet = job["packet"]
            if packet["kind"] == "group":
                job["status"] = "passed"
                continue
            if key not in data["checked_jobs"]:
                continue
            self.authorized(run, packet)
            self.join_check(run, packet)
            stage = stage_of(run, packet["stage"])
            role_id = stage["role"]
            role = run["config"]["roles"][role_id]
            shared = ["resource:" + r for r in packet["resources"]]
            shared += ["worktree:" + path_key(v["worktree"]) for v in packet["repositories"].values()]
            if role["skill"] in ("m-plan", "m-archive"):
                shared.append("docs:" + path_key(run["config"]["docs_root"]))
            occupied = [db.execute("SELECT run_id,assignment FROM claims WHERE resource=?", (resource,)).fetchone() for resource in shared]
            if any(row is not None and (row[0], row[1]) != (run["id"], key) for row in occupied):
                reasons.append({"job": key, "reason": "shared_resource_busy"})
                continue
            pool = run["bindings"].get(role_id, {})
            eligible = []
            for session_id in pool:
                session = json.loads(db.execute("SELECT data FROM sessions WHERE key=?", (session_id,)).fetchone()[0])
                if session["status"] == "idle" and session["completed"] < run["config"]["limits"]["reuse_after"]:
                    eligible.append((session["completed"], session_id, session))
            for _, session_id, session in sorted(eligible):
                resources = ["session:" + session_id] + shared
                if not Store.claim(db, resources, run["id"], key):
                    continue
                envelope = {"run_id": run["id"], "assignment": key, "generation": job["generation"],
                            "receiver": session_id, "receiver_cwd": session["cwd"], "reply_to": run["coordinator"],
                            "role": role_id, "skill": role["skill"], "contexts": role["contexts"],
                            "project_root": run["config"]["project_root"], "docs_root": run["config"]["docs_root"],
                            "authority_ref": run["authority"]["source_ref"], "review_mode": run["authority"]["review_mode"],
                            "packet": packet}
                if role["skill"] == "release":
                    envelope["release"] = {k: role[k] for k in ("environment", "procedure_ref")}
                op_id = self.new_operation(db, run, "dispatch", key, {"envelope": envelope})
                session["status"] = "unknown"
                db.execute("UPDATE sessions SET data=? WHERE key=?", (canonical(session), session_id))
                job.update(status="reserved", operation_id=op_id)
                run["status"] = "running"
                return {"action": "dispatch", "operation_id": op_id, "envelope": envelope,
                        "instruction": "Recheck host status; load contexts in receiver; send once and record outcome"}
            outstanding = [Store.operation(db, row[0]) for row in db.execute(
                "SELECT id FROM operations WHERE run_id=? AND kind='create' AND state IN ('intent','pending','uncertain')", (run["id"],))]
            if any(op["data"]["role"] == role_id for op in outstanding):
                reasons.append({"job": key, "reason": "creation_pending_or_uncertain"})
                continue
            all_sessions = {s for bindings in run["bindings"].values() for s in bindings}
            live = sum(json.loads(db.execute("SELECT data FROM sessions WHERE key=?", (s,)).fetchone()[0])["status"] != "retired"
                       for s in all_sessions) + len(outstanding)
            limits = run["config"]["limits"]
            if role["create"] and run["created"] < min(limits["max_created"], run["authority"]["creation_limit"]) and live < limits["max_live"]:
                target = role["create"]["target"]
                op_id = self.new_operation(db, run, "create", None, {"role": role_id, "target": target})
                run["created"] += 1
                return {"action": "create", "operation_id": op_id, "role": role_id, "target": target,
                        "instruction": "Create bootstrap-only task; reconcile its real ID/cwd and idle readiness before dispatch"}
            reasons.append({"job": key, "reason": "session_or_resource_busy_or_capacity_exhausted"})
        run["status"] = "waiting"
        return {"action": "wait", "reasons": reasons or [{"reason": "dependencies_or_stage_admission_pending"}],
                "active_operations": [j["operation_id"] for j in run["jobs"].values() if j["status"] in BUSY]}

    def do_operation_result(self, db, run, data):
        op = Store.operation(db, data["operation_id"])
        require(op["run_id"] == run["id"], "Operation belongs to another run")
        if op["state"] in ("completed", "manual", "not_delivered", "ready"):
            previous = op["data"].get("host_receipt")
            require(previous is None or previous == data, "Conflicting duplicate operation receipt", "stale_receipt")
            return {"status": op["state"], "duplicate": True}
        body = op["data"]
        outcome = data["outcome"]
        if op["kind"] == "create":
            require(outcome in ("pending", "uncertain", "not_delivered", "ready"), "Invalid creation receipt")
            if outcome == "pending":
                require("client_thread_id" in data and "session" not in data, "Pending creation needs only client_thread_id")
                require("client_thread_id" not in body or body["client_thread_id"] == data["client_thread_id"], "Creation identity changed")
                body["client_thread_id"] = data["client_thread_id"]
            if outcome == "ready":
                require("key" in data, "Ready creation needs verified real session identity and cwd")
                require(db.execute("SELECT 1 FROM sessions WHERE key=?", (data["key"],)).fetchone() is None,
                        "Creation resolved to an already known session; reconcile the operation")
                self.bind_session(db, run, body["role"], data["key"], data["cwd"], data["observation_ref"], created=True)
        else:
            require(outcome in ("delivered", "not_delivered", "uncertain"), "Invalid dispatch receipt")
            job = run["jobs"][op["assignment"]]
            require(job["operation_id"] == op["id"] and job["generation"] == body["envelope"]["generation"], "Stale dispatch receipt")
            if outcome == "not_delivered":
                require(op["state"] == "intent", "After an ambiguous delivery, use verified result/takeover rather than automatic retry")
                Store.release(db, run["id"], op["assignment"])
                job.update(status="pending", operation_id=None)
            else:
                job["status"] = "dispatched" if outcome == "delivered" else "uncertain"
        body["host_receipt"] = data
        Store.update_operation(db, op, outcome, body)
        return {"status": outcome}

    def do_result(self, db, run, data):
        op = Store.operation(db, data["operation_id"])
        body = op["data"]
        if op["state"] == "completed":
            require(body["result_digest"] == digest(data), "Conflicting duplicate phase result", "stale_receipt")
            return {"status": "accepted", "duplicate": True}
        job = run["jobs"][op["assignment"]]
        envelope = body["envelope"]
        require(job["operation_id"] == op["id"] and job["generation"] == envelope["generation"], "Stale assignment result", "stale_receipt")
        require(data["key"] == envelope["receiver"], "Result does not identify the assigned session")
        require(job["status"] in BUSY | {"manual"}, "Assignment cannot accept a result in its current state")
        if job["status"] != "manual":
            session = json.loads(db.execute("SELECT data FROM sessions WHERE key=?", (data["key"],)).fetchone()[0])
            require(session["status"] == "idle", "Verify the receiver stopped before accepting/releasing its assignment")
        require(set(data["task_ids"]) == set(job["packet"]["task_ids"]), "Result omits or adds admitted Task IDs")
        require(data["plans"] == job["packet"]["plans"], "Result uses another plan definition", "stale_plan")
        require(data["repositories"].keys() == job["packet"]["repositories"].keys(), "Result omits a participating repository")
        for key, item in data["repositories"].items():
            require(item["worktree"] == job["packet"]["repositories"][key]["worktree"], "Result changed the assigned worktree")
        phase = envelope["skill"]
        if phase in ("m-test", "m-archive", "release"):
            require(candidates(data) == candidates(job["packet"]), "Evidence is for another candidate", "stale_candidate")
        require(self.ready(run, job), "Prerequisite was invalidated before result acceptance")
        self.join_check(run, job["packet"])
        job["status"] = "passed" if data["outcome"] == "passed" else "failed"
        job["result"] = {k: v for k, v in data.items() if k not in ("key", "session")}
        if data["failure_signature"]:
            signature = data["failure_signature"]
            job["failures"][signature] = job["failures"].get(signature, 0) + 1
            if job["failures"][signature] >= run["config"]["limits"]["max_nonprogress"] or data["outcome"] == "blocked":
                run["status"] = "needs_input"
        Store.release(db, run["id"], op["assignment"])
        session = json.loads(db.execute("SELECT data FROM sessions WHERE key=?", (data["key"],)).fetchone()[0])
        session["completed"] += 1
        db.execute("UPDATE sessions SET data=? WHERE key=?", (canonical(session), data["key"]))
        body["result_digest"] = digest(data)
        Store.update_operation(db, op, "completed", body)
        return {"status": "accepted", "outcome": data["outcome"]}

    def do_pause(self, db, run, data):
        require(run["status"] not in ("complete", "cancelled"), "Run already ended")
        run["status"] = "paused"
        return {"status": "paused", "claims_released": False, "instruction": "Request safe-boundary stops; reconcile each outstanding assignment"}

    def do_resume(self, db, run, data):
        require(run["status"] in ("paused", "needs_input", "waiting"), "Run is not paused/waiting")
        unresolved = db.execute("SELECT 1 FROM operations WHERE run_id=? AND state IN ('uncertain','intent','pending')", (run["id"],)).fetchone()
        require(unresolved is None, "Reconcile outstanding creation/delivery intents before resuming", "uncertain_operation")
        require(not any(j["status"] == "manual" for j in run["jobs"].values()), "Review manual results before resuming")
        run["status"] = "running"
        return {"status": "running"}

    def do_takeover(self, db, run, data):
        require(run["status"] == "paused", "Pause before manual takeover")
        require(data["job_id"] in run["jobs"], "Unknown assignment")
        job = run["jobs"][data["job_id"]]
        require(job["status"] in BUSY, "Only outstanding assignments need takeover")
        op = Store.operation(db, job["operation_id"])
        key = op["data"]["envelope"]["receiver"]
        session = json.loads(db.execute("SELECT data FROM sessions WHERE key=?", (key,)).fetchone()[0])
        require(session["status"] == "idle", "Old writer must be verified inactive before takeover")
        job["status"] = "manual"
        body = op["data"] | {"takeover_ref": data["observation_ref"]}
        Store.update_operation(db, op, "manual", body)
        # Keep worktree/resource claims until manual evidence is accepted; free only the idle receiver.
        db.execute("DELETE FROM claims WHERE resource=? AND run_id=? AND assignment=?",
                   ("session:" + key, run["id"], data["job_id"]))
        return {"status": "manual", "instruction": "Complete/review manual evidence, then submit result for this same operation"}

    def do_transfer(self, db, run, data):
        require(run["status"] == "paused", "Pause before coordinator transfer")
        run["coordinator"] = data["new_coordinator"]
        db.execute("UPDATE runs SET coordinator=? WHERE id=?", (run["coordinator"], run["id"]))
        return {"status": "transferred", "coordinator": run["coordinator"]}

    def downstream(self, run, seeds):
        affected = set(seeds)
        changed = True
        while changed:
            changed = False
            stages = {run["jobs"][key]["packet"]["stage"] for key in affected}
            for key, job in run["jobs"].items():
                if key not in affected and (set(job["packet"]["requires"]) & affected
                                           or set(stage_of(run, job["packet"]["stage"])["after"]) & stages):
                    affected.add(key)
                    changed = True
        return affected

    def do_invalidate(self, db, run, data):
        require(set(data["job_ids"]) <= run["jobs"].keys(), "Unknown invalidated assignment")
        affected = self.downstream(run, data["job_ids"])
        require(not any(run["jobs"][key]["status"] in BUSY | {"manual"} for key in affected),
                "Pause and reconcile affected writers before invalidating their evidence")
        for key in affected:
            run["jobs"][key]["status"] = "failed"
            run["jobs"][key]["result"] = None
        run["status"] = "paused"
        return {"status": "invalidated", "job_ids": sorted(affected)}

    def do_retry(self, db, run, data):
        job = run["jobs"][data["job_id"]]
        require(job["status"] == "failed", "Retry only verified failed/invalidated work")
        require(max(job["failures"].values(), default=0) < run["config"]["limits"]["max_nonprogress"],
                "Non-progress bound reached; revise the product/plan decision before another run", "nonprogress")
        require(not any(run["jobs"][key]["status"] in BUSY | {"passed", "manual"}
                        for key in self.downstream(run, [data["job_id"]]) - {data["job_id"]}),
                "Invalidate/reconcile downstream evidence before retrying upstream work")
        packet = job["packet"] | {k: data[k] for k in ("repositories", "plans", "review_ref")}
        packet["_contract"] = phase_contract(run["config"]["roles"][stage_of(run, packet["stage"])["role"]]["skill"])
        self.authorized(run, packet)
        job.update(packet=packet, status="pending", generation=job["generation"] + 1, result=None, operation_id=None)
        return {"status": "pending", "generation": job["generation"]}

    def do_finish(self, db, run, data):
        require(all(self.stage_passed(run, s["id"]) for s in run["config"]["stages"]), "Required stages are incomplete")
        require(db.execute("SELECT 1 FROM claims WHERE run_id=?", (run["id"],)).fetchone() is None, "Unreleased claims remain")
        require(db.execute("SELECT 1 FROM operations WHERE run_id=? AND state IN ('intent','pending','uncertain')", (run["id"],)).fetchone() is None,
                "Uncertain/pending external outcomes remain")
        run["status"] = "complete"
        return {"status": "complete"}

"""Create and drive disposable real-host fixtures; host tools are called separately.

Usage: pilot.py init SETTINGS_JSON | pilot.py ROOT action RUN [JSON_PAYLOAD_FILE]
The coordinator supplies reviewed real observations/results; this helper never invents them.
"""

from pathlib import Path
import hashlib
import json
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from support import REPO_ROOT, git, plan_ref, proof, save
from pipeline_lib.store import Store
from pipeline_lib.workflow import Engine


def initialize(settings):
    root = Path(tempfile.mkdtemp(prefix="m-pipeline-host-pilot-")).resolve()
    metadata = {"root": str(root), "actor": settings["actor"], "authority_ref": settings["authority_ref"], "runs": {}}
    for name in ("a", "b"):
        repo, docs, worktrees = root / "projects" / name, root / "docs" / name, root / "worktrees" / name
        repo.mkdir(parents=True)
        worktrees.mkdir(parents=True)
        for section in ("intake", "features", "requirements", "specs", "decisions", "plan", "change", "lessons"):
            directory = docs / section
            directory.mkdir(parents=True)
            (directory / "README.md").write_text(f"# {section}\n\nDisposable pilot documents.\n", encoding="utf-8")
        (docs / "README.md").write_text("# Pilot docs\n\n" + "\n".join(f"- [{p.name}]({p.name}/README.md)" for p in docs.iterdir() if p.is_dir()) + "\n", encoding="utf-8")
        context = docs / "context"
        context.mkdir()
        (context / "pilot.md").write_text("# Pilot context\n\n## Boundaries\nThis is a disposable local fixture. Never access production, credentials, or remotes. Use the exact assigned worktree.\n", encoding="utf-8")
        brief = docs / "intake" / "request.md"
        brief.write_text("# Confirmed fixture brief\n\nCreate alpha.txt containing exactly alpha-ready followed by LF, and beta.txt containing exactly beta-ready followed by LF. Integrate both, verify exact bytes, run the configured local marker procedure, then archive only the assigned integration worktree. No remote effects.\n", encoding="utf-8")
        procedure = docs / "specs" / "release-procedure.md"
        procedure.write_text(f"# Local fixture release\n\nAfter validating both marker files in the tested commit, write only `{docs / 'plan' / 'release-marker.txt'}` with the tested full commit ID followed by LF. Do not change the code worktree or call any deployment service. Verify the marker bytes.\n", encoding="utf-8")
        git(repo, "init", "-b", "main")
        git(repo, "config", "user.name", "Pipeline Host Fixture")
        git(repo, "config", "user.email", "fixture@example.invalid")
        git(repo, "config", "core.autocrlf", "false")
        plan = f"""# Disposable pipeline {name.upper()}

## Scope

This fixture is part of the explicitly approved parent T8 pilot. Parent plan: {REPO_ROOT / 'plan.md'}.
Project/repository: {repo}; docs_root: {docs}; base: main. Dedicated worktrees are under {worktrees}.
Use the exact per-assignment worktree from the coordinator envelope and its root plan. No remote push, credentials or production actions.
The coordinator reviews the fixture plan within T8 authority; do not claim the user personally reviewed a generated revision.

## Tasks

| Task ID | Goal / write set | Acceptance | Rollback |
| --- | --- | --- | --- |
| P1 | Confirm this plan and governed docs using m-plan; preserve Scope and Tasks headings | Clear scope, task IDs, independent A1/B1 writes and evidence | Revert fixture-only plan changes |
| A1 | Create alpha.txt only using m-execute | Exact UTF-8 bytes alpha-ready plus LF | Revert that file |
| B1 | Create beta.txt only using m-execute | Exact UTF-8 bytes beta-ready plus LF | Revert that file |
| I1 | Integrate alpha.txt and beta.txt from both verified child commits into the assigned candidate worktree | Both exact files in one clean commit; no merge into main | Revert integration commit |
| V1 | Use m-test on the exact integrated candidate | Both file byte assertions pass; HEAD unchanged | No code changes |
| R1 | Follow the explicitly configured local release procedure | Durable marker contains the tested full commit plus LF | Remove only the fixture marker if needed |
| C1 | Use m-archive for the assigned integration worktree | Governed archive and local merge/cleanup evidence; retain other pilot worktrees | Retain durable commit and evidence |

Execution scope: P1, A1, B1, I1, V1, R1, C1. No other Task IDs are admitted.
The coordinator owns this plan's progress updates during A1/B1; split receivers write only their assigned marker file and external phase report.
Reports belong under {docs / 'plan'} and must not contain loaded context values. Use m-context local:pilot#Boundaries before phase actions.
All code changes are in disposable branches/worktrees, committed with English messages. Fixture source has no external dependencies.

## Progress

Pending coordinator review and real-host phase evidence.
"""
        (repo / "plan.md").write_text(plan, encoding="utf-8")
        git(repo, "add", ".")
        git(repo, "commit", "-m", "fixture: seed approved pilot scope")
        initial = git(repo, "rev-parse", "HEAD")
        tree = worktrees / "plan"
        git(repo, "worktree", "add", "-b", f"codex/pilot-{name}-plan", str(tree), initial)
        roles = {}
        for role, skill, initial_count in (("architect", "m-plan", 1), ("executor", "m-execute", 2),
                                            ("tester", "m-test", 1), ("closer", "m-archive", 1), ("publisher", "release", 0)):
            roles[role] = {"skill": skill, "contexts": [{"scope": "local", "name": "pilot", "section": "Boundaries"}],
                           "sessions": [], "initial": initial_count,
                           "create": {"target": {"type": "projectless", "directoryName": "pipeline-pilot-" + role}}}
        roles["publisher"].update(environment="fixture", procedure_ref=proof(procedure))
        stages = [{"id": "plan", "role": "architect", "after": [], "routing": "any"},
                  {"id": "execute", "role": "executor", "after": ["plan"], "routing": "split"},
                  {"id": "integrate", "role": "executor", "after": ["execute"], "routing": "join"},
                  {"id": "test", "role": "tester", "after": ["integrate"], "routing": "join"},
                  {"id": "release", "role": "publisher", "after": ["test"], "routing": "any"},
                  {"id": "archive", "role": "closer", "after": ["release"], "routing": "any"}]
        config = {"version": 1, "project_root": str(repo), "docs_root": str(docs),
                  "repositories": {"app": {"path": str(repo), "base_ref": "main", "worktree_root": str(worktrees)}},
                  "roles": roles, "stages": stages,
                  "limits": {"max_live": 6, "max_created": 8, "max_depth": 1, "max_nonprogress": 3, "reuse_after": 10}}
        config_path = root / f"blueprint-{name}.json"
        save(config_path, config)
        metadata["runs"][name] = {"repo": str(repo), "docs": str(docs), "worktrees": str(worktrees), "blueprint": str(config_path)}
    save(root / "pilot.json", metadata)
    return {"root": str(root), "metadata": str(root / "pilot.json")}


def main():
    if sys.argv[1] == "init":
        return initialize(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
    root, action, name = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    metadata = json.loads((root / "pilot.json").read_text(encoding="utf-8"))
    engine = Engine(Store(root / "state"))
    run_id = "host-pilot-" + name
    def call(operation, payload):
        return engine.apply({"action": operation, "run_id": run_id, "actor": metadata["actor"], "payload": payload})
    info = metadata["runs"][name]
    if action == "start":
        return call("init", {"blueprint": info["blueprint"]})
    if action == "launch":
        config = json.loads(Path(info["blueprint"]).read_text(encoding="utf-8"))
        return call("authorize", {"source_ref": metadata["authority_ref"], "brief": proof(Path(info["docs"]) / "intake/request.md"),
                                  "actions": sorted({r["skill"] for r in config["roles"].values()}), "repositories": ["app"],
                                  "environments": ["fixture"], "review_mode": "delegated", "review_ref": metadata["authority_ref"],
                                  "creation_limit": 8, "write_scope": {"app": ["."]}})
    if action == "stage":
        stage = sys.argv[4]
        run, _ = engine.store.read(run_id)
        definitions = {"plan": [("plan", "P1", "work", ["plan.md"])], "execute": [("alpha", "A1", "work", ["alpha.txt"]), ("beta", "B1", "work", ["beta.txt"])],
                       "integrate": [("integrate", "I1", "integrate", ["alpha.txt", "beta.txt"])], "test": [("test", "V1", "work", [])],
                       "release": [("release", "R1", "work", [])], "archive": [("archive", "C1", "work", [])]}
        packets = []
        for job_id, task_id, kind, writes in definitions[stage]:
            if stage == "plan":
                tree = Path(info["worktrees"]) / "plan"
            elif stage in ("execute", "integrate"):
                tree = Path(info["worktrees"]) / job_id
                base = run["jobs"]["plan"]["result"]["repositories"]["app"]["commit"]
                git(info["repo"], "worktree", "add", "-b", f"codex/pilot-{name}-{job_id}", str(tree), base)
            else:
                tree = Path(info["worktrees"]) / "integrate"
            plan = {} if stage == "plan" else {"app": plan_ref({"path": str(tree / "plan.md"), "sections": ["Scope", "Tasks"]}, tree)}
            packet = {"id": job_id, "stage": stage, "kind": kind, "task_ids": [task_id], "requires": [], "parent": None,
                      "repositories": {"app": {"worktree": str(tree), "commit": git(tree, "rev-parse", "HEAD")}}, "plans": plan,
                      "write_set": [{"repo": "app", "path": p} for p in writes], "resources": ["pilot-release-slot"] if stage == "release" else [],
                      "inputs": [proof(Path(info["docs"]) / "intake/request.md")], "review_ref": "parent:reviewed-fixture-plan"}
            packets.append(packet)
        return call("admit", {"jobs": packets, "seal_stages": [stage]})
    if action == "next":
        result = call("next", {})
        if result["action"] in ("dispatch", "create"):
            save(root / (result["operation_id"] + ".json"), result)
        return result
    if action == "share":
        source, _ = engine.store.read("host-pilot-a")
        config = json.loads(Path(info["blueprint"]).read_text(encoding="utf-8"))
        for role, pool in source["bindings"].items():
            config["roles"][role]["sessions"] = [{"host_id": key.split(":", 1)[0], "thread_id": key.split(":", 1)[1]} for key in pool]
        save(info["blueprint"], config)
        return {"updated": info["blueprint"]}
    if action == "accept":
        data = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
        dispatched = json.loads((root / (data["operation_id"] + ".json")).read_text(encoding="utf-8"))
        packet = dispatched["envelope"]["packet"]
        tree = Path(packet["repositories"]["app"]["worktree"])
        commit = data.get("commit") or git(tree, "rev-parse", "HEAD")
        receiver = dispatched["envelope"]["receiver"].split(":", 1)
        report = proof(data["report"])
        return call("result", {"operation_id": data["operation_id"], "session": {"host_id": receiver[0], "thread_id": receiver[1]},
                                "outcome": data["outcome"], "task_ids": packet["task_ids"], "plans": packet["plans"],
                                "repositories": {"app": {"worktree": str(tree), "commit": commit}}, "report": report,
                                "evidence": [proof(p) for p in data["evidence"]], "review_ref": data["review_ref"],
                                "failure_signature": data.get("failure_signature")})
    payload = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8")) if len(sys.argv) > 4 else {}
    return call(action, payload)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(main(), ensure_ascii=False))

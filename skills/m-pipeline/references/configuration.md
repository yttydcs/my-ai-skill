# Configuration And Launch

Copy `assets/pipeline.example.json` beside the project's configuration and replace its paths and task bindings. Paths resolve against that file. Do not put credentials or loaded context bodies in it. A non-Git umbrella may declare several independent Git repositories.

## Blueprint Version 1

Required top-level fields:

- `version`: `1`.
- `project_root`, `docs_root`: existing explicit directories. Resolve/bootstrap governed docs through `m-docs` before validation.
- `repositories`: keys map to `{path, base_ref, worktree_root}`. Each is a real Git repository. Every assignment has an exact dedicated worktree and full commit ID; checkpoint uncommitted progress before handoff.
- `roles`: keys map to `{skill, contexts, sessions, create, initial?}`. `initial` defaults to one. `contexts` contains `{scope: "local"|"global", name, section?}` references. `sessions` contains verified `{host_id, thread_id}` identities; never a pending creation ID. `create` is null or `{target: ...}`.
- Creation target: `{type: "projectless", directoryName: "short-name"}` or `{type: "project", projectId, base_ref}`. Validate saved project IDs with `list_projects`; project targets use worktrees from the explicitly configured ref. Projectless receivers must still use the assignment's verified worktree for code actions.
- `stages`: ordered `{id, role, after: [stage IDs], routing: "any"|"split"|"join"}`. Unknown dependencies/cycles/backward phase edges fail. Repair uses runtime transitions. A split execution stage admits the complete distinct-task set at once. A join admits one integration or validation assignment.
- `limits`: `{max_live, max_created, max_depth, max_nonprogress, reuse_after}`. Depth is zero or one; `max_created` counts all creation attempts, including setup, failed, uncertain and replacement attempts. `reuse_after` limits completed assignments per session before fresh replacement.

Skills: `m-discuss`, `m-plan`, `m-execute`, `m-test`, `m-archive`; explicitly selected composites `m-go`, `m-continue`; or `release` for a configured deployment procedure. A release role also requires `environment` and `procedure_ref: {path, sha256}`. The latter is an existing authorized procedure document, not a shell command inferred by the runtime. Configure its ordering relative to archive according to whether it needs the worktree or a durable artifact.

## Runtime Requests

All mutations use this envelope:

```json
{"action":"init","run_id":"feature-001","actor":{"host_id":"local","thread_id":"ACTUAL-COORDINATOR-ID"},"payload":{"blueprint":"ABSOLUTE-BLUEPRINT-PATH"}}
```

`actor` is the actual coordinator. Keep one state root outside project repositories and governed docs; pass it explicitly or use the resolved `CODEX_HOME/m-pipeline` default. Different stores do not share claims. JSON output is `{ok,result}` or `{ok:false,error:{code,message}}`; exits are 0 success, 2 rejected input/state, 3 environment failure. An error is not evidence that a preceding host call failed.

Actions and payloads:

| Action | Payload |
| --- | --- |
| `init` | `{blueprint: absolute path}`; repeat only with the same run definition and owner |
| `bootstrap` | `{roles: [role IDs], source_ref, creation_limit}`; the reference identifies the user's actual team-creation request |
| `bind` | `{role, session: {host_id,thread_id}, cwd, observation_ref}`; session must be in the blueprint |
| `observe` | `{session, status, observation_ref}`; status is idle/active/needs_input/unknown/retired |
| `authorize` | Launch contract below; immutable once started |
| `status`, `next`, `pause`, `resume`, `finish` | `{}` |

Other transition schemas are in [handoffs](handoffs.md) and [recovery](recovery.md). The runtime reserves an intent; the model uses purpose-built task tools outside its transaction. Do not send the JSON request itself as an instruction to a recipient.

## Launch Contract

The `authorize` payload requires `source_ref`, `brief`, `actions`, `repositories`, `environments`, `review_mode`, `review_ref`, `creation_limit`, `write_scope`.

- `source_ref`: verifiable reference to the real user launch instruction, such as the task and user turn identity. Do not store its secret-bearing body or manufacture a reference.
- `brief`: `{path,sha256}` to the confirmed governed brief.
- `actions`: permitted phase skill names, including `release` only if authorized.
- `repositories`: declared repository keys; `write_scope` maps each to authorized relative roots, such as `["src", "tests", "plan.md"]` or `["."]` when the whole repository is actually in scope.
- `environments`: authorized release environments; empty when deployment is absent.
- `review_mode`: `user` for a personally reviewed plan, or `delegated` only when the launch instruction explicitly delegates in-scope future plan review. `review_ref` points to that actual approval/delegation.
- `creation_limit`: total new-task attempts allowed, bounded by the blueprint. Zero permits reuse only. Setup-created tasks count toward the total.

After product discussion, ask only for missing material launch information. Existing session authorization persists. Scope expansion, an unresolved product choice, or a changed deployment target goes back to the product manager/user. Runtime fields are an audit trail; neither a role message nor `approved: true` grants authority.

# Assignment And Evidence Contracts

Use the request wrapper documented in [configuration](configuration.md). Paths below are absolute unless a field explicitly contains a relative write path. All artifact references are `{path,sha256}`; calculate the actual file hash. Never use a context file as an evidence artifact.

## Fingerprint Existing Plans

`pipeline_runtime.py fingerprint --input <file.json>` accepts `{path,sections:[exact unique Markdown headings]}`. It returns `{path,sections,revision}`. Use the worktree-root `plan.md`/`todo.md` and select all relevant definition sections. Checkboxes are normalized; progress outside those sections can change without invalidation. Missing/ambiguous headings or changed definitions fail. This is a reference to the original plan, not another plan.

## Admit And Seal

`admit` payload: `{jobs:[...],seal_stages:[stage IDs]}`. Each job requires:

```json
{
  "id": "implement-a",
  "stage": "execute",
  "kind": "work",
  "task_ids": ["T1"],
  "requires": [],
  "parent": null,
  "repositories": {"app":{"worktree":"ABSOLUTE-WORKTREE","commit":"FULL-COMMIT-ID"}},
  "plans": {"app":{"path":"ABSOLUTE-ROOT-PLAN","sections":["Scope","T1"],"revision":"ACTUAL-FINGERPRINT"}},
  "write_set": [{"repo":"app","path":"src/feature"}],
  "resources": [],
  "inputs": [{"path":"ABSOLUTE-BRIEF","sha256":"ACTUAL-SHA256"}],
  "review_ref": "ACTUAL-PLAN-REVIEW-REFERENCE"
}
```

`plans` may be empty for discuss/plan; subsequent phases require a plan for every participating repository. The runtime verifies real Git identities, clean worktrees and exact full commit IDs. Report/checkpoint dirty progress before handoff; dirty-state migration is not supported.

`resources` contains explicit globally shared keys for documents, integration targets or release environments. Session, physical worktree, and planning/archive docs-root claims are automatic. Acquisition is all-or-none. Cross-run sharing requires one state store and consistently named resource keys.

Seal a stage's complete expected set in the same admission call. Late additions fail instead of allowing a premature join. `any`/`join` admit one job; `split` admits distinct nonoverlapping work. Prefer dependencies between stages. `requires` adds exact assignment dependencies and cannot cycle.

One-level children use a same-stage root `kind:"group"` with no writes. Its `task_ids` equal the union of declared child Task IDs; `requires` is exactly its children's job IDs. Children have `parent:<group ID>` and no deeper group parent. Admit the group and all children together. The coordinator may derive this split from the approved plan before sealing; an executor requests subdivision through the coordinator rather than independently spawning an untracked team.

`kind:"integrate"` is a separate planned `m-execute` join stage with one owner. It consumes all required outputs, assembles them into a candidate branch/worktree and records a new exact commit. This is not a release merge into the base branch. Test/archive/release require the complete exact predecessor candidate; differing branch commits require integration first.

## Result Review

After the receiver stops, inspect its original phase report, tests and actual artifact state. `result` requires:

- `operation_id`: the dispatched operation.
- `session`: assigned `{host_id,thread_id}`; identifies the surrendered assignment even for a manually completed takeover.
- `outcome`: `passed`, `failed` or `blocked`.
- `task_ids`, `plans`: the same admitted set and plan references.
- `repositories`: final exact worktrees/commits. Execute/plan may produce new commits; test/archive/release evidence must refer to the dispatched candidate. Archive may have removed its worktrees, but commits must still resolve in declared repositories.
- `report`: original phase report artifact reference.
- `evidence`: nonempty array of verified artifact references.
- `review_ref`: actual coordinator semantic review reference. The runtime checks structural identity, not the correctness of a test or truth of an assertion.
- `failure_signature`: null for passed, otherwise a stable short code identifying the actionable blocker/non-progress. Do not include secrets or arbitrary log bodies.

Accepting a valid result persists it before releasing claims. Duplicate matching results are harmless; conflicting or stale results fail. An old matching result can be acknowledged without changing a newer retry's state. Context/phase errors become blocked evidence, never a successful no-op.

`finish` succeeds only after all configured stages have sealed and passed, and no claims or uncertain creation/delivery remain. Preserve archive paths and durable commits before cleanup makes worktree references unavailable.

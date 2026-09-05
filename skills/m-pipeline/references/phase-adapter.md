# Original Phase Adapters

Read the actual named skill at `<envelope.skills_root>/<skill>/SKILL.md` and its required references at stage entry. This is the same original skill family adjacent to the companion, not a vendored copy. Use its adjacent `m-context` loader as well. Runtime admission records a hash of those phase/shared files and rejects drift; review changed contracts before refreshing an affected assignment. For older envelopes without a root, verify that the source and invoked installed phase versions agree before acceptance.

| Role | Invocation and acceptance |
| --- | --- |
| Product manager | `m-discuss`; establish the brief and resolve product decisions. A discussion can occur before the runtime launch. |
| Architect | `m-plan`; keep its worktree-root plans, Task IDs, acceptance criteria and `m-docs` invocation. Record actual user approval or bounded delegated review truthfully. |
| Executor | `m-execute`; only admitted Task IDs/write sets in the exact worktree(s), original lightweight validation and reporting. |
| Tester | `m-test`; evaluate the complete integrated candidate using original acceptance/evidence rules. |
| Release owner | `m-archive`; preserve its docs/merge/cleanup behavior. A separate `release` assignment runs only the configured authorized procedure. |

## Receiver Protocol

1. Confirm the operation/run/assignment/generation, phase, result destination and actual launch authority. Read the exact root plan and its assigned Task IDs. The coordinator's admission does not authorize extra tasks.
2. Announce and co-invoke `m-context` for each envelope context. Use the existing loader with exact scope/name/section and explicit docs root. Finish every required load before phase actions. If loading fails, report blocked with metadata only; do not guess values, bypass the loader, or retry in another scope.
3. Use the envelope's absolute worktree as the shell working directory, even if the host task's default cwd differs. Verify repository identity and candidate. Do not switch to the main checkout or assume task creation inherited the intended branch.
4. Invoke the actual phase skill. Its worktree, document, subagent and approval rules apply. An independent role session is not an exception to in-phase delegation limits. A group assignment is a coordination record; only its bounded children invoke execution.
5. Return the original phase report, changed files, Task IDs, validation, risks and exact final commit identities. Include an outer receipt linking those artifacts. Do not mark a completed turn or self-written receipt as overall acceptance.

The coordinator reads and verifies the report, observes that the writer stopped, then submits `result`. Recipients do not mutate coordination state or send unrequested messages to other parties. Cross-task coordination uses only the authorized workflow tasks.

## Documentation Ownership

`m-context` is a companion load before the phase. `m-plan` and `m-archive` retain their own explicit `m-docs` calls. The outer coordinator calls `m-docs` only for setup-owned/stable documents it changes. Do not wrap every phase in duplicate documentation passes.

Plans and stable docs are canonical; the database contains references and receipts. Keep context data in its existing user-controlled location. Do not copy it into configuration, plans, receipts, logs, screenshots, fixtures or commits. Assign an explicit shared resource key for any stable document writer beyond the automatically serialized planning/archive docs work.

For plan fingerprints, select all sections that define scope, assigned Task IDs, write sets, acceptance and constraints. Exclude progress-only sections. The runtime normalizes checklist completion markers, but does not infer whether omitted sections contain requirements. The architect/coordinator must review that selection against the entire original plan.

## Composite And Feedback Ownership

Choose the ordinary execute/test stages by default. If the user explicitly selects `m-go` or `m-continue`, let that composite own the internal loop and wait for its result. Do not attach a second outer test loop. `m-continue` still requires evidence of an existing execute/test pass.

Failed tests return to the owning admitted execution task; invalidate affected downstream evidence, review refreshed candidate/plan fingerprints, retry, and resume. Ordinary in-scope repair does not need repeated continuation approval. Repeated identical non-progress reaches the configured bound and returns an actionable decision to the product manager/user.

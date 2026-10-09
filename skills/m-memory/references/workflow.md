# Workflow write boundaries

Use this adapter only when the project deliberately selects the service as its memory authority. Read libraries, write target, permitted source libraries, retrieval method and budget come from user/project choices; a personal preference library is independent of a project library. Do not infer permission to write one from permission to read another. The m-* storage routing selects this adapter only for bound projects.

| Phase | Read when needed | Durable write boundary |
|---|---|---|
| m-discuss | Current requirements, constraints and explicitly selected preferences | A confirmed requirement or decision that should survive the session; unresolved discussion remains local unless deliberately retained as source material. |
| m-plan | Relevant current requirements/specs and their summaries | A confirmed lasting design change, if any. Keep the execution plan, todo list and task ordering local. |
| m-execute / m-quick | The affected contract and spec; exact source sections when summaries are insufficient | Consolidate a lasting information change at the phase's documentation boundary. Tool calls, retries, temporary hypotheses and progress do not trigger knowledge writes. |
| m-test | Acceptance requirements and the exact evidence needed | A reusable verified finding or corrected durable constraint; routine test logs/results are local evidence, not automatic memory objects. |
| m-continue / m-go | Resume from local workflow state, reading current memory only for relevant changed constraints | Reuse the underlying phase boundary. Another iteration does not itself authorize another knowledge write. |
| m-archive | Current affected documents and final validated effects | Commit actual durable changes once, with CAS and an explicit lease guard when coordinating archival writes; see [archive](m-archive.md). |

Classify impact before composing a commit. A bug fix that restores the existing requirement does not revise that requirement or regenerate its summary. If a technical contract changed, update the affected spec and its summary. A confirmed behavior change can update the requirement and the summaries that actually depend on it. No changed durable information means no knowledge commit, including no empty or identical commit submitted merely to announce completion.

The local agent may write or manually improve a summary using its broader context. Every durable claim still needs an explicit source; first persist a newly confirmed fact as source material, then bind the summary to the source revision. Read the current summary before editing, preserve valuable manual changes and use CAS. A delayed producer computed from old content cannot overwrite a newer manual edit or attach its old output to a newer source revision. Re-read and reconcile on conflict.

Use the atomic ordering and dependency rules in [m-docs](m-docs.md). Read trace, references or history only when a question calls for provenance; do not preload all fix records. Index maintenance, embeddings and summaries are separate explicit actions, not side effects of ordinary search. A disconnected service makes the memory operation unavailable; keep only local execution state, without creating a replacement knowledge store.

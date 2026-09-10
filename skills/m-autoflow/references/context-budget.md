# Context and Output Reuse

Applies to reads and reports across m-* phases, including direct phase entry. It does not waive phase gates, required checks, or project-specific formats.

- Read the selected skill and references needed for the current action, not the whole collection. A reference list is a routing map, not a preload checklist. For a large reference, locate its relevant section first; include surrounding constraints.
- Reuse instructions and project-doc content already read in this task when the content is unchanged and still available in context. Phase changes and explicit skill invocations do not require rereading unchanged files. Recheck only changed or uncertain sources. After compaction or a handoff, reload missing operative constraints; a remembered filename is not the instructions.
- Keep the confirmed docs root, relevant source paths, scope/AC definitions and evidence location in the existing plan or handoff. Do not create a separate reading ledger or copy skill text there. Reuse docs routing; inspect affected leaf docs and indexes when their inputs change.
- Batch independent reads, search before opening large files, and bound log output to the relevant failure or result. Keep full logs as artifacts. Truncated output is incomplete evidence: narrow the next read instead of repeating the same oversized request.
- Maintain one authoritative acceptance/evidence record under `review.md`. Later phases link it and update affected rows. Do not reproduce complete test logs, acceptance maps or unchanged task tables in every phase report.
- User-facing updates describe changes, findings and next decisions. On unchanged approval/status transitions, reference the already-presented plan/table and exact Task IDs rather than printing it again. Reissue the table when scope changes or the prior table is unavailable.
- For a running build/test/deployment, prefer completion events or a bounded tool wait over repeated model-driven status queries. Retain the job ID and last state; return concise changes or terminal results. Respect tool wait limits and required progress communication. Do not create recurring automations or background monitors without user authorization.

These rules reduce repeated context and output, not verification quality. Freshness of mutable source, candidate, dependencies and acceptance still follows `review.md`; never treat stale evidence as a pass.

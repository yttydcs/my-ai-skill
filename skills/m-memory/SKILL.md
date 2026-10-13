---
name: m-memory
description: Read and write private agent information through the configured Agent Memory service. Use for service-backed project or personal libraries, current source and summaries, explicit provenance or history lookup, and short-lived locks; do not use for local plans or unrequested migration.
---

# m:memory

Agent Memory is the only authority for information deliberately moved into a configured library. The user or project configuration chooses the read libraries, write target, permitted source libraries and search method. Never infer a universal project library from a directory name or search every available library by default.

Resolve the project's explicit binding first; read [binding and client](references/binding.md) when configuring a project or invoking the client. Use `scripts/memory_client.py --binding <path>` for bounded search, reads and CAS commits. It requires only Python's standard library. Installed m-docs, m-context and m-archive select this path when the project declares a service binding; unbound projects retain their existing file authority. If the service is unavailable, fail explicitly without switching to local docs, inventing a summary, bypassing TLS or following redirects with credentials.

For routine work, select the task's knowledge category before searching; avoid mixing current contracts with all historical records. Use short domain keywords for lexical retrieval, preserving identifiers and adding the corpus language when needed. Start with a few candidates, then read the exact object or section needed. Follow the [retrieval strategy](references/retrieval.md#task-directed-lexical-retrieval) when choosing scope, reformulating a query or changing methods. Source documents and editable summaries remain separate; dependencies and history are read only when needed. Check the status, revision and reported method before relying on a result.

For evidence sufficiency, citations, section retrieval or client-produced embeddings, read [retrieval](references/retrieval.md). A relevant first snippet is not the whole current contract: check decision-relevant conditions, exceptions and later amendments within the selected source before implementing or asserting its rule. Query failures, partial vector coverage and empty results have different meanings; use only an explicitly chosen alternative. Similarity scores are rankings, not confidence that a question is answerable.

Write only when a durable fact, requirement, design decision, approved preference or stable summary actually changes. Do not save local `plan.md`, task chatter, tool traces or every intermediate step. On a durable change, read the current revision, include the expected revision and a fresh idempotency key, and submit related source and summary changes in one commit when possible. A 409 requires rereading and reconciling; never overwrite by retrying with an invented revision. Agent edits to a summary follow the same dependency checks as generated summaries.

The service exposes generic state and fenced leases. A workflow skill may use a lease for its own concurrent write protocol, but the memory service does not decide whether a task or archive is complete. A lease does not bypass content revision checks.

An `audit_completion_unavailable` error with `operation_may_have_committed: true` is an uncertain outcome. Keep the audit ID and inspect current state; where the endpoint has a still-live idempotency receipt, replay only the identical original request/key. Do not create a fresh key or infer rollback. A pending audit event is not proof of either success or failure. Leave audit configuration/capacity changes to an explicitly authorized owner operation; do not weaken retention or delete information merely to make a write succeed.

If a write returns `storage_quota_exceeded`, it has not partially published. The owner can inspect per-library metrics, adjust an explicit capacity policy, or deliberately remove unneeded data. Do not silently discard source material, formal summaries or history to fit. A routine query does not authorize building indexes or generating embeddings.

For an `object_identity_bytes` limit, deleted object IDs still count. Deleting content or pruning history will not make room for a new identity, and restoring retained history uses the same identity with a fresh revision. Inspect the configured limit and usage; only an explicitly authorized owner policy change can increase that capacity. Do not purge tombstones, recreate old IDs or remove the policy as an automatic retry.

Existing local materials are not migrated automatically. Credentials, production content and benchmark private cases stay outside the code repository. Read the relevant adapter only when applying the corresponding workflow:

- [m-docs adapter](references/m-docs.md) for governed project documentation.
- [m-context adapter](references/m-context.md) for explicitly selected reusable context.
- [m-archive adapter](references/m-archive.md) for closeout writes.
- [Workflow write boundaries](references/workflow.md) for discuss, plan, execute, test, quick and continuation phases.

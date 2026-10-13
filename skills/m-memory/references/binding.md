# Project binding and client

Select one binding once in the project's AGENTS.md (an absolute path, or a path resolved relative to that declared project root). Carry that path across its worktrees explicitly. Alternatively set `M_MEMORY_BINDING` for the current project process, not globally across unrelated projects. `--binding` / `--memory-binding` override that environment setting. Do not discover bindings by walking parents or selecting the first reachable library.

The binding stores connection and scope configuration only, not knowledge. Each device uses its own token file and trusted public CA. Relative file paths resolve relative to the binding file. Keep credentials and machine-specific bindings out of pushable repositories.

```json
{
  "version": 1,
  "backend": "agent-memory",
  "url": "https://memory.example:8443",
  "token_file": "device-token",
  "ca_file": "root.crt",
  "read_libraries": ["PROJECT_LIBRARY_UUID"],
  "write_library": "PROJECT_LIBRARY_UUID",
  "allowed_source_libraries": ["PROJECT_LIBRARY_UUID"],
  "budget_bytes": 8192,
  "indexes": {
    "PROJECT_LIBRARY_UUID": {
      "id": "INDEX_UUID", "revision": "INDEX_REVISION_UUID", "method": "bm25"
    }
  },
  "context_libraries": {"local": "PROJECT_LIBRARY_UUID"}
}
```

Choose actual UUIDs from the owner's selected libraries and index configuration. `write_library` may be null for read-only use. Multiple read libraries require explicit `--library`; there is no automatic all-library search or ranking/precedence. Context scope mappings must belong to the selected read libraries. A separate binding can select a personal library as the write target. Selecting global scope does not authorize writes to a read-only preference library.

The standalone helper requires Python 3.10+ and only its standard library:

```text
python <m-memory>/scripts/memory_client.py --binding <binding.json> check
python <m-memory>/scripts/memory_client.py --binding <binding.json> capabilities
python <m-memory>/scripts/memory_client.py --binding <binding.json> search "export timeout" --category requirements
python <m-memory>/scripts/memory_client.py --binding <binding.json> search "EXPORT_TIMEOUT" --category specs --method fts --limit 3
python <m-memory>/scripts/memory_client.py --binding <binding.json> read <object-uuid> --revision <observed-revision>
python <m-memory>/scripts/memory_client.py --binding <binding.json> commit
```

`commit` reads a JSON bundle from stdin. Keep the exact request and idempotency key in the active session for uncertain-result reconciliation; do not save a permanent local knowledge replica. The local Agent authors source/summary content and provides CAS revisions. The helper does not generate summaries, decide when to write, or automatically retry. Use `commit --archive` for closeout commits; it requires an explicit lease guard.

```json
{
  "idempotency_key": "unique-logical-write-key",
  "operations": [
    {"action": "patch", "object_id": "SOURCE_UUID", "expected_revision": "READ_SOURCE_REVISION", "content": "Updated requirement"},
    {"action": "patch", "object_id": "SUMMARY_UUID", "expected_revision": "READ_SUMMARY_REVISION", "content": "Updated summary", "dependencies": [{"source_library_id": "PROJECT_LIBRARY_UUID", "source_object_id": "SOURCE_UUID"}]}
  ]
}
```

New source creation uses `action:create`, a client UUID, `kind:source`, title, content and metadata such as `{"category":"specs"}`. New summaries use `kind:derived` and explicit dependencies. No current-document update solely because a fix finished. Indexes are separately configured maintenance, not side effects of search.

`capabilities` reads only `/v1/capabilities` on the bound origin with the same credential, TLS, no-redirect and response-budget protections. It does not enumerate libraries or change selected scope. Use it when a retrieval feature requires advertised protocol support; `check` remains selected-library index discovery.

For bounded source sections, provenance, history and leases use the JSON `request` command with a library-relative suffix. It cannot select a different service origin:

```text
... request GET objects/<object-uuid>/trace --query depth=1
... request GET objects/<object-uuid>/references --query direction=outgoing
... request GET section-indexes/<index-uuid>/objects/<object-uuid> --query expected_revision=<revision> --query offset=0 --query limit=3
... request POST locks/archive/acquire --body-stdin
```

Supply the server's lease TTL payload, then include its token/fence/name in each protected commit; renew/release via the documented runtime API. Do not remove the guard after a failure. `request --body-stdin` accepts full search payloads for advanced strategies. `search` uses the binding's method by default; `--method` explicitly selects a method for this call without changing the binding, index, scope or byte budget. All five section/document methods are supported, but their required vectors/model fields and server capabilities must already be satisfied; the client never generates embeddings or falls back. `--limit` bounds candidates from 1 to 50; a conflicting limit in stdin is rejected. `search --body-stdin` accepts extra fields such as metadata filters, caller-computed vectors and object_revisions; it cannot override method, index revision, query or target. The API's method/profile/coverage validation remains authoritative.

The client enforces configured library/source/response-budget boundaries, disables proxy environment inheritance and redirects, verifies TLS, and never caches knowledge. An oversized response fails explicitly; narrow the read to sections or deliberately change the configured budget. A failed or lost write response can have committed: inspect current state/receipt or replay the identical still-live idempotency key, never blindly issue a fresh key. For attachments use the existing `agent-memory request --binary-file/--output` transport with the same explicit binding URL/CA/device and selected library; do not use downloaded attachments as a text knowledge mirror.

## Named contexts

With a service binding, m-context chooses only the requested local/global mapping. `auto` selects local when configured, otherwise global; missing context, section, TLS, or authorization errors do not fall through to another library or to files. Listing/find return one bounded page; continue only when needed using the reported offset.

Store a context as a source object with ID `uuid5(UUID(library_id), "m-context:" + exact_name)`, title `context:<exact_name>`, and metadata `{"category":"context","name":"<exact_name>"}`. Use m-context's name validation and exact casing; `#section` remains a read selector. Deterministic identity avoids duplicate named contexts across devices; create collisions and updates still require normal CAS reconciliation. Agent saves/edits using the generic commit operation, reading existing content/revision first and preserving unrelated sections. Ordinary specs use their own durable IDs, not this naming convention.

The service has no field-level secret exclusion from generated text indexes. Existing credential-bearing contexts stay at their existing authority until the user explicitly accepts migration/storage/indexing scope; no automatic import.

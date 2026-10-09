# Migration helper and verification

The companion m-memory package must be installed beside this skill. The helper uses Python 3.10+ standard library and its cache-free client. No service SDK, model or database driver is required.

## Preview and selection

When no target binding exists yet, first run `python <m-memory-migrate>/scripts/migrate.py scan --root <exact-docs-root> --manifest <private-inventory.json>`. It makes no network request and requires no credentials. This inventory is not an import manifest: after choosing the target, create a separate bound manifest with `preview` below. Do not substitute a placeholder UUID or create a service library merely to satisfy a preview-only request.

```text
python <m-memory-migrate>/scripts/migrate.py preview --root <exact-docs-root> --binding <binding.json> --collection <stable-project-label> --manifest <private-manifest.json>
```

Keep the manifest and journal outside the source root and any pushable code repository. They contain paths, hashes, IDs, categories, sizes and progress, not Markdown bodies or tokens. Existing output files are not overwritten. The collection label plus normalized relative path forms a stable UUIDv5 identity under the destination library; keep the collection name stable across retries/devices. A fresh manifest for already imported paths does not authorize replacing their objects.

Review `entries` and set `selected: true` only for agreed source files; edit category/title if needed. Categories are intake/features/requirements/specs/decisions/lessons/change. Generic README/navigation documents may be kept as source when useful, but they do not replace current requirements or service retrieval. The helper excludes known transient, context and hidden directories and reports them by name without reading their bodies. Non-Markdown files are recorded as deferred, not discarded. It does not identify every secret, detect summary semantics, split oversized files, parse PDF/Word or import attachments.

The manifest binds the source root, service origin and library, without storing the device token. It also records an inventory of all eligible Markdown paths/hashes; a file being added, removed or modified makes the manifest stale before apply/verify, even if it was unselected. Re-preview and review deliberately; do not edit hashes to disguise changes after an import began. Every source must be UTF-8 and fit the service's one-MiB text limit. Larger documents need an explicit logical split with stable section IDs and retained source mapping before migration.

## Import and resume

```text
python <m-memory-migrate>/scripts/migrate.py apply --manifest <private-manifest.json> --binding <binding.json> --journal <private-journal.json>
python <m-memory-migrate>/scripts/migrate.py verify --manifest <private-manifest.json> --binding <binding.json> --journal <private-journal.json>
```

`apply` is the explicit mutation command. It freezes the reviewed manifest digest in the journal, preflights the complete inventory and submits one source per atomic create commit. Each source has metadata category and migration collection/path/hash. The journal stores its exact deterministic idempotency key before sending; bodies are reread from the still-matching source, not duplicated locally. Journal updates use atomic file replacement. Do not run two processes against one journal concurrently; separate devices have separate local journals, while deterministic object IDs prevent duplicate imports and server CAS rejects conflicting creates.

After interruption, reuse the same manifest/journal. A pending request checks its commit receipt first; when no receipt exists it retries the identical create/key. Existing objects or expired ambiguous receipts produce an explicit conflict rather than a guessed overwrite. Completed entries are reread in bounded UTF-8 chunks and must still match their recorded revision and exact SHA-256. A remote edit, delete or mixed-revision read stops verification. Neither an available receipt nor an imported count alone is proof that the present content is intact.

`verify` reads all selected objects, checks revisions and hashes, then repeats local inventory validation. An existing matching journal first returns to `in_progress`, so a failed recheck does not leave its previous success status active. Its `sources_verified` status covers initial imported source content only. After authorized enrichment modifies object revisions, retain the initial import report as phase evidence and separately verify the new content, CAS results and relationships; do not rewrite the original receipt journal to pretend the old revision is current.

## Information layer

- **References:** Resolve relative Markdown links against each source path and the manifest's IDs. Leave the exact source body intact; add typed `references` with target library/object/revision and optional heading span using CAS. Preserve existing references on an update. External URLs remain external; missing or excluded targets remain explicit unresolved items. Do not create extra documents just to make a broken link disappear. A reference is navigation, not a required summary dependency.
- **Summaries:** Existing summaries require inspection of their actual sources and source revisions. Generate missing summaries with the local Agent only where useful, and keep valuable manual edits. Persist a `derived` object with explicit dependencies. Imported raw notes are evidence, not automatically a complete requirements document. Conflicting documents need a declared resolution rather than an invented consolidated truth.
- **Attachments:** Use the existing `agent-memory request` binary transport described by m-memory. Bind each file to its source object's current revision, supply an idempotency key, upload with `--binary-file`, and verify server size/SHA-256 against the source file. Download and hash in a temporary validation location when byte round-trip evidence is required, then remove that test copy. Attachments change the owning object's revision: finish them before generating dependent summaries and final reference anchors. The current service limit is 16 MiB per attachment; report larger files as blocked rather than silently omitting or parsing them. The helper's deferred list must be reconciled before claiming a full migration.
- **Named context:** Ordinary approved context uses m-context's UUIDv5 naming and category convention, not this helper's generic document IDs. Migrate it separately through explicit commits and test named/section loading. Do not use general full-text indexing as if it provided secret-field exclusion.

Keep an explicit disposition for each selected object's references, summary and attachments: complete, unnecessary with reason, or pending. A local migration report may store object IDs, hashes and these statuses but no replacement knowledge corpus. Prepare and test the chosen index separately, since migration does not grant permission to select a semantic encoder or invoke a model.

## Cutover

Use the existing service binding format. Record the completed mapping and validation identities before switching AGENTS; a mere binding change never imports files. Recheck local changes and remote revisions at the cutover boundary, reconcile any delta, and ensure other devices stop editing the old source. Do not delete unselected material or use a recursive docs-directory deletion when that directory also contains local plans, credentials, attachments or deferred files. Removing tracked files and rewriting Git history are separate operations with different scopes.

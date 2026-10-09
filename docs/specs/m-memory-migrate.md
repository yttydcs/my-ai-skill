# Memory migration contract

The package consists of SKILL.md, a conditional migration reference, UI metadata and a standard-library `scripts/migrate.py` helper. It loads the sibling m-memory client; no service-side project or migration engine is introduced.

`scan` inventories an explicit source root before a target binding exists. It uses no credentials or network and emits an inventory-only file, which cannot be applied as an import manifest.

`preview` takes root, binding, collection and a new manifest path. Entries start unselected. The manifest fixes the origin, write library, inventory and deterministic IDs, using UUIDv5 under the library UUID over the compact JSON array `["migrate", collection, relative_path]`. Excluded folders and deferred non-Markdown paths remain visible in the inventory report. Source bodies are never stored in the manifest.

`apply` preflights the entire inventory and selected UTF-8 payloads, freezes the manifest hash in a separate journal, then records a deterministic idempotency key before each create commit. Receipt reconciliation recovers uncertain successful requests. A collision or expired ambiguous result fails rather than adopting or updating the existing object. Journal writes use file replacement; a journal belongs to one active process. The server's idempotency and object identity constraints still protect cross-device races.

`verify` walks current content through the service chunk API, checking revision, offsets, total bytes, progress and SHA-256. It rechecks local inventory after the remote walk. The successful status is `sources_verified`, with information-layer/cutover obligations still explicit. After authorized attachment or reference enrichment changes revisions, preserve this initial phase evidence and independently validate the new revision; do not falsify the old journal.

See [the skill's maintained command contract](../../skills/m-memory-migrate/references/migration.md) for information-layer and cutover procedures, and [requirements](../requirements/m-memory-migrate.md) for acceptance.

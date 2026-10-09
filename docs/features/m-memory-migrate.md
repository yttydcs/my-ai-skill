# Project memory migration

Invoke `$m-memory-migrate` with a source docs directory and selected target library/binding. A preview lists candidates, excluded paths and deferred non-Markdown files; it reads no remote knowledge and uploads nothing. The Agent selects the already authorized scope or resolves missing scope before importing.

The helper imports selected UTF-8 Markdown sources with stable object IDs and a metadata-only progress journal. Interrupted imports resume through commit receipts; local changes, existing object collisions and newer remote revisions stop the operation. Source bytes and revisions are verified through bounded reads, including empty and multi-byte text. Original files remain untouched.

The Agent then handles required references, editable summaries and opaque attachments through existing memory APIs. Those steps and project authority cutover have explicit statuses; source-import success alone never means the whole project migrated. Local plans and execution logs are excluded, existing credential contexts are not automatically imported, and there is no knowledge cache or offline fallback.

See [requirements](../requirements/m-memory-migrate.md), [technical contract](../specs/m-memory-migrate.md) and [skill](../../skills/m-memory-migrate/SKILL.md).

# Memory migration requirements

Provide a reusable migration skill so selected existing project knowledge can become service-authoritative without losing source content or requiring repeated manual API construction.

- M1: Preview an explicit root and library without service mutations; report deferred/excluded material and require explicit file selection.
- M2: Preserve imported source UTF-8 bytes and source-path identity; do not automatically upload local plans, logs or credentials.
- M3: Resume a frozen migration without duplicate objects; never overwrite an existing object merely because its path matches.
- M4: Verify current remote revision and complete source hash; stop on local drift, remote edits, corruption, missing data or nonadvancing pagination.
- M5: Keep only paths, IDs, hashes and receipts in local migration metadata. Summaries, references and attachments need explicit disposition before declaring full migration.
- M6: Switch authority only after fresh verification and within user-approved scope; no automatic deletion, Git-history rewrite, backup selection or local knowledge fallback.

The initial helper supports Markdown source import. It does not claim automatic interpretation of requirements, automatic attachment migration or autonomous summary generation. The Agent orchestrates those information-layer steps with the existing service contracts. See [specification](../specs/m-memory-migrate.md).

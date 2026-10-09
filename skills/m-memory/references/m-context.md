# m-context with Agent Memory

Preserve the caller's explicit local, global or named-context choice. Map each chosen scope to a user-configured library; never search personal and project libraries together just because both are accessible. Resolve exact context identities and optional sections before reading full content. Discovery returns short metadata; a named load returns the requested body.

Plaintext credentials may be intentionally readable to the Agent, but they must not become ordinary full-text or vector index input without an explicit user choice. Existing m-context files, including secrets, are not migrated by this adapter. If an existing local context remains authoritative, continue its current loader until the user selects a service-backed replacement.

The current service does not provide field-level secret exclusion from its shared generated text indexes. Disabling a library's query method is not a guarantee that text was never indexed physically. Do not move credential-bearing context into this service under an assumption of such exclusion; the user must explicitly accept the storage/indexing boundary or use a separate credential store. Ordinary project facts and preferences can use the normal selected-library path.

Save or edit only the requested named context with current revision checking. Do not replicate loaded secrets into plans, benchmark reports, archives or routine final answers.

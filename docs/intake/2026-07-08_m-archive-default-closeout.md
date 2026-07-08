# 2026-07-08_m-archive-default-closeout

## Source

- Source: Codex chat
- Date: 2026-07-08
- Requester: user

## Original Request Evidence

The user clarified that the previous `$m-archive` response was wrong because `$m-archive` should already imply workflow end:

> `m:archive` 理论上这个指令已经暗含了要结束workflow了，理论上和结束workflow是等价的

## Context

The previous workflow completed archive and then asked the user to reply "是" before merge and worktree cleanup. The user corrected the intended command semantics: archive should mean archive plus closeout, not archive plus a second confirmation prompt.

## Interpreted Requirement

- Normal `$m-archive` invocation means archive and end workflow.
- `$m-archive` should not ask a second "whether to end workflow" question after archive completion.
- Archive-only behavior remains possible only when the user explicitly asks not to merge, not to clean up, or to pause after archive.
- Safety checks remain required before merge and worktree cleanup.

## Routed Docs

- Feature: [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- Requirements: [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- Specs: [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- Change archive: [../change/2026-07-08_m-archive-default-closeout.md](../change/2026-07-08_m-archive-default-closeout.md)

## Open Questions

- None.

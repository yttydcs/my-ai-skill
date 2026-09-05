# Documentation

## Reading Order
- Start with intake when original request evidence matters.
- Read features for current user-visible feature behavior.
- Read requirements for long-lived capability intent and acceptance.
- Read specs for technical contracts and repository integration rules.
- Read decisions for architecturally significant choices.
- Read plan for archived workflow planning history.
- Read change for completed workflow results and verification.
- Read lessons for reusable prevention guidance.

## Troubleshooting Order
- Start with lessons when the request is about a symptom, outage, or repeated confusion.
- Read change only when the lesson doc is missing or does not explain this workflow's detail.
- Confirm stable truth in features, specs, and requirements before changing behavior.

## Retired Capabilities

- `m-orchestrator` was removed on 2026-09-05. Its intake, decisions, plans, changes, lessons, and retired feature/requirement/spec documents remain as history. They do not authorize dispatch, runtime recovery, or archive admission in the current skill collection. See the [retired feature status](features/m-project-orchestrator.md).

## Private Docs Boundary

- Project or product knowledge may live in a private docs root separate from code repositories.
- A private docs root can be a local folder or a separate local/private Git repository.
- Remote configuration, push targets, and backup strategy are user-owned decisions.
- Do not treat docs inside a pushable code repository as canonical when the project has a private docs root unless the user explicitly says so.

## Workflow Control Exception
- Active workflow control files remain at the worktree root as `plan.md` or `todo.md` when a workflow requires them.
- Treat `docs/plan/` as the archive layer for planning artifacts, not the active control surface.

## Sections
- [intake/README.md](intake/README.md)
- [features/README.md](features/README.md)
- [requirements/README.md](requirements/README.md)
- [specs/README.md](specs/README.md)
- [decisions/README.md](decisions/README.md)
- [plan/README.md](plan/README.md)
- [change/README.md](change/README.md)
- [lessons/README.md](lessons/README.md)

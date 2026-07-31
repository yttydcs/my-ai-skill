# Features

## Purpose

Store current user-visible feature behavior as complete feature dossiers.

## How to Enter This Section

- Start here when the request is about a product feature, user workflow, screen, button, CRUD behavior, permission, or acceptance scenario.
- Use this section for feature behavior that may span multiple code repositories.
- Link technical contracts to `../specs/` instead of duplicating them.

## What Belongs Here

- feature goals and non-goals
- actors, permissions, entry points, layout, navigation, and UI states
- CRUD workflows and validation rules
- acceptance scenarios, preferably in a lightweight Given/When/Then style
- cross-repo ownership maps and links to related specs, decisions, changes, and intake records

## Naming / Maintenance Rules

- Use stable names without dates.
- Update the feature doc whenever current behavior changes.
- Do not use change archives as the only home for current feature truth.

## Current Docs

- [m-project-orchestrator.md](m-project-orchestrator.md) - persistent per-project Planner with temporary Workers and bounded Tester Pools
- [m-context.md](m-context.md) - reusable plaintext Agent context loading and skill composition
- [m-autoflow-workflow.md](m-autoflow-workflow.md)
- [m-quick-fast-path.md](m-quick-fast-path.md) - guarded one-repo direct-edit path with mandatory governed-doc context

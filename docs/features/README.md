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

- [m-autoflow-workflow.md](m-autoflow-workflow.md)

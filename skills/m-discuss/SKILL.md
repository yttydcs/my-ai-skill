---
name: m-discuss
description: Discussion and discovery phase for the m-autoflow workflow. Use when Codex needs to clarify a vague request, brainstorm feasible options, challenge unreasonable requirements, compare approaches, search current best practices when useful, create or confirm the workflow worktree early, and produce a decision-ready brief before $m-plan.
---

# m:discuss

## Overview

Use this skill before `$m-plan` when the work needs product discovery, technical brainstorming, option comparison, or current external research. Act like a senior product partner with strong engineering judgment: help shape the right problem before anyone writes an execution plan.

## Quick Start

- Read `references/discussion.md`.
- Read `references/research.md` when current external evidence, web search, vendor/library comparison, security/regulatory facts, or best-practice research would materially improve the discussion.
- Read `../m-autoflow/references/initialization.md` before creating or confirming a branch/worktree.
- Read `../m-autoflow/references/output-components.md` before presenting the discussion result.
- Use `$m-docs` when discussion creates or changes intake, features, requirements, specs, or decisions.

## Workflow

1. Capture the original request, goals, non-goals, assumptions, and open questions.
2. Confirm `project_root`, `docs_root`, `code_repos`, base branch, and whether a dedicated worktree already exists.
3. Create or confirm the dedicated worktree when this discussion starts a full workflow.
4. Explore viable options, tradeoffs, constraints, risks, and rejected ideas.
5. Search the web only when current external evidence or best practices matter; cite sources and separate facts from inference.
6. Challenge unreasonable, unsafe, contradictory, or under-specified requirements and propose better alternatives.
7. Produce a discussion brief that `$m-plan` can consume without chat-only context.

## Exit Gate

End with:

- problem / opportunity
- confirmed goals and non-goals
- assumptions and open questions
- viable options and rejected options
- research summary and citations when used
- recommended direction
- worktree / branch / docs root status
- whether the work may proceed to `$m-plan`

Use a compact option comparison table when several directions were evaluated. Add Mermaid only when branches, dependencies, or ownership are difficult to understand linearly. Link any created brief, doc, branch, or worktree artifact using the shared output rules.

Do not produce the executable architecture plan, implement code, run heavy validation, create `docs/change`, merge branches, or clean worktrees from this phase.

---
name: m-autoflow-research
description: Optional web research phase for the m-autoflow planning workflow. Use only when the user explicitly asks to search the web, look up current information, investigate external sources, compare current options, or do online research before planning. Supports parallel read-only research sub-agents when host policy allows it, then requires the main agent to verify sources, reconcile conflicts, cite links, and feed only confirmed findings into plan.md or docs through $m-docs when appropriate.
---

# m:autoflow research

## Overview

Use this skill for optional online research before or during `$m-autoflow-plan`. Do not trigger it for ordinary planning unless the user explicitly asks for web research, current external information, or source-backed investigation.

## Quick Start

- Read `references/research.md`.
- Treat this as a read-only planning aid, not an implementation phase.
- Use current official or primary sources when technical, legal, financial, product, API, library, or policy details may have changed.
- Use parallel research sub-agents only when host policy allows it and the research question can be split into independent source domains or hypotheses.
- The main agent must synthesize, verify, and cite final findings; do not pass through sub-agent conclusions unreviewed.

## Trigger Gate

Run this skill only when the user explicitly asks for one of these:

- web search
- online research
- current or latest external facts
- market, vendor, library, API, regulation, security, or product comparison
- source-backed investigation before planning

Do not run this skill for normal `$m-autoflow-plan` work that can be answered from repo docs, code, requirements, specs, or user-provided context.

## Workflow

1. Define the research question, decision it informs, and freshness requirement.
2. Split the research into independent lanes when useful, such as official docs, alternatives, risks, security, performance, pricing, migration, or community issue evidence.
3. Dispatch parallel read-only research sub-agents only when allowed and useful. Each lane must have a bounded question, allowed source types, and required output format.
4. Search and read sources. Prefer primary and official sources; use secondary sources only to discover leads or compare interpretations.
5. Cross-check claims across sources and dates. Mark uncertain or conflicting findings explicitly.
6. Produce a concise research brief with citations, confidence, tradeoffs, and implications for planning.
7. If findings change stable project truth, explicitly use `$m-docs` to route updates into `docs/requirements` or `docs/specs`. Do not bury durable conclusions only in `plan.md`.

## Exit Gate

Return:

- research question and scope
- sources used with links
- confirmed findings
- conflicts or uncertainties
- planning implications
- requirements/specs/docs impact
- whether more research is needed

Do not implement code, create worktrees, or update archive docs from this phase.

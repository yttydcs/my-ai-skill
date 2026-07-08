# Research Rules

Use this reference for optional web research during `$m-discuss`.

## Optionality

- Research is not mandatory.
- Use it when the user asks for online research, web search, source-backed investigation, current external information, or best-practice comparison.
- Use it when the discussion would otherwise rely on stale or uncertain external facts.
- Do not browse when repo docs, code, stable requirements, and user context are enough.

## Source Quality

- Prefer official docs, primary vendor pages, specifications, standards, changelogs, release notes, source repositories, issue trackers, and authoritative datasets.
- For technical API/library/framework questions, rely on official documentation or primary repository evidence.
- For security, legal, financial, compliance, pricing, or product availability questions, verify against current primary sources.
- Use blogs, forums, and social posts only as supporting evidence or leads, unless the user specifically wants sentiment/community reports.
- Record publication dates, version numbers, and retrieval-sensitive facts when they matter.

## Parallel Research

Parallel sub-agents are allowed only for read-only research lanes and only when host policy permits delegation.

Use parallel lanes when:

- the question naturally separates into independent source domains
- different vendors or approaches can be researched independently
- one lane can inspect official docs while another checks issues, risks, or migration evidence
- time-sensitive coverage benefits from concurrent searches

Do not use sub-agents when:

- the question is narrow enough for one search pass
- source interpretation requires a single continuous chain of reasoning
- the user asked not to delegate
- host policy does not allow sub-agents

Each sub-agent context package must include:

- research lane title
- bounded question
- freshness requirement
- allowed source types
- sources to avoid
- expected output: links, dates, direct evidence, confidence, uncertainties
- instruction to avoid implementation, edits, credentials, or destructive actions

## Synthesis

The main agent must:

- review every source before relying on it
- deduplicate repeated claims
- compare dates and versions
- separate fact from inference
- mark uncertainty instead of overclaiming
- cite links in the final answer or planning artifact
- feed only verified findings into `plan.md`, requirements, or specs

## Docs Routing

Use `$m-docs` when research changes stable project truth:

- product requirements -> `docs/requirements`
- architecture or API choices -> `docs/specs`
- reusable external investigation method or recurring vendor pitfall -> `docs/lessons`
- workflow-specific research summary -> discussion brief, active `plan.md`, or later `docs/change`

Do not treat research notes alone as a source of truth.

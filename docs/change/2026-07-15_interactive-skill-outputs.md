# 2026-07-15 Official Interactive Skill Outputs

## 变更背景 / 目标

The earlier visual-output improvement covered Markdown tables, Mermaid, file links, screenshots, review comments, and Git directives. The user clarified that Codex's official `$visualize:visualize` capability should also be available for high-value skill results such as option selection, evidence navigation, buttons, and icons.

This workflow adds a bounded official-interaction layer without weakening plain-Markdown fallback, approval gates, repository safety, or host portability.

## 具体变更内容

- Added `skills/m-autoflow/references/interactive-output-patterns.md` as the workflow-specific trigger, fallback, secret-protection, and action-boundary contract.
- Extended the shared component-selection reference so interaction is selected only when it materially improves selection, drill-down, evidence navigation, or a next-phase request.
- Integrated the first rollout with `$m-discuss`, `$m-plan`, `$m-test`, and `$m-archive` while keeping their existing phase semantics.
- Required official invocation by `$visualize:visualize` name rather than a versioned plugin-cache path.
- Kept presentation-only state local and routed Codex work through `window.openai.sendFollowUpMessage` followed by normal entry-gate revalidation.
- Preserved complete Markdown outcomes when inline rendering or the host bridge is unavailable.
- Added contract tests for routing, fallback, secret handling, follow-up-only actions, and path portability.
- Validated a representative result at exact 736px and 320px inner widths with Lucide icons, local selection, follow-up payload capture, and screenshot evidence.

## Docs root

- `D:\project\my-ai-skills\docs` after merge.
- The selected governed docs root is versioned in the same local repository as the skills.
- No push, publication, remote modification, or backup target was requested or performed.

## Intake impact

- Intake impact: updated.
- The existing visual-output intake was clarified during planning and now links this completed interactive-output workflow.

## Feature impact

- Feature impact: updated.
- `m-autoflow` now documents official inline interaction as an optional high-value output path with a first rollout across four phases.

## Requirements impact

- Requirements impact: updated.
- Durable requirements now cover trigger selection, accessibility, fallback, capability-name routing, secret protection, and phase-gated follow-up actions.

## Specs impact

- Specs impact: updated.
- The technical contract now defines reference ownership, runtime boundaries, `window.openai.sendFollowUpMessage`, thread-scoped generated artifacts, and regression expectations.

## Decision impact

- Decision impact: none.
- The hybrid policy is localized and reversible, and it does not alter repository architecture or introduce a persistent runtime dependency requiring an ADR.

## Lessons impact

- Lessons impact: updated.
- Added a reusable lesson for distinguishing fragment defects from Codex visualization preview-host limitations during keyboard and console validation.

## Related intake

- [Visual output components request](../intake/2026-07-15_visual-output-components.md)

## Related features

- [m-autoflow workflow](../features/m-autoflow-workflow.md)

## Related requirements

- [m-autoflow workflow skill](../requirements/m-autoflow-skill.md)

## Related specs

- [m-autoflow workflow skill spec](../specs/m-autoflow-skill.md)

## Related decisions

- None.

## Related lessons

- [Codex visualization preview limitations](../lessons/codex-visualization-preview-limitations.md)

## 对应 plan.md 任务映射

- `VIS-1`: completed; added the shared interactive-output contract and static-to-interactive routing.
- `VIS-2`: completed; integrated `$m-discuss`, `$m-plan`, `$m-test`, and `$m-archive`.
- `VIS-3`: completed; extended regression coverage, validated and synchronized five skill packages, and verified exact installed-source parity.
- `VIS-4`: completed; rendered and operated a representative result with desktop, narrow, accessibility, local-selection, and follow-up-boundary evidence.
- `VIS-D1`: deferred; remaining skills require a separate evidence-backed rollout decision.
- `VIS-D2`: not executed; standalone publication was outside the requested Codex conversation surface.
- `VIS-D3`: rejected; a repository visualization runtime would duplicate the official capability.
- [Archived plan](../plan/2026-07-15_interactive-skill-outputs.md)

## 经验 / 教训摘要

- Official interaction should supplement, never replace, exact Markdown status and manual next commands.
- A visual button is a follow-up request, not proof that approval, execution, archive, or cleanup succeeded.
- Distributed skills should bind to the capability name and let the installed official skill own rendering and design-system details.
- Preview-host behavior must be separated from fragment behavior: native controls, focus state, local selection, payload capture, and source inspection provide independent evidence.

## 可复用排查线索

- Symptoms: inline controls render but a synthetic Enter / Space action does not fire in the preview; a preview reload logs `MutationObserver.observe`; a button appears to request a phase without proving the phase ran.
- Trigger conditions: official render-helper output inside a sandboxed iframe, browser automation against the preview wrapper, host bridge simulation, or plugin-version drift.
- Keywords / errors: `$visualize:visualize`, `::codex-inline-vis`, `window.openai.sendFollowUpMessage`, `MutationObserver.observe`, `aria-pressed`, `plugins/cache`.
- Quick checks: inspect the fragment for the reported API; verify native button semantics and visible focus; operate local selection by click; capture the exact follow-up payload; compare `scrollWidth` with the required viewport width; confirm the complete Markdown fallback remains present.

## 关键设计决策与权衡

- Chose a hybrid trigger instead of Markdown-only or always-interactive output to balance convenience, latency, visual noise, and portability.
- Kept detailed workflow rules in a progressive-disclosure reference so phase `SKILL.md` files remain concise.
- Used follow-up requests instead of direct repository mutations so normal workflow approvals and entry gates remain authoritative.
- Reused official Lucide and utility-class support instead of adding dependencies or copying version-specific implementation instructions.
- Kept generated fragments and screenshots thread-scoped and outside repository source.

## 测试与验证方式 / 结果

- Full unit discovery: 26 tests passed; 1 existing Windows symlink-privilege case skipped with `WinError 1314`.
- Skill validation: `m-autoflow`, `m-discuss`, `m-plan`, `m-test`, and `m-archive` passed.
- Synchronization and parity: all five changed packages matched source and installed file sets and SHA-256 content, excluding generated build metadata.
- Portability review: no distributed skill contains a versioned visualization plugin-cache path.
- Exact desktop layout: 736px inner viewport, `scrollWidth = 736`, four buttons and four Lucide icons visible.
- Exact narrow layout: 320px inner viewport, `scrollWidth = 320`, controls wrapped without clipping.
- Interaction: local `aria-pressed` state and detail text changed together.
- Follow-up boundary: captured payload requested `$m-archive` and explicitly required the receiving phase to re-check the test gate, plan, and Git state.
- Fragment safety: no direct Git, filesystem, archive, cleanup, `fetch`, XHR, or WebSocket operation.
- `git diff --check`: passed.

## 潜在影响

- Official inline interaction may add latency and context cost when selected; the trigger requires a material usability benefit.
- Host implementations may differ in keyboard automation or preview-wrapper console behavior; complete Markdown fallback remains authoritative.
- Future plugin contract changes may require compatibility review, but capability-name routing avoids a pinned version dependency.

## 回滚方案

- Revert implementation commit `26fe749` and planning commit `39b640f`, then resynchronize the five affected skill packages from the restored source revision.
- Revert test-record commit `f99a6d8` and the archive commit separately when removing workflow history is also required.
- No generated visualization artifact needs repository rollback because runtime evidence was never committed to source.

## 子Agent执行轨迹

- No sub-agents were used. VIS-1 through VIS-3 had tightly coupled references and route assertions, VIS-4 was a serial host-interaction validation, and the user invoked direct phase commands rather than `$m-go`.

# 2026-07-20 m-discuss Grill Mode

## 变更背景 / 目标

The user asked to investigate Matt Pocock's public `grill-me` skill and integrate the useful interview behavior into this repository's `$m-discuss` phase. The goal was to add an explicit, one-question-at-a-time decision pressure-test without creating an external runtime dependency, slowing ordinary discussion, or weakening the existing brief and phase gates.

## 具体变更内容

- Added `skills/m-discuss/references/grilling.md` as the conditional interview protocol.
- Updated `$m-discuss` routing so Grill Mode activates only after an explicit request to be grilled, pressure-test a plan through hard questions, or resolve decisions one at a time.
- Kept ordinary ambiguous requests on the existing standard discussion path.
- Added a task-local decision snapshot for confirmed, rejected, deferred, and open decisions plus facts, evidence gaps, and parent/child dependencies.
- Required discoverable facts to be researched before asking the user.
- Required exactly one judgment question per turn, with one recommended answer and rationale, followed by a wait for the user's answer.
- Added early wrap-up, explicit shared-understanding confirmation, and no-automatic-planning/implementation gates.
- Preserved `references/discussion.md` as the authority for the final brief, blockers, worktree status, and `$m-plan` handoff.
- Updated `manifests/m-discuss.json` to version `0.2.0` and packaged the new reference.
- Added `tests/test_m_discuss_grill_contract.py` with eight deterministic contract tests.
- Updated workflow feature, durable requirements, and technical spec docs.
- Synchronized the validated source to ignored dist output and the installed `C:\Users\HelloWorld\.codex\skills\m-discuss` copy.

## Docs root

- Active workflow docs root: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\docs`
- Canonical local docs root after closeout: `D:\project\my-ai-skills\docs`
- Publication status: local-only; no remote, push, publication, or backup configuration changed.

## Intake impact

Updated. Added the original request and research summary in [2026-07-20_m-discuss-grill-mode.md](../intake/2026-07-20_m-discuss-grill-mode.md).

## Feature impact

Updated. [m-autoflow-workflow.md](../features/m-autoflow-workflow.md) now describes explicit Grill Mode behavior and acceptance.

## Requirements impact

Updated. [m-autoflow-skill.md](../requirements/m-autoflow-skill.md) now defines activation, interview, completion, and compatibility requirements.

## Specs impact

Updated. [m-autoflow-skill.md](../specs/m-autoflow-skill.md) now defines package routing, module ownership, validation, and sync contracts.

## Decision impact

Updated. Added and accepted [2026-07-20_m-discuss-grill-mode.md](../decisions/2026-07-20_m-discuss-grill-mode.md).

## Lessons impact

None. No new reusable failure pattern emerged. The focused-test import error was an already documented repository behavior covered by [python-unittest-discovery-nonpackage-tests.md](../lessons/python-unittest-discovery-nonpackage-tests.md), so that lesson was reused without modification.

## Related intake

- [2026-07-20_m-discuss-grill-mode.md](../intake/2026-07-20_m-discuss-grill-mode.md)

## Related features

- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related requirements

- [m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- [2026-07-20_m-discuss-grill-mode.md](../decisions/2026-07-20_m-discuss-grill-mode.md)

## Related lessons

- [Python unittest discovery for non-package tests](../lessons/python-unittest-discovery-nonpackage-tests.md)

## 对应 plan.md 任务映射

- `GM-1`: added the conditional skill routing and local Grill Mode protocol.
- `GM-2`: updated manifest/version and added focused contract tests.
- `GM-3`: aligned feature, requirements, and spec docs.
- `GM-4`: validated source, synchronized generated copies, and verified hash parity.
- `GM-5`: created this archive and the retained plan record, then handed closeout to the control-plane merge/cleanup sequence.

## 经验 / 教训摘要

- The useful part of upstream `grill-me` is the reusable interview discipline, not its small wrapper file.
- A conditional reference preserves normal skill latency and keeps the always-loaded `SKILL.md` concise.
- Stateless questioning becomes safer when it feeds an existing durable brief and explicit downstream phase gate.
- One-question behavior needs explicit prompt-contract tests because models may otherwise batch questions or continue directly into implementation.
- Existing troubleshooting lessons should be reused instead of creating duplicate lesson documents for the same runner failure.

## 可复用排查线索

- Symptoms: Grill Mode activates on an ordinary vague request; several questions appear in one turn; the agent asks for repository facts; the interview ends by implementing; the brief loses unresolved decisions.
- Trigger conditions: conditional reference omitted from the manifest; trigger wording becomes implicit; single-question/wait wording is weakened; `discussion.md` stops being the final handoff authority.
- Keywords: `grill-me`, `grilling`, `explicit Grill Mode`, `one question per turn`, `shared understanding`, `references/grilling.md`, `m-discuss 0.2.0`.
- Quick checks:
  - run `python -m unittest discover -s tests -p "test_m_discuss_grill_contract.py"`;
  - verify `manifests/m-discuss.json` includes `references/grilling.md`;
  - verify ordinary ambiguity alone is explicitly excluded from activation;
  - compare source, dist, and installed skill trees while excluding generated `.build-info.json`.

## 关键设计决策与权衡

- Chose an internal explicit mode over an external dependency, mandatory grilling, or a separate `$m-grill` entry point.
- Chose open-ended but deduplicated questioning with a natural-language wrap-up instead of a hard numeric cap.
- Required explicit user confirmation but kept `$m-plan` and implementation as separate user-authorized phases.
- Retained upstream source and MIT license links as attribution while keeping the local protocol independently owned and runtime-independent.

## 测试与验证方式 / 结果

- Focused Grill Mode contract tests: 8 passed.
- Full repository unittest discovery: 40 passed, 1 existing conditional test skipped.
- Source `m-discuss` skill validation: passed.
- Installed `m-discuss` skill validation: passed.
- `git diff --check`: passed.
- Source -> dist SHA-256 parity: 5 files matched, excluding generated `.build-info.json`.
- Source -> installed SHA-256 parity: 5 files matched, excluding generated `.build-info.json`.
- Dist and installed build metadata version: `0.2.0`.
- Heavy `$m-test`: skipped because there is no runtime UI, schema, network, security-boundary, or performance behavior. Residual risk is limited to model-mediated adherence during a live interview.

## 潜在影响

- Explicit Grill Mode conversations may be longer than ordinary discussion by design.
- Prompt-contract tests verify instruction completeness, not every possible model response.
- Over-broad future trigger edits could regress ordinary discussion latency.
- Dist output remains intentionally ignored; the installed copy depends on the repository sync tool.

## 回滚方案

1. Revert archive commit and implementation commits `07258e9`, `2174254`, `6698149`, and `ee906f6` as appropriate.
2. Restore `manifests/m-discuss.json` to version `0.1.0` without `references/grilling.md`.
3. Run `tools/sync-skills.ps1 -Skill m-discuss` from the restored source to replace dist and installed copies.
4. Rerun skill validation and repository unittest discovery.

## 子Agent执行轨迹

- None. The user did not request delegation, host policy did not permit proactive delegation, and the approved tasks had sequential contract dependencies.

## Closeout

- Archive commit: created on `feat/m-discuss-grill-mode` before control-plane convergence.
- Default closeout after this archive commit: fast-forward local `main`, verify status, remove the dedicated worktree, and delete the merged local feature branch.
- Push status: not requested and not performed.

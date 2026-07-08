# 2026-07-09_m-go-automated-execution

## 变更背景 / 目标

新增 `$m-go` / `m:go` 指令。它定位为 `$m-plan` 之后的高自动化执行入口：主 Agent 只负责调度、审查、验证和验收，所有实现性文件改动由 worker 子 Agent 完成；可并行任务应并行；委派执行完成后自动进入 `$m-test` 行为，并在失败时委派修复直到验收通过或明确阻塞。

## 具体变更内容

- 新增 `skills/m-go` skill 包：
  - `SKILL.md`
  - `references/go.md`
  - `agents/openai.yaml`
- 新增 `manifests/m-go.json`。
- 更新 `$m-autoflow`：
  - 路由 `$m-go`
  - 阶段规则记录 execute 或 go 的执行入口选择
  - 子 Agent 治理记录 `$m-go` 的强制委派语义
  - manifest 依赖加入 `m-go`
  - 默认提示包含 execute-or-go
- 更新 `$m-test` 文案，使其可以被 `$m-go` 自动测试循环调用。
- 更新 stable docs：
  - intake 原始需求
  - feature 当前行为
  - requirements 持久需求
  - specs 技术契约
  - decision 架构决策
- 将 active worktree 根部 `plan.md` 归档到 `docs/plan/2026-07-09_m-go-automated-execution.md`，避免关闭 workflow 后在主仓库根目录残留控制文件。
- 同步安装：
  - `C:\Users\HelloWorld\.codex\skills\m-go`
  - `C:\Users\HelloWorld\.codex\skills\m-autoflow`
  - `C:\Users\HelloWorld\.codex\skills\m-test`

## Docs root

- `D:\project\my-ai-skills\docs`
- Docs changes are local Git changes in the skill source repository. No docs remote, publication, push target, or backup destination was changed.

## Intake impact

updated

## Feature impact

updated

## Requirements impact

updated

## Specs impact

updated

## Decision impact

updated

## Lessons impact

none

No new reusable troubleshooting lesson was created. Existing lesson `skill-frontmatter-yaml-colon` was respected by keeping new skill frontmatter concise and validating the changed skills.

## Related intake

- [../intake/2026-07-09_m-go-automated-execution.md](../intake/2026-07-09_m-go-automated-execution.md)

## Related features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- [../decisions/2026-07-09_m-go-automated-execution.md](../decisions/2026-07-09_m-go-automated-execution.md)
- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)

## Related lessons

- [../lessons/skill-frontmatter-yaml-colon.md](../lessons/skill-frontmatter-yaml-colon.md)

## Related plan

- [../plan/2026-07-09_m-go-automated-execution.md](../plan/2026-07-09_m-go-automated-execution.md)

## 对应 plan.md 任务映射

- G1 - Update stable docs for `$m-go`: completed.
- G2 - Add `$m-go` skill package and manifest: completed.
- G3 - Integrate `$m-go` into umbrella governance: completed.
- G4 - Validate and sync affected skills: completed.
- G5 - Archive and close workflow: this document and closeout.
- G6 - Push branch: not executed; push remains explicit via `$m-gitpush`.

## 经验 / 教训摘要

- `$m-go` is intentionally separate from `$m-execute` so normal execution remains lightweight and optional-delegation based.
- `$m-go` invocation is treated as authorization for worker sub-agent execution within the approved plan scope when host policy permits delegation.
- `$m-go` does not archive, merge, clean, or push; it stops after delegated execution and automatic testing so `$m-archive` can preserve closeout boundaries.
- Active workflow control files should be retained under `docs/plan/` during archive instead of being merged into the main repo root.

## 可复用排查线索

- Symptom: `$m-go` appears to let the main agent edit files directly.
  - Quick check: read `skills/m-go/references/go.md` and confirm `Main Agent Responsibilities` and `Hard Rules`.
- Symptom: `$m-go` appears to bypass `$m-plan`.
  - Quick check: confirm `Entry Gate` requires a confirmed `plan.md` or `todo.md`.
- Symptom: `$m-test` seems optional inside `$m-go`.
  - Quick check: confirm `$m-go` automatic test-loop wording in `skills/m-go/SKILL.md` and `references/go.md`.

## 关键设计决策与权衡

- Chose a separate `$m-go` skill instead of adding a strict mode to `$m-execute`.
- Kept `$m-autoflow` as the umbrella and shared reference host.
- Kept `$m-go` concise at `SKILL.md` level and moved detailed rules into `references/go.md`.
- Did not add compatibility aliases or alter docs backup/publication behavior.

## 测试与验证方式 / 结果

Passed:

- `tools\validate-skills.ps1 -Skill m-go`
- `tools\validate-skills.ps1 -Skill m-autoflow`
- `tools\validate-skills.ps1 -Skill m-test`
- `tools\validate-skills.ps1 -Skill m-execute`
- `tools\sync-skills.ps1 -Skill m-go`
- `tools\sync-skills.ps1 -Skill m-autoflow`
- `tools\sync-skills.ps1 -Skill m-test`
- `git diff --check` with expected Windows CRLF warnings only
- Markdown relative-link existence check for `docs/**/*.md`
- Search confirmed no stale stable-doc links to `../../plan.md`

Skipped:

- `$m-test` heavy review was not run. The user invoked `$m-archive` directly after `$m-execute`, so the skipped heavy validation and residual risk are recorded here.

Residual risk:

- No end-to-end live `$m-go` run was performed in this workflow.
- Future validation of `$m-go` should exercise a real confirmed plan with worker sub-agents and automatic `$m-test` looping.

## 潜在影响

- The Codex skill list gains a new `$m-go` entry after sync.
- `$m-autoflow` now references `$m-go`.
- `$m-test` can be described as both manually invokable and automatically used by `$m-go`.

## 回滚方案

- Revert the archive/merge commit if already merged.
- Remove `skills/m-go`, `manifests/m-go.json`, and the installed `C:\Users\HelloWorld\.codex\skills\m-go` copy if reverting locally.
- Revert `$m-autoflow`, `$m-test`, stable docs, and indexes to the previous commit.
- Rerun sync for any reverted installed skills.

## 子Agent执行轨迹

- No sub-agents were used during this implementation run.
- Reason: the user invoked `$m-execute`, not `$m-go`; host delegation rules require explicit sub-agent authorization.
- The new `$m-go` rules define mandatory worker sub-agent execution for future `$m-go` invocations.

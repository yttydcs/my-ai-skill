# Templates

Use these templates as concise defaults.

## Blocking Output

```md
问题清单
- <issue 1>
- <issue 2>

阻塞：是
禁止进入下一阶段或写代码
```

## plan.md Skeleton

```md
# Plan - <workflow-name>

## Workflow Information
- Repo:
- Branch:
- Base:
- Project Root:
- Docs Root:
- Code Repos:
- Worktree:
- Current Stage:

## Stage Records

### Initialization
- guide.md:
- project/docs/code repo confirmation:
- base/worktree confirmation:

### Discuss - Discovery And Requirements Shaping
#### Goal
#### Scope
#### Assumptions
#### Open Questions
#### Options Considered
#### Rejected Options
#### Recommended Direction
#### Research Summary
#### Worktree / Branch / Docs Root Status
#### Issue List

### Plan - Requirements And Architecture
#### Discussion Summary
#### Accepted / Rejected Requirements
#### Requirements Analysis
##### Goal
##### Scope
##### Use Cases
##### Functional Requirements
##### Non-functional Requirements
##### Inputs / Outputs
##### Edge Cases
##### Acceptance Criteria
##### Risks
#### Architecture Design
##### Overall Solution
##### Alternatives Considered
##### Module Responsibilities
##### Data / Call Flow
##### Interface Drafts
##### Error Handling and Safety
##### Performance and Testing Strategy
##### Extensibility Design Points
#### Issue List

### Stage 3.1 - Planning
#### Project Goal and Current State
#### Docs Governance Routing Decision
#### Related Intake / Features / Requirements / Specs / Decisions / Lessons
#### Stable Docs Impact
- Intake impact:
- Feature impact:
- Requirements impact:
- Specs impact:
- Decision impact:
#### Executable Task List
#### Execution Scope After Approval
##### Will Execute
- <Task IDs approved for the next execution phase>
##### Will Not Execute Now
- <Task IDs plus reason: blocked / out of scope / deferred / research-only / separate approval required>
#### Task Details
#### Dependencies
#### Risks and Notes
#### Parallelism Assessment
#### Issue List
```

## Task Block

```md
##### <Task ID> - <Title>
- Owner:
- Worktree:
- Plan Path:
- Goal:
- Files / Modules:
- Write Set:
- Acceptance:
- Test Points:
- Rollback:
```

## Plan Task Summary Table

Use this table in the direct `$m-plan` response after creating or confirming the active `plan.md` / `todo.md`.

```md
| Task ID | Title | Scope | Files / Modules | Acceptance / Tests | Risk / Notes |
| --- | --- | --- | --- | --- | --- |
| <Task ID> | <short title> | Will execute / Will not execute now | <paths or modules> | <short acceptance or test cue> | <risk, blocker, or deferral reason> |
```

## docs/change Skeleton

```md
# YYYY-MM-DD_<topic>

## 变更背景 / 目标
## 具体变更内容
## Docs root
## Intake impact
## Feature impact
## Requirements impact
## Specs impact
## Decision impact
## Lessons impact
## Related intake
## Related features
## Related requirements
## Related specs
## Related decisions
## Related lessons
## 对应 plan.md 任务映射
## 经验 / 教训摘要
## 可复用排查线索
## 关键设计决策与权衡
## 测试与验证方式 / 结果
## 潜在影响
## 回滚方案
## 子Agent执行轨迹
```

## docs/lessons Skeleton

```md
# <lesson-topic>

## Summary
## Lookup Hints
## Symptoms
## Impact
## Trigger Conditions
## Root Cause
## Investigation Trail
## Resolution
## Prevention / Guardrails
## Related Docs
```

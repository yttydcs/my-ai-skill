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
- Worktree:
- Current Stage:

## Stage Records

### Initialization
- guide.md:
- base/worktree confirmation:

### Stage 1 - Requirements Analysis
#### Goal
#### Scope
#### Use Cases
#### Functional Requirements
#### Non-functional Requirements
#### Inputs / Outputs
#### Edge Cases
#### Acceptance Criteria
#### Risks
#### Issue List

### Stage 2 - Architecture Design
#### Overall Solution
#### Alternatives Considered
#### Module Responsibilities
#### Data / Call Flow
#### Interface Drafts
#### Error Handling and Safety
#### Performance and Testing Strategy
#### Extensibility Design Points
#### Issue List

### Stage 3.1 - Planning
#### Project Goal and Current State
#### Docs Governance Routing Decision
#### Executable Task List
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

## docs/change Skeleton

```md
# YYYY-MM-DD_<topic>

## 变更背景 / 目标
## 具体变更内容
## Requirements impact
## Specs impact
## Related requirements
## Related specs
## 对应 plan.md 任务映射
## 关键设计决策与权衡
## 测试与验证方式 / 结果
## 潜在影响
## 回滚方案
## 子Agent执行轨迹
```

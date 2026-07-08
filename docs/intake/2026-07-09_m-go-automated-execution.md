# 2026-07-09 m-go Automated Execution

## Source

- Date: 2026-07-09
- Source: Codex chat
- Requester: User

## Original Request Summary

The user requested a new `m:go` command. Its positioning should be similar to `m:execute`, but with a stricter execution model:

- the executor is a sub-agent
- the main agent using `m:go` does not perform implementation
- all modifications are completed through sub-agents
- the main agent only schedules, coordinates, and audits
- parallelizable execute tasks should run in parallel
- after all tasks finish, the workflow should automatically call `m:test`
- the loop should continue until every acceptance item is complete

## Initial Interpretation

`$m-go` should be a high-automation entry point after `$m-plan`, not a replacement for `$m-execute`. It must preserve plan gating while making delegated implementation and automatic test-loop behavior explicit.

## Stable Docs Impact

- Feature impact: update `docs/features/m-autoflow-workflow.md`
- Requirements impact: update `docs/requirements/m-autoflow-skill.md`
- Specs impact: update `docs/specs/m-autoflow-skill.md`
- Decision impact: add `docs/decisions/2026-07-09_m-go-automated-execution.md`

## Related Docs

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- [../decisions/2026-07-09_m-go-automated-execution.md](../decisions/2026-07-09_m-go-automated-execution.md)
- [../plan/2026-07-09_m-go-automated-execution.md](../plan/2026-07-09_m-go-automated-execution.md)
- [../change/2026-07-09_m-go-automated-execution.md](../change/2026-07-09_m-go-automated-execution.md)

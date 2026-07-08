# Templates

Use these templates as concise defaults. Adjust to fit the project.

## docs/README.md

```md
# Documentation

## Reading Order
- intake
- features
- requirements
- specs
- decisions
- plan
- change
- lessons

## Troubleshooting Order
- lessons
- change
- features
- specs
- requirements

## Private Docs Boundary
- Docs may be private and separate from code repositories.
- Remote, push, publication, and backup decisions are user-owned.

## Sections
- [intake/README.md](intake/README.md)
- [features/README.md](features/README.md)
- [requirements/README.md](requirements/README.md)
- [specs/README.md](specs/README.md)
- [decisions/README.md](decisions/README.md)
- [plan/README.md](plan/README.md)
- [change/README.md](change/README.md)
- [lessons/README.md](lessons/README.md)
```

## Intake Doc

```md
# YYYY-MM-DD <Request Topic>

## Source
## Request Text / Source-preserving Summary
## Context
## Confirmed Requirements
## Open Questions
## Routed Docs
## Related Changes
```

## Feature Doc

```md
# <Feature>

## Status
## Goal
## Non-goals
## Actors / Permissions
## Entry Points
## Layout / Navigation
## Data Model
## CRUD Workflows
### Create
### Read / Search / Filter
### Update
### Delete / Disable
## Validation Rules
## Empty / Loading / Error States
## API / Integration Contracts
## Audit / Security
## Acceptance Scenarios
## Cross-repo Ownership
## Related Intake
## Related Requirements
## Related Specs
## Related Decisions
## Related Changes
## Related Lessons
```

## Requirement Doc

```md
# <Capability>

## Background
## Goal
## Scope
## Scenarios
## Functional Requirements
## Non-functional Requirements
## Edge Cases
## Acceptance Criteria
## Related Features
## Related Specs
## Related Changes
```

## Spec Doc

```md
# <Capability Spec>

## Scope
## Interfaces / Contracts
## Data Model or Protocol
## Error Handling
## Security / Safety
## Performance Constraints
## Related Features
## Related Requirements
## Related Decisions
## Related Changes
```

## Decision Entry

```md
# YYYY-MM-DD <Decision Topic>

## Status
## Context
## Options Considered
## Decision
## Consequences
## Confidence
## Supersedes / Superseded By
## Related Features
## Related Specs
## Related Changes
```

## Plan Entry

```md
# YYYY-MM-DD <Topic>

## Goal
## Docs Root
## Related Intake
## Related Features
## Related Requirements
## Related Specs
## Related Decisions
## Intake Impact
## Feature Impact
## Requirements Impact
## Specs Impact
## Decision Impact
## Tasks
## Acceptance
## Tests
## Rollback
```

## Change Entry

```md
# YYYY-MM-DD <Topic>

## Background
## Changes
## Related Plan
## Related Intake
## Related Features
## Related Requirements
## Related Specs
## Related Decisions
## Lessons Impact
## Related Lessons
## Searchable Lessons Summary
## Intake Impact
## Feature Impact
## Requirements Impact
## Specs Impact
## Decision Impact
## Validation
## Rollback
```

## Lesson Entry

```md
# <Lesson Topic>

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

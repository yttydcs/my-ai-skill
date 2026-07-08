# Skill Frontmatter YAML Colon

## Summary

Skill `SKILL.md` frontmatter is parsed as YAML. A long unquoted `description` that contains YAML-sensitive colon syntax can fail validation even when the Markdown body is otherwise correct.

## Lookup Hints

- Symptoms: validator says the skill frontmatter is invalid
- Keywords: `Invalid YAML in frontmatter`, `mapping values are not allowed`, `description`, `SKILL.md`, `quick_validate.py`, colon
- Trigger Conditions: hand-editing a skill frontmatter description, especially a long one with punctuation
- Quick Checks:
  - run `tools\validate-skills.ps1 -Skill <skill-name>`
  - inspect the top `---` frontmatter block
  - remove colon-like wording or quote the YAML scalar

## Symptoms

- `tools\validate-skills.ps1 -Skill <skill-name>` reports `Invalid YAML in frontmatter`.
- The YAML parser reports `mapping values are not allowed`.
- The line/column points into the `description` field rather than the Markdown body.

## Impact

- The skill cannot be treated as valid by the repository validator.
- Syncing an invalid skill may leave the local installed skill out of date or misleading.
- The visible failure can look like a content problem even though the root cause is YAML syntax.

## Trigger Conditions

- The skill frontmatter is edited manually.
- The `description` is long and includes a colon pattern.
- The description is not quoted as a YAML scalar.

## Root Cause

YAML treats some colon patterns as mapping syntax. In this workflow, the umbrella `m-autoflow` description included a colon before a list of phase examples, which made the frontmatter parser reject the file.

## Investigation Trail

- Ran `tools\validate-skills.ps1 -Skill m-autoflow`.
- Validator reported `Invalid YAML in frontmatter` and `mapping values are not allowed`.
- The reported location pointed at the `description` line.
- Rewording the description to avoid the colon pattern made the skill pass validation.

## Resolution

- Reworded the `m-autoflow` description so the YAML frontmatter remained a plain scalar.
- Reran `tools\validate-skills.ps1 -Skill m-autoflow`.
- Confirmed the skill was valid.

## Prevention / Guardrails

- Keep skill frontmatter descriptions plain and concise.
- Avoid colon-introduced example lists inside unquoted frontmatter values.
- Prefer moving detailed examples into the Markdown body.
- Always run `tools\validate-skills.ps1 -Skill <skill-name>` after changing skill frontmatter.
- If a colon is necessary, quote the YAML scalar and rerun validation.

## Related Intake / Features / Requirements / Specs / Decisions / Changes

- Related intake:
  - [../intake/2026-07-08_m-skill-phase-rename.md](../intake/2026-07-08_m-skill-phase-rename.md)
- Related features:
  - [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- Related requirements:
  - [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- Related specs:
  - [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- Related decisions:
  - [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)
- Related changes:
  - [../change/2026-07-08_m-skill-phase-rename.md](../change/2026-07-08_m-skill-phase-rename.md)

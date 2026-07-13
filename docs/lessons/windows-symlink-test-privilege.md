# Windows Symlink Test Privilege

## Summary

Windows may reject symbolic-link fixture creation with `WinError 1314` for an ordinary process. A security regression test can therefore be skipped even when the runtime path-containment guard is implemented correctly.

## Lookup Hints

- Keywords: `WinError 1314`, symbolic link, symlink test skipped, `客户端没有所需的特权`, Windows Developer Mode, `SeCreateSymbolicLinkPrivilege`.
- Quick check: attempt a temporary `Path.symlink_to` operation and distinguish fixture-creation failure from an assertion failure in the code under test.

## Symptoms

- A symlink or root-escape regression test reports `skipped` on Windows.
- Python raises `[WinError 1314] 客户端没有所需的特权` while creating the fixture.
- All non-symlink path-validation tests pass.

## Impact

- The environment cannot directly exercise the symlink/junction escape branch.
- Treating the skip as a pass would overstate validation coverage; treating it as an implementation failure would misdiagnose an environment limitation.

## Trigger Conditions

- Windows process without symbolic-link creation privilege.
- Developer Mode disabled or unavailable.
- Test runner not elevated and no suitable privilege granted.

## Root Cause

The operating system rejects fixture creation before the code under test resolves or validates the link target.

## Investigation Trail

1. Ran the `m-context` standard-library unit suite.
2. The test attempted to create a link inside the context root pointing to a file outside it.
3. Windows returned `WinError 1314` before `load_context` was called.
4. The test recorded an environment-based skip while the runtime `resolve` plus containment check remained covered by review and other path tests.

## Resolution

- Keep the test and skip only when fixture creation itself raises an OS permission error.
- Report the skip and residual risk explicitly.
- Re-run on a Windows environment with symbolic-link privilege or Developer Mode when full evidence is required.

## Prevention / Guardrails

- Do not remove the escape test merely because one environment cannot create its fixture.
- Do not label an environment skip as a passing root-escape test.
- Keep deterministic resolved-path containment logic independent from the test environment.
- For high-risk filesystem changes, obtain a privileged or Developer-Mode validation environment before acceptance.

## Related Docs

- [Intake](../intake/2026-07-13_m-context.md)
- [Feature](../features/m-context.md)
- [Requirements](../requirements/m-context-skill.md)
- [Specification](../specs/m-context-skill.md)
- [Change](../change/2026-07-13_m-context.md)

---
name: m-gitpush
description: Git push workflow with a safe temporary local proxy fallback. Use when the user asks Codex to push a Git branch, especially from MyFlowHub workspaces, or when git push/GitHub access fails with connection reset, timeout, cannot connect to github.com:443, or similar network errors and the user allows using local proxy port 7897.
---

# m:gitpush

## Overview

Push the current Git branch safely. Try the normal remote first; if GitHub is unreachable, retry once through the local proxy at `127.0.0.1:7897` using command-local Git `-c` options only.

## Quick Start

- Read `../m-autoflow/references/output-components.md` before presenting push status.

## Workflow

1. Confirm repository state:
   - Run `git status --short --branch`.
   - Run `git remote -v`.
   - Run `git branch --show-current`.
   - Do not push from the wrong repository or a detached HEAD.

2. Push normally first:

   ```powershell
   git push origin <branch>
   ```

   Use the current branch name unless the user specified a different branch or remote.

3. If push succeeds:
   - Run `git status --short --branch`.
   - Report the pushed commit range or branch update from Git output.

4. If push fails because GitHub is unreachable:
   - Treat these as network failures: `Connection was reset`, `Could not connect to server`, `Failed to connect to github.com port 443`, timeout, or TCP connect failure.
   - Check the local proxy port:

     ```powershell
     Test-NetConnection 127.0.0.1 -Port 7897 -InformationLevel Quiet
     ```

   - If the port is available, retry with temporary command-local proxy settings:

     ```powershell
     git -c http.proxy=http://127.0.0.1:7897 -c https.proxy=http://127.0.0.1:7897 push origin <branch>
     ```

   - Do not use `git config --global`, `git config --system`, persistent environment variables, or permanent remote URL changes.

5. If the proxy retry succeeds:
   - Run `git status --short --branch`.
   - State that the proxy was temporary and no Git config was changed.

6. If the proxy port is unavailable or the proxy retry fails:
   - Report the exact blocking error.
   - Leave the repository unchanged.
   - Mention the branch is still ahead if status shows it.

## Guardrails

- Never force push unless the user explicitly asks for force push.
- Never change global Git proxy configuration for this workflow.
- Never store proxy settings in repo config unless the user explicitly asks for persistent config.
- Prefer `git -c http.proxy=... -c https.proxy=... push ...` over setting `HTTP_PROXY` or `HTTPS_PROXY`.
- Keep unrelated local changes untouched. If the worktree is dirty, push commits only if they already exist; do not auto-commit unless the user requested it.

## Output

- Lead with whether the push succeeded or is blocked.
- Report remote, branch, pushed range, proxy use, and final ahead/behind state in a compact table when several fields matter.
- Emit `::git-push` on its own line only after the push actually succeeds and the active host supports the component.

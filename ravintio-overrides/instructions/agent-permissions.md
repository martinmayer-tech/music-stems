# Agent permissions

These grants are standing. The developer gave them on 2026-11-14, in feature 0000007-agent-permissions. ADR-0004 records the decision.

## Never

- The agent never merges a PR into `main`. Merging into `main` stays human-only.
- The agent never pushes to `main` and never commits on `main`.
- The agent never force-pushes any branch.

## Grants

The agent takes each action below without asking first. It still records each one in the run's build log.

- **Commit:** commit on any branch except `main`.
- **Push:** push any branch except `main` to `origin`. This counts as the remote push grant that the phase invocation rules require.
- **Create PRs:** run `gh pr create` for any branch.
- **Poll git and CI:** wait for checks with `gh pr checks --watch`, `gh run watch`, or repeated `gh pr checks` and `git fetch`. Report the result when every check finishes, including when all pass.
- **Squash merge:** run `gh pr merge --squash` on a PR whose base branch starts with `feat/` or `initiative/`. Check the base with `gh pr view` first. Never use this grant for a PR into `main`.
- **Delete redundant branches:** delete a redundant branch locally with `git branch -d` or `git branch -D`, and on `origin` with `git push origin --delete {branch}`. ADR-0014 records this grant.

## Redundant branches

A branch is redundant when any of these holds:

- Its PR shows `MERGED` in `gh pr view`.
- `git merge-base --is-ancestor` shows its tip inside `origin/main` or inside the branch its PR merged into.
- Its files match a commit inside `origin/main`. `git diff --quiet {branch} {commit}` exits 0 for that commit. A feature branch whose squashed copy merged through a `hotfix/` or `chore/` PR is the usual case.

The old initiative branch counts as redundant once its reshaped PR into `main` has merged.

The agent may always delete a merged branch. The developer gave this word on 2026-11-21. A merged branch needs no PR of its own and no second approval.

Before each deletion, the agent checks these rules:

- Never delete `main`, the current branch, or a branch with an open PR.
- Never delete a branch that a worktree in `plan/.initiative-worktrees/` holds, or one that the initiative driver uses while it runs.
- Never delete a branch whose commits no other branch holds, unless its PR shows `MERGED` or its files match a commit inside `origin/main`.
- Use `git branch -D` only for a branch whose PR shows `MERGED` or whose files match a commit inside `origin/main`. A squash merge leaves its tip outside every other branch.
- Record each deleted branch and its tip hash in the build log, or in the reply when no run is active. `git branch {name} {hash}` then restores it.

## Limits these grants cannot lift

- **merge-guard:** the `merge-guard.mjs` hook allows `gh pr merge --squash` only when the base starts with `initiative/`. A squash into a `feat/` branch stays blocked until the hook changes.
- **Desktop app:** the Claude desktop app may forbid CI polling in a session. Where it does, its rule wins, and the agent tells the developer that a passing run arrives without a notice.
- **Branch protection:** GitHub branch protection on `main` still applies.

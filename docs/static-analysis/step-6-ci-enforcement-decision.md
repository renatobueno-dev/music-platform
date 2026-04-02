# 🚦 Static Analysis — Step 6: CI Enforcement Decision

> Historical note: this step records the point where static analysis was intentionally kept local. The repository has since moved to a fuller quality setup, and the current source of truth is [QUALITY.md](../QUALITY.md) plus `.github/workflows/deploy.yml`.

## 📌 Context

At this point in the static-analysis path:

- the repo-level `pylint` baseline is in place
- the small real findings were fixed
- the biggest `radon` hotspots were reduced
- the docstring policy is selective rather than blanket
- the framework-aware suppressions were narrowed

That made CI enforcement a conscious workflow decision rather than a cleanup prerequisite.

## 🎯 Scope decision

At Step 6, the decision was: do **not** add `pylint` or `radon` to CI yet.

At that time, the repository had a usable local static-analysis baseline, but CI still prioritized the existing validation gates:

- contract tests
- compile checks
- Docker build
- Helm validation
- Terraform validation
- rendered manifest checks

## ✅ Validation target

The documentation at that stage needed to clearly communicate:

- static analysis is intentionally local at that point
- this is a conscious quality/workflow choice, not an omission
- CI enforcement can be reconsidered later if the team wants to maintain that extra gate

## 🏁 Completion criteria

Step 6 was complete when the repo explicitly said:

- `pylint` was not currently part of CI
- the baseline was local-only by design
- the conditions for adding CI enforcement later are understood

## ⚠️ Errors and issues observed

This step did not expose a code problem. It was a workflow-boundary decision.

Observed considerations:

- the lint baseline is stable enough to use locally
- that still does not automatically make it worth enforcing in CI
- adding another CI gate would increase maintenance expectations and should only happen if the team wants that cost

Coding and implementation issues during the step:

- no workflow change was applied on purpose
- the main risk in this step was documentation drift: the repo needed to say clearly that static analysis was intentionally outside the current CI contract

## 📝 Step execution notes

- Step completed in the current cycle.
- Decision taken: keep static analysis out of CI for now.
- Historical reasoning:
  - the local baseline is useful and clean
  - the project already has strong runtime and deployment validation gates
  - CI should not gain a new gate until the team explicitly wants to own it
- If CI enforcement is reconsidered later, the expected prerequisites are:
  - stable lint configuration
  - intentionally accepted remaining suppressions
  - agreement that the extra gate is worth maintaining

Current state note:

- This historical decision was later superseded.
- The current source of truth is [QUALITY.md](../QUALITY.md) and `.github/workflows/deploy.yml`, where `pylint` and `radon` run in the dedicated `python-quality` CI job.

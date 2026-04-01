# Quality Guide — Music Platform API

This document covers the testing strategy and CI pipeline overview.

> For environment setup and how to run the app, see [SETUP.md](./SETUP.md).

---

## 🧪 Tests

The API contract test suite is part of the implemented project baseline, not an optional follow-up.

Contract tests are implemented for:

- root and health availability
- songs CRUD behavior
- playlists CRUD behavior
- playlist-song relationship behavior
- focused negative-path contract validation

Test execution is intentionally isolated from the normal runtime path:

- `tests/conftest.py` forces a disposable SQLite `DATABASE_URL`
- each test run resets schema state for repeatable results
- local runtime database state is not reused by the test suite

Local repeatability check:

```bash
./scripts/verify-local-tests.sh 3
```

Direct single-run command:

```bash
./.venv/bin/python -m pytest -q tests
```

---

## 🚀 CI Overview

The GitHub Actions workflow (`.github/workflows/deploy.yml`) runs on pull requests, pushes to `main`, and manual `workflow_dispatch` runs. It has two jobs: a **validation job** (API contract tests, compile check, Docker build, Helm lint, Terraform validate, and rendered-manifest checks) and a **deploy job** (image push, Terraform apply, runtime secret verification, Helm upgrade, rendered Istio apply, and rollout check). If `KUBE_CONFIG_DATA` is absent, deploy is skipped with an explicit notice rather than failing. Workflow concurrency is also enabled so superseded runs for the same PR/ref are canceled automatically.

For triggers, full job steps, required secrets, and troubleshooting, see [`github-actions.md`](./cicd/github-actions.md).

---

## 🔎 Static Analysis

Static analysis is useful here as a complementary learning and cleanup layer.

- `pylint` helps surface code smells, style issues, and framework-specific lint noise
- `radon` helps highlight complexity hotspots and maintainability signals

These tools are not currently part of the required CI gate for this project, but they are valuable for understanding the codebase and planning refactors.

That is an intentional decision for the current project boundary, not a missing workflow task. The CI gate remains focused on runtime and deployment validation until the static-analysis standard is something the team explicitly wants to maintain in automation.

For commands and interpretation guidance, see [STATIC_ANALYSIS.md](./STATIC_ANALYSIS.md). For the detailed step-by-step cleanup path, see [static-analysis/README.md](./static-analysis/README.md).

---

## 🔗 Related documents

- [Setup guide](./SETUP.md)
- [GitHub Actions guide](./cicd/github-actions.md)
- [Static analysis guide](./STATIC_ANALYSIS.md)
- [Development Log](./DEVELOPMENT_LOG.md)

# 🔐 Phase 3 — Step 18: Align Secret Flow With Deployment Story

## 📌 Context

Step 17 defined who owns secrets by environment.  
Step 18 aligns the real deployment path so CI/CD, Terraform, and Helm follow that ownership model consistently.

Without this alignment, docs can say one thing while deploy behavior does another.

## 🎯 Scope decision

For shared Kubernetes environments, deployment must use external runtime secret ownership.

- Terraform keeps infrastructure-only ownership (namespace and labels).
- GitHub Actions keeps deploy-access ownership (`KUBE_CONFIG_DATA`) and orchestration.
- Helm consumes external runtime credentials through `db.existingSecret`.
- Runtime credentials remain outside repository-managed chart values.

## ✅ Implementation

Workflow alignment:

- Added `DB_EXISTING_SECRET_NAME` workflow env (default `music-platform-secret`).
- Added deploy step to verify external secret exists in target namespace.
- Added key validation for `DATABASE_URL` and `POSTGRES_PASSWORD`.
- Forced Helm deploy to use:
  - `--set db.existingSecret="${DB_EXISTING_SECRET_NAME}"`
- Added validation render for external-secret Helm mode in CI.

Documentation alignment:

- `docs/cicd/github-actions.md`
- `docs/SETUP.md`
- `docs/kubernetes/helm-guide.md`
- `docs/INFRA_DECISIONS.md`
- `docs/SECRETS_OWNERSHIP.md`
- `docs/terraform/flow-integration.md`

## 🔁 Validation

Step 18 validation target:

- shared-environment deploy fails early if runtime DB secret is missing or malformed
- deploy no longer relies on implicit chart-managed runtime secret generation in CI path
- docs and workflow describe the same secret ownership and delivery chain

## 🐞 Step execution notes (issues)

- No blocking issue occurred.
- Main issue addressed: policy and deploy path were partially misaligned (ownership documented, but not fully enforced in CI deploy behavior).
- Local validation note: host `python3` did not have `pytest` installed; test validation was rerun successfully using project virtualenv (`.venv/bin/python -m pytest -q tests`).

## 🏁 Completion criteria

Step 18 is complete when a reader and operator can trace one coherent flow:

1. Terraform prepares namespace baseline.
2. External runtime secret exists with required keys.
3. CI verifies and deploys.
4. Helm consumes the external secret.
5. Istio policies apply and rollout validates.

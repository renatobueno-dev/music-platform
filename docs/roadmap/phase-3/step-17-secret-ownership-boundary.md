# 🔐 Phase 3 — Step 17: Define Secret Ownership Boundary

## 📌 Context

The repository now has migration-owned schema flow and stronger runtime/deploy discipline.

For secret management, multiple delivery paths still exist (local env vars, Helm chart-generated secret, and existing Kubernetes secret references). Without a boundary, origin and rotation ownership become unclear.

## 🎯 Scope decision

Secret ownership boundary is explicitly defined by environment:

- local and Docker Compose: developer-managed secret values
- Kubernetes shared environments: externally injected pre-created Secret is the preferred owner (`db.existingSecret`)
- chart-generated secret path: fallback for isolated/demo environments only
- CI/CD secrets: deploy-access only (`KUBE_CONFIG_DATA`), not application runtime credentials
- Terraform: no application runtime secret ownership

## ✅ Implementation

Added stable policy guide:

- `docs/SECRETS_OWNERSHIP.md`

Aligned supporting references:

- `docs/INFRA_DECISIONS.md`
- `docs/SETUP.md`
- `docs/kubernetes/helm-guide.md`
- `docs/README.md`
- root `README.md`

## 🔁 Validation

Step 17 validation is documentation consistency:

- secret origin, injection, rotation, and allowed definers are explicit
- Kubernetes secret ownership model is no longer implicit
- CI secret scope is separated from app runtime secret ownership
- docs navigation points to a single boundary policy source

## 🐞 Step execution notes (issues)

- No blocking issue occurred.
- Main issue addressed: mixed secret ownership paths were technically supported but not clearly governed by a single policy.

## 🏁 Completion criteria

Step 17 is complete when a reader can answer:

- where secrets originate,
- who injects them,
- who rotates them,
- and who is allowed to define them per environment.

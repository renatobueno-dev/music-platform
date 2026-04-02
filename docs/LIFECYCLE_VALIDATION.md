# Lifecycle Validation

> Final validation summary for the implemented project lifecycle. Confirms the application works through the intended local, test, container, cluster, and Istio ingress paths.

---

## 🎯 Goal

Record the final validation boundary for the current project scope:

- local Python/app lifecycle
- API contract test lifecycle
- Docker/Compose lifecycle
- Kubernetes + Helm + Terraform + Istio resource lifecycle
- live validation through the documented Istio ingress path

This project does **not** require public DNS or internet-facing validation to satisfy its intended scope. The cluster-live Istio ingress path is the final deployed-entry validation boundary.

---

## ✅ Validation Summary

| Step | Scope                                                                        | Result |
| ---- | ---------------------------------------------------------------------------- | ------ |
| A1   | Local lifecycle (`venv` + `DATABASE_URL` + Alembic + app startup)            | Passed |
| A2   | API contract tests                                                           | Passed |
| A3   | Docker lifecycle (`DB -> migrations -> API`)                                 | Passed |
| A4   | Kubernetes lifecycle (Terraform foundation, Helm workloads, Istio resources) | Passed |
| B1   | Istio ingress live path (`playcatch.local` over HTTPS via ingress gateway)   | Passed |

---

## 🐍 A1 — Local Lifecycle

Validated in the normal local runtime flow:

1. activate virtual environment
2. install dependencies
3. set `DATABASE_URL`
4. run `alembic upgrade head`
5. start the app
6. verify:
   - `/`
   - `/health`
   - `/docs`

Confirmed outcome:

- startup succeeded without schema-ownership drift
- database reachability checks passed
- API root, health, and Swagger UI responded correctly

---

## 🧪 A2 — API Contract Tests

Validated through the project test flow:

```bash
./scripts/verify-local-tests.sh 1
```

Confirmed outcome:

- contract suite completed green
- core coverage remained intact for:
  - root and health
  - songs CRUD
  - playlists CRUD
  - playlist-song relationship behavior

---

## 🐳 A3 — Docker Lifecycle

Validated through the migration-owned container path:

1. start database container
2. apply migrations against that database
3. start API container
4. verify:
   - `/`
   - `/health`
   - `/docs`

Confirmed outcome:

- DB container reached healthy state
- API container stayed up
- endpoints responded through the containerized path

Operational note:

- a stale persisted Docker volume can break first-run migration attempts; a clean `docker compose down -v` resolves that environment-specific condition.

---

## ☸️ A4 — Kubernetes Lifecycle

Validated on Minikube through the project’s deployed stack:

1. confirm cluster context
2. apply Terraform namespace baseline
3. ensure required external DB secret exists
4. deploy Helm release
5. apply Alembic migrations to the cluster database
6. verify DB and API rollout
7. apply rendered Istio traffic and security manifests
8. verify workloads and mesh resources

Confirmed outcome:

- API deployment rolled out successfully
- DB StatefulSet rolled out successfully
- workload pods reached ready state with Istio sidecars
- Gateway, VirtualService, DestinationRule, PeerAuthentication, and AuthorizationPolicies were present

Important implementation truth:

- the namespace baseline must stay compatible with the current Istio sidecar-injection model
- namespace quota must account for workload containers plus injected sidecars

---

## 🌐 B1 — Istio Ingress Live Path

Validated through the documented deployed entry path from [traffic.md](./istio/traffic.md):

```bash
kubectl port-forward -n istio-system svc/istio-ingressgateway 18443:443
curl -k --resolve playcatch.local:18443:127.0.0.1 https://playcatch.local:18443/health
```

Prerequisites:

- `playcatch-tls` TLS secret present in `istio-system`
- Gateway, VirtualService, and DestinationRule already applied

Confirmed outcome:

- HTTPS health request returned `{"status":"ok"}`
- request traversed:
  - ingress gateway
  - host match for `playcatch.local`
  - `VirtualService` routing
  - service handoff into the API workload

This is the project’s final deployed-entry validation path.

---

## 🚫 Not Required For This Project

The following are outside the intended validation scope:

- public DNS
- internet-facing public domain
- public load balancer exposure
- real external internet HTTPS validation

Those belong to a different deployment maturity layer.

---

## 🏁 Final Statement

The project runs correctly through its full intended lifecycle and is live through its documented deployment path.

That validated lifecycle is:

### A1 → A2 → A3 → A4 → B1

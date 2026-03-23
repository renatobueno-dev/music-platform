# Documentation

Topic-based reference for the Music Platform API project.

## Project-wide guides

| File | Description |
| --- | --- |
| [CHANGELOG.md](../CHANGELOG.md) | Notable changes per version — Added, Changed, Fixed |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Data model, layer structure, and cross-cutting design decisions |
| [SETUP_AND_QUALITY.md](./SETUP_AND_QUALITY.md) | Environment variables, local/Docker/Kubernetes setup, and testing guide |
| [DEVELOPMENT_LOG.md](./DEVELOPMENT_LOG.md) | Development journey — reasoning, decisions, and corrections per stage |

## Domain

| File | Description |
| --- | --- |
| [domain-scope.md](./domain/domain-scope.md) | Domain model fields and relationship decisions for `Song` and `Playlist` |
| [crud-endpoint-plan.md](./domain/crud-endpoint-plan.md) | Full CRUD route map with methods, schemas, and status codes |

## Containers

| File | Description |
| --- | --- |
| [docker-guide.md](./containers/docker-guide.md) | Docker/Compose steps A–E with validation and troubleshooting checks |

## Kubernetes

| File | Description |
| --- | --- |
| [k8s-concept-map.md](./kubernetes/k8s-concept-map.md) | Docker/Compose → Kubernetes resource concept translation |
| [helm-guide.md](./kubernetes/helm-guide.md) | Helm chart structure, values, and install/lint commands |

## Istio

| File | Description |
| --- | --- |
| [readiness.md](./istio/readiness.md) | Istio readiness checklist and pre-install validation |
| [traffic.md](./istio/traffic.md) | Gateway and VirtualService traffic entry routing |
| [security.md](./istio/security.md) | mTLS PeerAuthentication and AuthorizationPolicy rules |

## CI/CD

| File | Description |
| --- | --- |
| [github-actions.md](./cicd/github-actions.md) | GitHub Actions workflow: triggers, build/push, and deploy steps |

## Terraform

| File | Description |
| --- | --- |
| [scope.md](./terraform/scope.md) | Terraform ownership boundary and responsibility definition |
| [helm-boundary.md](./terraform/helm-boundary.md) | Separation contract between Terraform and Helm concerns |
| [min-scope.md](./terraform/min-scope.md) | Minimum valid Terraform scope for this project |
| [flow-integration.md](./terraform/flow-integration.md) | Integrating Terraform into the full Helm/Istio/CI pipeline |

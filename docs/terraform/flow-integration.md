# Terraform Integration Flow

Integrates Terraform as a prerequisite step in the full delivery sequence.

## Integrated delivery sequence

1. Terraform foundation
   - Manage namespace baseline (`music-platform`) and required labels (Istio injection).
2. Helm application release
   - Deploy API and DB chart resources.
3. Istio application integration
   - Apply traffic and security manifests.
4. Rollout verification
   - Confirm pods, routes, and policies are healthy.

This keeps each layer focused and ordered by dependency.

## CI/CD fit

The workflow now includes Terraform in both paths:

1. Validation job:
   - `terraform fmt -check`
   - `terraform init -backend=false`
   - `terraform validate`
2. Deploy job:
   - `terraform init`
   - optional `terraform import` for pre-existing namespace
   - `terraform apply` for baseline resources
   - Helm deploy
   - Istio manifest apply
   - rollout/resource verification

## Why this integration is coherent

- It preserves existing Helm + Istio behavior.
- It avoids Terraform/Helm object overlap.
- It makes Terraform useful immediately with minimum safe scope.
- It keeps failure diagnostics explicit in workflow logs by layer.

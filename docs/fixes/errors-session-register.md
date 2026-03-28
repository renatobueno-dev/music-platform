# Playlist API Error Register (Session Scope)

This document records only errors that were actually reported or observed during the full project execution flow in this session.

## Reported/Observed Errors

1. GitHub Actions deploy job failed:
   - `Build Push And Deploy` -> `Process completed with exit code 1.`
2. Missing deploy secret:
   - `Missing required secret KUBE_CONFIG_DATA`
3. Invalid workflow syntax:
   - `Invalid workflow file: .github/workflows/deploy.yml#L1`
4. Workflow expression error:
   - `(Line: 51, Col: 9): Unrecognized named-value: 'secrets'`
5. Workflow expression error:
   - `(Line: 125, Col: 9): Unrecognized named-value: 'secrets'`
6. GitHub Actions validate job failed:
   - `Validate Build And Manifests` -> `Process completed with exit code 128.`
7. GitHub Actions validate job failed:
   - `Validate Build And Manifests` -> `Process completed with exit code 50.`
8. Terraform install step failed:
   - `error: cannot delete old terraform`
   - `Is a directory`
   - `Error: Process completed with exit code 50.`
9. Step 5 validation formatting failure:
   - `terraform -chdir=terraform fmt -check` failed (`main.tf` formatting issue).
10. Local command path error:
    - `fatal: cannot change to '.../13_checkpoint_nivel_3': No such file or directory`
11. Local tool policy block:
    - Command rejected as `blocked by policy`
12. Local Docker daemon unavailable:
    - `failed to connect to the docker API ... docker.sock ... no such file or directory`
13. Local host Python dependency error:
    - `ModuleNotFoundError: No module named 'fastapi'`
14. Agent lifecycle/tooling error:
    - `agent with id ... not found`

## Deduplicated Root-Cause Groups

1. **Missing CI secret configuration**
   - Related errors: #1, #2
2. **Invalid GitHub Actions expression context**
   - Related errors: #3, #4, #5
3. **Terraform binary install path collision**
   - Related errors: #7, #8
4. **General CI job execution failures (non-specific at report level)**
   - Related errors: #6
5. **Terraform formatting inconsistency in repository code**
   - Related errors: #9
6. **Incorrect local path usage**
   - Related errors: #10
7. **Execution policy restrictions in tooling environment**
   - Related errors: #11
8. **Docker daemon not available locally at command time**
   - Related errors: #12
9. **Host Python environment missing project dependencies**
   - Related errors: #13
10. **Transient/expired agent handle**
    - Related errors: #14

## Grouped by Issue Type

### CI config issue

| Error # | Error (short) | Where it happened | Stage/Step |
| --- | --- | --- | --- |
| 1 | `Build Push And Deploy` exit code 1 | GitHub Actions deploy run | Etapa 4 / Phase 4 |
| 2 | Missing `KUBE_CONFIG_DATA` | Workflow deploy precheck/secrets | Etapa 4 / Phase 4 |
| 3 | Invalid workflow file | `deploy.yml` parse | Etapa 4 / Phase 4 |
| 4 | `Unrecognized named-value: 'secrets'` (line 51) | Workflow expression context | Etapa 4 / Phase 4 |
| 5 | `Unrecognized named-value: 'secrets'` (line 125) | Workflow expression context | Etapa 4 / Phase 4 |
| 6 | Validate job exit code 128 | CI validation run failure | Etapa 4 / Phase 4 |
| 7 | Validate job exit code 50 | CI validation run failure | Etapa 4 / Phase 4 |
| 8 | `cannot delete old terraform` / `Is a directory` | Terraform install step in workflow | Etapa 4 / Phase 4 |

### Checkpoint code issue

| Error # | Error (short) | Where it happened | Stage/Step |
| --- | --- | --- | --- |
| 9 | `terraform fmt -check` failed (`main.tf`) | Terraform posture changes | Fixes Step 5 |

### Session/tooling issue

| Error # | Error (short) | Where it happened | Stage/Step |
| --- | --- | --- | --- |
| 10 | `fatal: cannot change to ... No such file or directory` | Local command path typo | Session tooling |
| 11 | Command rejected `blocked by policy` | Local command policy guard | Session tooling |
| 12 | Docker API socket not found | Local Docker daemon unavailable | Step 3 validation run |
| 13 | `ModuleNotFoundError: fastapi` | Host Python outside project env/container | Step 4 prep/validation |
| 14 | `agent with id ... not found` | Agent lifecycle cleanup | E2E test cleanup |

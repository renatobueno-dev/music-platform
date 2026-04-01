# Static Analysis Guide

> How to use `pylint` and `radon` in this project to complement tests, spot code smells, and learn from the codebase quality signals.

---

## 🎯 Goal

Static analysis is useful here for a different reason than tests:

- tests answer whether the API behaves correctly
- static analysis helps us inspect maintainability, consistency, and code-smell signals

This project already treats tests as part of the finished baseline. Static analysis is an additional learning and cleanup layer, not the main proof that the application works.

For the runtime and CI validation baseline, see [QUALITY.md](./QUALITY.md).

---

## 🧰 Tools Used

| Tool | What it helps answer | What it does **not** prove |
| --- | --- | --- |
| `pylint` | Are there style problems, suspicious patterns, or easy-to-miss code smells? | That the API works at runtime |
| `radon cc` | Which functions or tests are becoming complex? | That complex code is automatically wrong |
| `radon mi` | How maintainable each file looks at a high level | That a high MI score means design is perfect |

The useful mindset is:

- use tests to confirm behavior
- use static analysis to guide cleanup and refactoring

---

## ▶️ How To Run Locally

1. Activate the project virtual environment and install the normal dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```

2. The repo-level baseline lives in [`.pylintrc`](../.pylintrc), and the static-analysis tools are included in `requirements-dev.txt`. If the environment was created before those dependencies were added, refresh it with:

   ```bash
   ./.venv/bin/pip install -r requirements-dev.txt
   ```

3. Run `pylint` across the Python source tree:

   ```bash
   ./.venv/bin/python -m pylint $(rg --files -g '*.py')
   ```

4. Run `radon` cyclomatic complexity:

   ```bash
   ./.venv/bin/python -m radon cc app tests migrations -s -a
   ```

5. Run `radon` maintainability index:

   ```bash
   ./.venv/bin/python -m radon mi app tests migrations
   ```

---

## 🧠 How To Read The Results In This Repo

### `pylint`

Default `pylint` is useful, but this repo has a few framework patterns that create extra noise:

- Alembic dynamic APIs such as `alembic.context` and `alembic.op`
- SQLAlchemy dynamic helpers such as `func.now()`
- ORM model classes that look unusual to generic lint rules

That means raw `pylint` output should be interpreted in groups:

| Finding group | How to treat it first |
| --- | --- |
| Alembic / SQLAlchemy dynamic API warnings | Review carefully, but expect some false positives |
| Small code-smell findings (`useless-return`, readability issues, genuinely confusing names) | Fix first |
| Missing docstrings | Treat as style policy, not runtime risk |
| ORM model convention noise (`too-few-public-methods`) | Usually low priority |

### `radon`

`radon` gives a different kind of signal:

- high cyclomatic complexity usually means a block is doing too many branches or checks at once
- maintainability index gives a rough file-level health score

In this project, the most complex blocks tend to be large contract tests rather than the core application runtime. That is a useful refactoring signal, but it is not the same thing as a production bug.

The shipped `.pylintrc` intentionally suppresses the noisiest framework-specific warnings first so the remaining output is easier to trust:

- Alembic dynamic member lookups
- SQLAlchemy `func.now()` false positives
- low-value docstring noise
- test bootstrap import-position noise

---

## 🔍 Repo-Specific Learning Points

These are the practical patterns that showed up during the local analysis work:

### Framework-aware linting matters

Running `pylint` with no project-specific tuning can make the report look worse than the runtime reality, especially in:

- `migrations/`
- SQLAlchemy model files in `app/models/`

That is a good lesson for school projects too: a linter is only helpful when its rules fit the technology stack.

### Large contract tests can become complexity hotspots

The biggest `radon cc` scores came from full CRUD contract tests that validate many steps in one function. Those tests are still valuable, but they are strong candidates for splitting into smaller focused cases such as:

- create/list
- get by id
- update
- delete
- negative paths

### Maintainability should be interpreted with context

`radon mi` is helpful as a broad health signal, but it should be read together with:

- test coverage
- readability
- whether a hotspot is in runtime code or test code

---

## ✅ Recommended Improvement Order

If static-analysis cleanup becomes a follow-up task, this is the practical order:

1. add a project-level `pylint` baseline so framework noise stops hiding the real signal
2. fix the small real code-smell findings first
3. split the highest-complexity contract tests into smaller focused tests
4. decide a docstring policy for app code versus tests
5. add framework-aware suppressions where the tool misunderstands the stack
6. only consider CI lint enforcement after the local baseline is stable

This order keeps effort proportional to value.

---

## 🪜 Step-By-Step Cleanup Path

Detailed execution records now live in [docs/static-analysis/](./static-analysis/README.md).

Tracked steps:

1. [Step 1 - `pylint` baseline](./static-analysis/step-1-pylint-baseline.md)
2. [Step 2 - remaining `pylint` findings](./static-analysis/step-2-remaining-pylint-findings.md)
3. [Step 3 - `radon` complexity hotspots](./static-analysis/step-3-radon-complexity-hotspots.md)
4. [Step 4 - docstring policy](./static-analysis/step-4-docstring-policy.md)
5. [Step 5 - framework-aware suppressions](./static-analysis/step-5-framework-aware-suppressions.md)
6. [Step 6 - CI enforcement decision](./static-analysis/step-6-ci-enforcement-decision.md)
7. [Step 7 - `radon` maintenance policy](./static-analysis/step-7-radon-maintenance-policy.md)

---

## 📊 Current Snapshot

At the current stage of this guide:

- Step 1 is complete
- Step 2 is complete
- Step 3 is complete
- Step 4 is complete
- Step 5 is complete
- Step 6 is complete
- Step 7 is complete
- `radon mi` remains healthy overall
- the biggest complexity signals are in large contract tests, not in core runtime code
- the remaining `radon cc` results are now governed by a documented A/B maintenance policy

This makes the current cleanup path practical and contained rather than open-ended.

---

## 🚫 What This Guide Does Not Change

This guide does **not** mean:

- `pylint` is currently a required CI gate
- `radon` is part of the deployment workflow
- static analysis replaces runtime validation

Current decision:

- static analysis remains intentionally local
- CI enforcement is deferred unless the team later decides the extra gate is worth maintaining

The current project validation baseline remains:

- contract tests
- migrations
- runtime checks
- Docker lifecycle
- Kubernetes/Istio lifecycle

See [LIFECYCLE_VALIDATION.md](./LIFECYCLE_VALIDATION.md) for that end-to-end proof.

---

## 🔗 Related Documents

- [QUALITY.md](./QUALITY.md)
- [LIFECYCLE_VALIDATION.md](./LIFECYCLE_VALIDATION.md)
- [MIGRATIONS.md](./MIGRATIONS.md)
- [DEVELOPMENT_LOG.md](./DEVELOPMENT_LOG.md)

# Static Analysis Guide

> How to use default `pylint` and default `radon` as the primary Python analysis baseline in this project, with tests and the other quality tools acting as supporting layers.

---

## 🎯 Goal

Static analysis is useful here for a different reason than tests:

- tests answer whether the API behaves correctly
- static analysis helps us inspect maintainability, consistency, and code-smell signals

This project already treats tests as part of the finished baseline. Static analysis adds the main non-runtime cleanup signal, and the primary tools for that job are default `pylint` and default `radon`.

The supporting tools in the broader quality stack still matter, but they are refinements around that Python baseline rather than substitutes for it.

For the runtime and CI validation baseline, see [QUALITY.md](./QUALITY.md).

---

## 🧰 Tools Used

| Tool       | What it helps answer                                                        | What it does **not** prove                   |
| ---------- | --------------------------------------------------------------------------- | -------------------------------------------- |
| `pylint`   | Are there style problems, suspicious patterns, or easy-to-miss code smells? | That the API works at runtime                |
| `radon cc` | Which functions or tests are becoming complex?                              | That complex code is automatically wrong     |
| `radon mi` | How maintainable each file looks at a high level                            | That a high MI score means design is perfect |

The useful mindset is:

- use tests to confirm behavior
- use default `pylint` and default `radon` to drive cleanup and refactoring
- use the rest of the tooling stack to refine formatting, text hygiene, and infrastructure validation

---

## ▶️ How To Run Locally

1. Activate the project virtual environment and install the normal dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```

2. The static-analysis tools are included in `requirements-dev.txt`. If the environment was created before those dependencies were added, refresh it with:

   ```bash
   ./.venv/bin/pip install -r requirements-dev.txt
   ```

3. Run **default** `pylint` across the repository's Python quality scope (`app/`, `tests/`, `migrations/`):

   ```bash
   ./.venv/bin/python -m pylint --rcfile=/dev/null app tests migrations
   ```

4. Run default `radon` cyclomatic complexity:

   ```bash
   ./.venv/bin/python -m radon cc app tests migrations
   ```

5. Run default `radon` maintainability index:

   ```bash
   ./.venv/bin/python -m radon mi app tests migrations
   ```

---

## 🧠 How To Read The Results In This Repo

### `pylint`

Default `pylint` is the real baseline, but this repo has a few framework patterns that create extra noise:

- Alembic dynamic APIs such as `alembic.context` and `alembic.op`
- SQLAlchemy dynamic helpers such as `func.now()`
- ORM model classes that look unusual to generic lint rules

That means raw `pylint` output should be interpreted in groups, not dismissed:

| Finding group                                                                               | How to treat it first                             |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Alembic / SQLAlchemy dynamic API warnings                                                   | Review carefully, but expect some false positives |
| Small code-smell findings (`useless-return`, readability issues, genuinely confusing names) | Fix first                                         |
| Missing docstrings                                                                          | Treat as style policy, not runtime risk           |
| ORM model convention noise (`too-few-public-methods`)                                       | Usually low priority                              |

### `radon`

`radon` gives a different kind of signal:

- high cyclomatic complexity usually means a block is doing too many branches or checks at once
- maintainability index gives a rough file-level health score

In this project, the most complex blocks tend to be large contract tests rather than the core application runtime. That is a useful refactoring signal, but it is not the same thing as a production bug.

---

## 🔍 Repo-Specific Learning Points

These are the practical patterns that showed up during the local analysis work:

### Framework-aware linting matters

Running `pylint` with no project-specific tuning can make the report look worse than the runtime reality, especially in:

- `migrations/`
- SQLAlchemy model files in `app/models/`

That is a good lesson for school projects too: start from the default report, then separate genuine issues from framework noise instead of assuming the default tool is wrong.

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

1. run default `pylint` and default `radon` and group the findings by type
2. fix the small real code-smell findings first
3. fix or consciously justify the naming, docstring, and import-structure findings
4. split the highest-complexity contract tests into smaller focused tests
5. isolate genuine framework false positives only after the default report is understood
6. move CI enforcement in only after the default baseline is intentionally worked down

This order keeps the primary goal clear: fix what the default Python analysis tools report first, then refine the rest of the repo around that core.

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
- the GitHub Actions workflow now runs `pylint` and `radon` in a dedicated Python-quality job
- that Python-quality job now uses the default `pylint` and default `radon` commands as the repo baseline

This makes the current cleanup path practical and contained rather than open-ended.

---

## 🚫 What This Guide Does Not Change

This guide does **not** mean:

- static analysis replaces runtime validation
- Ruff should absorb Pylint policy rules
- Ruff should absorb Radon complexity/maintainability signals
- the supporting repo-quality tools are unimportant

The current project validation baseline still includes:

- contract tests
- migrations
- runtime checks
- Docker lifecycle
- Kubernetes/Istio lifecycle

Static analysis now runs in CI as a separate layer because the repo baseline is stable enough to maintain that gate without mixing responsibilities. See [LIFECYCLE_VALIDATION.md](./LIFECYCLE_VALIDATION.md) for the end-to-end runtime proof.

---

## 🔗 Related Documents

- [QUALITY.md](./QUALITY.md)
- [LIFECYCLE_VALIDATION.md](./LIFECYCLE_VALIDATION.md)
- [MIGRATIONS.md](./MIGRATIONS.md)
- [DEVELOPMENT_LOG.md](./DEVELOPMENT_LOG.md)

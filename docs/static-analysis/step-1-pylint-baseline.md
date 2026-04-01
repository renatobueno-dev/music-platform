# 🔧 Static Analysis — Step 1: Pylint Baseline

## 📌 Context

The first full `pylint` run was noisy enough to hide the real issues.

Initial signal:

- 134 findings
- score `6.24 / 10`

The biggest groups were:

- Alembic dynamic API warnings
- SQLAlchemy dynamic-call warnings
- test bootstrap import-position warnings
- docstring noise

That meant the raw report was not yet a good cleanup queue.

## 🎯 Scope decision

Before fixing code, create a repo-level baseline so `pylint` fits the actual stack.

This step includes:

- adding a repo-level [`.pylintrc`](../../.pylintrc)
- pinning `pylint` and `radon` in [requirements-dev.txt](../../requirements-dev.txt)
- documenting the static-analysis workflow in [STATIC_ANALYSIS.md](../STATIC_ANALYSIS.md)

## ✅ Validation target

After the baseline is added:

- framework noise should drop sharply
- the remaining findings should be small enough to trust
- the output should primarily reflect real cleanup work, not tool mismatch

## 🧩 Baseline choices

The baseline intentionally suppresses these noisy groups first:

- missing module/function/class docstrings
- ORM `too-few-public-methods`
- test bootstrap import-order noise
- Alembic dynamic member lookups through `context.*` and `op.*`
- naming exceptions required by Alembic metadata and `SessionLocal`
- SQLAlchemy `func.now()` false positives through `not-callable`

This keeps meaningful findings such as:

- `line-too-long`
- `useless-return`

## 🏁 Completion criteria

Step 1 is complete when:

- the repo has a usable `pylint` baseline
- static-analysis tools are part of the dev dependency path
- `pylint` output is short enough to serve as a real action list

## ⚠️ Errors and issues observed

The main issue in Step 1 was not broken application code. It was poor signal quality from the raw lint run.

Observed problems:

- Alembic dynamic member lookups produced repeated `no-member` errors in:
  - `migrations/env.py`
  - `migrations/versions/abff2336451a_baseline_schema.py`
- SQLAlchemy `func.now()` produced repeated `not-callable` false positives in model files.
- test bootstrap setup produced import-order noise in `tests/conftest.py`.
- docstring requirements generated a large volume of low-value noise for this repo.
- the raw report also surfaced a few real issues, but they were easy to miss inside the noise:
  - `useless-return` in `app/routes/playlists.py`
  - `line-too-long` in the Alembic baseline revision
- coding/implementation issues during the step:
  - there was no existing repo-level `pylint` baseline, so the setup had to start from zero
  - `zsh` globbing required the `generated-members=context.*,op.*` experiment to be quoted during local testing
  - `generated-members` solved the Alembic member noise, but it did not solve SQLAlchemy `func.now()` `not-callable` noise, so that part needed a separate lint-baseline decision

## 📝 Step execution notes

- Step completed in the current cycle.
- Result after baseline:

  | Run state | Findings | Score |
  | --- | ---: | ---: |
  | Before baseline | 134 | 6.24 / 10 |
  | After baseline | 5 | 9.92 / 10 |

- Remaining findings after this step:
  - `useless-return` in `app/routes/playlists.py`
  - 4 `line-too-long` findings in the Alembic baseline revision

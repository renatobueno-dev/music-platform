# 🧩 Static Analysis — Step 5: Framework-Aware Suppressions

## 📌 Context

After the repo-level baseline and selective cleanup passes, the remaining lint policy question was how broad the suppressions should stay.

The goal of this step is not to hide warnings. It is to move the remaining framework-specific noise into the smallest practical boundary.

## 🎯 Scope decision

Keep the Alembic and SQLAlchemy suppressions framework-aware and intentional instead of muting those rules globally.

Target areas:

- Alembic `context.*` and `op.*` dynamic members
- SQLAlchemy `func.now()` false positives in ORM models
- declarative-model `too-few-public-methods` noise

## ✅ Validation target

After this step:

- Alembic `no-member` noise should stay handled through a targeted config path
- ORM-only suppressions should live with the ORM model files rather than as broad global disables
- the full-project `pylint` run should remain clean

## 🏁 Completion criteria

Step 5 is complete when framework-specific lint misunderstandings are handled in the narrowest practical place and the repo still passes `pylint`.

## ⚠️ Errors and issues observed

This step exposed which parts of the earlier lint baseline were broader than necessary.

Observed issues and decisions:

- Alembic `no-member` handling through `generated-members=context.*,op.*` already worked well and did not need to move into file-local suppressions.
- Re-enabling `not-callable` and `too-few-public-methods` showed that the remaining noise was concentrated in declarative model files, not across the repo.
- `Mapped[...]` false positives were not reproduced with the current pinned `pylint`/`astroid` toolchain, so no extra suppression was added for that pattern.

Coding and implementation issues during the step:

- the narrowing work needed a probing run with previously disabled checks re-enabled to confirm where the warnings actually came from
- the step ended up being smaller than expected because the current toolchain behaved better on `Mapped[...]` than earlier exploratory runs suggested

## 📝 Step execution notes

- Step completed in the current cycle.
- Global disables were narrowed by moving ORM-only suppressions into:
  - `app/models/base.py`
  - `app/models/song.py`
  - `app/models/playlist.py`
  - `app/models/playlist_song.py`
- The repo-level config kept the targeted Alembic handling through `generated-members=context.*,op.*`.
- Verification result after the refinement:

  | Check                 | Result       |
  | --------------------- | ------------ |
  | full-project `pylint` | `10.00 / 10` |
  | `pytest -q tests`     | passed       |

- Static analysis remains a local quality tool. Runtime validation, tests, migrations, and deployment flow remain the primary project gates.

# 📝 Static Analysis — Step 4: Docstring Policy

## 📌 Context

Before the baseline, missing docstrings were one of the biggest `pylint` groups.

That does not automatically mean the repo needs docstrings everywhere.

## 🎯 Scope decision

Decide the docstring standard intentionally before adding large amounts of text.

Practical direction for this repo:

- prioritize docstrings where logic is non-obvious
- avoid low-value docstrings in simple tests and declarative models

Good candidates for docstrings:

- bootstrap/runtime modules with important assumptions
- non-obvious service helpers
- modules where the reasoning is harder to infer from the code alone

Low-value candidates:

- simple CRUD contract tests
- straightforward ORM model classes
- simple schema classes that already read clearly

## ✅ Validation target

The repo should end with a clear writing standard that improves understanding instead of adding text only to satisfy a generic linter.

## 🏁 Completion criteria

Step 4 is complete when the team can explain:

- where docstrings are expected
- where they are intentionally optional
- why that choice fits this project

## ⚠️ Errors and issues observed

This step was mainly about deciding where extra explanation adds value without turning the repo into docstring noise.

Policy tension resolved in this step:

- avoiding low-value docstrings added only for lint compliance
- while still documenting modules and helpers where reasoning is not obvious

Coding and implementation issues during the step:

- the repo-level `pylint` baseline already suppresses missing-docstring warnings, so this step had to be driven by documentation value rather than by lint pressure
- the service modules mix obvious CRUD helpers with less-obvious relationship and reload behavior, so the main work was deciding where a docstring was worth keeping concise and where it would only restate the code
- tests, schemas, and ORM models were intentionally left mostly unchanged to preserve the selective policy boundary

## 📝 Step execution notes

- Step completed in the current cycle.
- The selected docstring targets were:
  - `app/main.py`
  - `app/database.py`
  - `app/services/song_service.py`
  - `app/services/playlist_service.py`
- The policy stayed intentionally selective:
  - tests were not mass-documented
  - schema classes were not mass-documented
  - ORM models were not mass-documented
- The current lint baseline still suppresses generic missing-docstring warnings, but the repo now has a practical documented standard in code rather than only in prose.

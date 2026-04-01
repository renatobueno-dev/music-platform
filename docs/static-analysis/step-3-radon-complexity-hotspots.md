# 📈 Static Analysis — Step 3: Radon Complexity Hotspots

## 📌 Context

`radon` did not show a broad maintainability problem in the project.

Observed high-level result:

- most blocks ranked `A`
- a smaller group ranked `B`
- only a few ranked `C` or `D`
- maintainability index stayed at `A` across the repo

The biggest complexity signals appeared in large contract tests rather than the runtime code.

## 🎯 Scope decision

Treat the highest-complexity test functions as refactoring candidates before touching lower-value areas.

Main hotspots observed:

- `tests/test_playlists_contract.py`
- `tests/test_songs_contract.py`
- `tests/test_playlist_song_contract.py`

## ✅ Validation target

Refactor large test functions into smaller focused test cases so failures are easier to isolate and the complexity signal improves on rerun.

Examples of better split boundaries:

- create/list
- get by id
- update
- delete
- negative paths

## 🏁 Completion criteria

Step 3 is complete when the main complexity hotspots are broken into smaller readable tests and `radon cc` reflects the reduction.

## ⚠️ Errors and issues observed

This step was focused on readability and maintenance rather than fixing broken behavior, so the main risks were accidental coverage drift and refactor churn.

Hotspots at the start of the step:

- `tests/test_playlists_contract.py` CRUD contract (`D / 22`)
- `tests/test_songs_contract.py` CRUD contract (`C / 19`)
- `tests/test_playlist_song_contract.py` relationship contract (`C / 11`)

Coding and implementation issues during the step:

- the first multi-file patch attempt collided with overlapping edits, so the refactor was reapplied as clean full-file rewrites for the three hotspot files
- the first `radon` pipeline attempt returned `no radon output`, so the verification flow was changed to write JSON to a temporary file before parsing it

Outcome notes:

- splitting the CRUD tests increased the number of test cases, but improved failure isolation and reduced per-function complexity
- the only remaining `radon` hotspot after the refactor was a `B / 9` missing-resource relationship test, which is acceptable for the current cleanup boundary

## 📝 Step execution notes

- Step completed in the current cycle.
- The large CRUD-style contract tests were split into smaller focused cases:
  - create/list
  - get by id
  - update
  - delete
  - link/unlink behaviors
- Verification result after the refactor:

  | Check | Result |
  | --- | --- |
  | `pytest -q tests` | `23 passed` |
  | `pylint` on changed test files | `10.00 / 10` |
  | `radon cc` hotspot result | no remaining `C` or `D` blocks in `tests/` |

- Complexity improvement snapshot:

  | Stage | Hotspot summary |
  | --- | --- |
  | Before Step 3 | `D / 22`, `C / 19`, `C / 11` |
  | After Step 3 | highest remaining hotspot is `B / 9` |

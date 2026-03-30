#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTEST_RUNNER="${ROOT_DIR}/.venv/bin/python"
RUNS="${1:-3}"

if [[ ! -x "${PYTEST_RUNNER}" ]]; then
  echo "Missing virtual environment runner: ${PYTEST_RUNNER}" >&2
  echo "Create it first with: python3 -m venv .venv && ./.venv/bin/pip install -r requirements-dev.txt -r requirements.txt" >&2
  exit 1
fi

if ! [[ "${RUNS}" =~ ^[1-9][0-9]*$ ]]; then
  echo "Invalid runs value: ${RUNS}. Use a positive integer." >&2
  exit 1
fi

cd "${ROOT_DIR}"

for run in $(seq 1 "${RUNS}"); do
  echo "--- local test verification run ${run}/${RUNS} ---"
  "${PYTEST_RUNNER}" -m pytest -q --cache-clear
done

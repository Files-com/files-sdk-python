#!/usr/bin/env bash
# Checks this package without changing it: formatting, lint, types and the
# unit tests (see scripts/tasks.py). PYTHON chooses the interpreter. The
# generated model tests need the Files.com mock server named in tests/base.py.
set -euo pipefail
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" scripts/tasks.py check

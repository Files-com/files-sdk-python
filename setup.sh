#!/usr/bin/env bash
# The generator runs this after writing the package. It formats the sources
# with the pinned Black before anything tests, builds or publishes them;
# test.sh only checks the formatting. PYTHON chooses the interpreter.
set -euo pipefail
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" scripts/tasks.py format

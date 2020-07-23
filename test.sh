#!/usr/bin/env sh

# Execute running tests from same directory as current script
cd "$(dirname "$0")"

python3 -m unittest discover
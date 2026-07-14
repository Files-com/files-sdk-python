#!/usr/bin/env bash

# Execute running tests from same directory as current script
cd "$(dirname "$0")"

# Generated API tests expect the Files.com mock server to be running.

# Install dependencies
pip3 install --user "flake8~=6.1.0" "requests>=2.20" "black~=23.9.0" "pyright==1.1.347" "requests-toolbelt==1.0.0"

python3 -m black .
python3 -m flake8 files_sdk && python3 -m pyright && python3 -m unittest discover

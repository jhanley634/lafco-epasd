#! /usr/bin/env bash
# Copyright 2024 John Hanley. MIT licensed.

# Activates this repo's virtual environment before running Python.

TOP_DIR=$(git rev-parse --show-toplevel)
REPO=$(basename ${TOP_DIR})
ACTIVATE=~/.venv/${REPO}/bin/activate
test -r ${ACTIVATE} || {
    echo "Please run 'make venv' to create a virtual environment."
    exit 1
}
source ~/.venv/${REPO}/bin/activate

exec python "$@"

#!/usr/bin/env bash

# This script will run unit tests (when we have some)
# For now it only checks that the python code formatting is nice
# It will be run by some CI job later.

cd `dirname "$0"`

flake8 ../.. --exclude ../venv/

if [ $? -ne 0 ]; then
    echo
    echo "Syntax check failed"
    exit 1
else
    echo
    echo "Syntax check succeeded"
    exit 0
fi

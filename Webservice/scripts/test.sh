#!/usr/bin/env bash

# This script will run unit tests (when we have some)
# For now it only checks that the python code formatting is nice
# It will be run by some CI job later.

cd `dirname "$0"`/../../

Webservice/venv/bin/flake8 . --exclude Webservice/venv/

if [ $? -ne 0 ]; then
    echo
    echo "Code formatting check failed."
    exit 1
else
    echo
    echo "Code formatting check succeeded."
    exit 0
fi

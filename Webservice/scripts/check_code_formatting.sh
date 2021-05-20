#!/usr/bin/env bash

# This script checks if the python code is properly formatted


cd `dirname "$0"`/../../


echo
echo "========================= Checking the code formatting ========================="
echo

# Check the code formatting
Webservice/venv/bin/flake8 --max-line-length 90 . --exclude Webservice/venv/

if [ $? -ne 0 ]; then
    echo
    echo "Code formatting check failed."
    exit 1
else
    echo
    echo "Code formatting check succeeded."
    echo 0
fi

#!/usr/bin/env bash

# This script runs unit tests
# and checks the code formatting

cd `dirname "$0"`/../../


# Run the tests

Webservice/venv/bin/pytest colorization/src/tests.py
TEST_RESULT=$?

echo
echo "========================= Checking the code formatting ========================="
echo

# Check the code formatting
Webservice/venv/bin/flake8 . --exclude Webservice/venv/
CODEFORMAT_RESULT=$?

if [ $CODEFORMAT_RESULT -ne 0 ]; then
    echo
    echo "Code formatting check failed."
    exit 1
else
    echo
    echo "Code formatting check succeeded."
fi

exit $TEST_RESULT


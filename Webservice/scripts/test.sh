#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/../../

# Run the tests
Webservice/venv/bin/pytest colorization/src/tests.py --cov=. --cov-config=.coveragerc

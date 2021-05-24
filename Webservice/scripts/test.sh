#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/../../

# Run the tests
Webservice/venv/bin/pytest colorization/src/tests.py Webservice/test_web.py --cov=. --cov-config=.coveragerc

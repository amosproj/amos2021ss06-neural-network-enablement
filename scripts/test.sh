#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/..

# Run the tests

# for the webservice
venv/bin/pytest webservice/test_web.py --cov=. --cov-config=.coveragerc --cov-report='' --capture=tee-sys

# for the colorization
venv/bin/pytest colorization/tests.py --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys

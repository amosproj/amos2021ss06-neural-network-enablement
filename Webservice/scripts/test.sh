#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/../../

# Run the tests

# for the webservice
Webservice/venv/bin/pytest Webservice/test_web.py --cov=. --cov-config=.coveragerc

# for the pipeline unittests
Webservice/venv/bin/pytest colorization/src/tests.py -k 'PipelineTests' --cov=. --cov-config=.coveragerc --cov-append

# for the pipeline functional tests
Webservice/venv/bin/pytest colorization/src/tests.py -k 'FunctionalTest' --cov=. --cov-config=.coveragerc --cov-append

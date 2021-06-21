#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/..

# Run the tests

# for the webservice
venv/bin/pytest webservice/test_web.py --cov=. --cov-config=.coveragerc --cov-report='' --capture=tee-sys
WEB_RET=$?

# for each pipeline unittest
venv/bin/pytest colorization/tests.py -k 'PipelineTests' --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
STEPS_RET=$?

# for the pipeline functional tests
venv/bin/pytest colorization/tests.py -k 'FunctionalTest' --cov=. --cov-config=.coveragerc --cov-append --capture=tee-sys
PIPELINE_RET=$?


if [ $WEB_RET -ne 0 ] || [ $STEPS_RET -ne 0 ] || [ $PIPELINE_RET -ne 0 ]; then
    # exit failure if any of the tests failed
    exit 1
fi

#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/..

# Run the tests

# for the webservice
venv/bin/pytest webservice/test_web.py --cov=. --cov-config=.coveragerc --cov-report='' --capture=tee-sys

# for each pipeline unittest
venv/bin/pytest colorization/tests.py -k 'step_preprocess'  --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
venv/bin/pytest colorization/tests.py -k 'step_colorize'    --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
venv/bin/pytest colorization/tests.py -k 'step_postprocess' --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys

# for the pipeline functional tests
venv/bin/pytest colorization/tests.py -k 'FunctionalTest'   --cov=. --cov-config=.coveragerc --cov-append --capture=tee-sys

#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/../../

# Run the tests

# for the webservice
Webservice/venv/bin/pytest Webservice/test_web.py --cov=. --cov-config=.coveragerc --cov-report='' --capture=tee-sys

# for each pipeline unittest
Webservice/venv/bin/pytest colorization/src/tests.py -k 'step_preprocess'  --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
Webservice/venv/bin/pytest colorization/src/tests.py -k 'step_colorize'    --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
Webservice/venv/bin/pytest colorization/src/tests.py -k 'step_postprocess' --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys

# for the pipeline functional tests
Webservice/venv/bin/pytest colorization/src/tests.py -k 'FunctionalTest'   --cov=. --cov-config=.coveragerc --cov-append --capture=tee-sys

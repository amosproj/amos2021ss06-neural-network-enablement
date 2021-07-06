#!/usr/bin/env bash

# This script exectutes all unit tests


cd `dirname "$0"`/..

# Run the tests

# for the webservice
venv/bin/pytest webservice/test_web.py --cov=. --cov-config=.coveragerc --cov-report='' --capture=tee-sys
WEB_RET=$?

# for the video merge and splite functional tests
venv/bin/pytest colorization/tests.py -k 'SplitAndMergeTestsForVideo' --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
VIDEO_RET=$?

# for each pipeline unittest
venv/bin/pytest colorization/tests.py -k 'PipelineTests' --cov=. --cov-config=.coveragerc --cov-append --cov-report='' --capture=tee-sys
STEPS_RET=$?

# for the pipeline functional tests
venv/bin/pytest colorization/tests.py -k 'FunctionalTest' --cov=. --cov-config=.coveragerc --cov-append --capture=tee-sys
PIPELINE_RET=$?


if [ $WEB_RET -ne 0 ]; then
    echo "Webservice test failed with status $WEB_RET."
    exit 1
elif [ $VIDEO_RET -ne 0 ]; then
    echo "Video merge/split test failed with status $VIDEO_RET."
    exit 1
elif [ $STEPS_RET -ne 0 ]; then
    echo "Pipeline steps test failed with status $STEPS_RET."
    exit 1
elif [ $PIPELINE_RET -ne 0 ]; then
    echo "Pipeline integrations test failed with status $PIPELINE_RET."
    exit 1
fi

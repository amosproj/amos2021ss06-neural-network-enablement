#!/usr/bin/env bash

# Run script to start the webservice

# ===============================================================

cd `dirname "$0"`/..

if [[ ! -d "venv" ]]; then
    echo "Did not find virtual environment, did you run the setup.sh script?"
    exit 1
fi


echo "======================================================================"
echo "Starting webservice"
echo "You can shut it down using Ctrl+C"
echo "======================================================================"

if [ $HOSTNAME != "davinci-mini" ]; then
    (sleep 1; xdg-open "http://localhost:5000") &
fi

venv/bin/python3 webservice/app.py

#!/usr/bin/env bash

# Run script to generate documentation

# ===============================================================

cd `dirname "$0"`/..

if [[ ! -d "venv" ]]; then
    echo "Did not find virtual environment, did you run the setup.sh script?"
    exit 1
fi


echo "======================================================================"
echo "Generating Documentation"
echo "======================================================================"


# enter virtual environment
source venv/bin/activate

sphinx-apidoc -o sphinx/source/ colorization
sphinx-apidoc -o sphinx/source/ webservice

cd sphinx
make clean
make html
cd ..

rm -r docs/*
cp -r sphinx/build/html/* docs/
cp -r sphinx/build/html/.buildinfo docs/

# leave virtual environment
deactivate

if [ $HOSTNAME != "davinci-mini" ]; then
    xdg-open docs/index.html
fi


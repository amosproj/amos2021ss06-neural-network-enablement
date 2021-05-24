#!/usr/bin/env bash

# This script checks, if the acl library can be imported in python.
# It will only work on the ATLAS device

python3 -c "import acl"

if [ $? -eq 0 ]; then
    echo "Success. Acl was successfully imported"
    exit 0
fi

# Try with environment variables set
export PYTHONPATH=$PYTHONPATH:$HOME/Ascend/ascend-toolkit/latest/pyACL/python/site-packages/acl

echo
echo "Trying again"

python3 -c "import acl"

if [ $? -eq 0 ]; then
    echo
    echo "Found acl library. You need to set some environment variables."
    echo ""
    echo "As user HwHiAiUser copy this to the bottom of ~/.bashrc, Then run 'source ~/.bashrc' and run this script again:"
    echo ""
    echo "export PYTHONPATH=$PYTHONPATH:$HOME/Ascend/ascend-toolkit/latest/pyACL/python/site-packages/acl"
    exit 0
else
    echo
    echo "Didn't find acl library."
    echo "Are you running this on the Atlas Board?"
    echo "Did you install the acltoolkit?"
    exit 1
fi

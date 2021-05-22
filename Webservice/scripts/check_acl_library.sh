#!/usr/bin/env bash

# This script checks, if the acl library can be imported in python.
# It will only work on the ATLAS device

python3 -c "import acl"

if [ $? -eq 0 ]; then
    echo "Success. Acl was successfully imported"
    exit 0
fi

# Try after setting a few environment variables
export PYTHONPATH=$PYTHONPATH:$HOME/Ascend/ascend-toolkit/latest/pyACL/python/site-packages/acl

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Ascend/ascend-toolkit/latest/acllib_centos7.6.x86_64/acllib/lib64
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Ascend/ascend-toolkit/latest/x86_64-linux_gcc7.3.0/atc/lib64
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Ascend/ascend-toolkit/latest/toolkit/lib64


echo
echo "Trying again"

python3 -c "import acl"

if [ $? -eq 0 ]; then
    echo
    echo "Found acl library. You need to set some environment variables. (as user HwHiAiUser)"
    echo "Look in the script Webservice/check_acl_library.sh and copy the four exports."
    echo "to the bottom of ~/.bashrc, Then run 'source ~/.bashrc' and run this script again."
    exit 0
else
    echo
    echo "Didn't find acl library."
    echo "Are you running this on the Atlas Board?"
    echo "Did you install the acltoolkit?"
    exit 1
fi

#!/usr/bin/env bash

# This script checks, if the acl library can be imported in python.
# It will only work on the ATLAS device

export PYTHONPATH=$PYTHONPATH:$HOME/Ascend/ascend-toolkit/latest/pyACL/python/site-packages/acl

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Ascend/ascend-toolkit/latest/acllib_centos7.6.x86_64/acllib/lib64
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Ascend/ascend-toolkit/latest/x86_64-linux_gcc7.3.0/atc/lib64
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Ascend/ascend-toolkit/latest/toolkit/lib64

python3 -c "import acl"

if [ $? -eq 0 ]; then
    echo "Success"
    exit 0
else
    exit 1
fi

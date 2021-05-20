#!/usr/bin/env bash

# ===============================================================
# Setup script to initialize the virtual environment and update
# the dependencies on an Ubuntu based system
# ===============================================================

# config
SUPPORTED_OS="Ubuntu 18.04"
SUPPORTED_PYTHON="3.7.5"

# command line arguments

# first argument
# --yes: answer yes_or_no function with Y (used by ci)
YES=$1


# ===============================================================

# helper
function yes_or_no {
    # don't run interactively
    if [[ "$YES" == "--yes" ]]; then
        echo "$* [y/n]: Y"
        return 0
    fi

    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0  ;;
            [Nn]*) echo "Aborted" ; return  1 ;;
        esac
    done
}

# ===============================================================

# beginning of script
echo "========================"
echo "Welcome!"
echo "This script will setup the environment for the webservice."
echo "If you're already set up, it will update the dependencies."
echo "========================"


# lsb_release is not available on Windows
which "lsb_release" > /dev/null
if [ $? -ne 0 ]; then
    echo
    echo "This script shall be run on $SUPPORTED_OS."
    echo "Couldn't detect your OS."
    echo "If you think this is a mistake, please make sure, the command 'lsb_release' is available."
    echo "On Debian/Ubuntu you can do this using 'sudo apt install lsb-release'."
    echo

    yes_or_no "Do you want to continue at your own risk?" || exit 1

else
    # check os version
    os=`lsb_release -d`

    if [[ "$os" != *"$SUPPORTED_OS"* ]]; then
        echo
        echo "This script shall be run on $SUPPORTED_OS."
        echo "You are running ${os:13}"
        echo

        yes_or_no "Do you want to continue at your own risk?" || exit 1
    fi
fi

echo


# check python version
py_version=`python3 --version`

if [[ "$py_version" != *"$SUPPORTED_PYTHON" ]]; then
    echo
    echo "The supported python version is $SUPPORTED_PYTHON."
    echo "You have $py_version. Have you installed version $SUPPORTED_PYTHON and made it the default?"
    echo "(When you type 'python3' a python shell with version $SUPPORTED_PYTHON should open)"
    echo

    yes_or_no "Do you want to continue with $py_version at your own risk?" || exit 1
fi

cd `dirname "$0"`/..

# set up virtualenv if necessary
if [[ -d "venv" ]]; then
    echo
    echo "Found existing virtual environment."
else
    echo
    echo "Creating virtual environment..."
    echo

    # install virtualenv if not available
    which "virtualenv" > /dev/null
    if [ $? -ne 0 ]; then
        python3 -m pip install virtualenv --user
    fi

    python3 -m virtualenv --python=python3 venv

    if [ $? -ne 0 ]; then
        echo "Something went wrong when creating the virtual environment."
        echo
        echo "A virtual environment is expected at 'Webservice/venv/'"
        echo "You can follow this guide to set it up manually:"
        echo "https://docs.python.org/3/library/venv.html"
        exit 1
    fi
fi

echo
echo "Updating dependencies..."
echo

venv/bin/python3 -m pip install --upgrade pip
venv/bin/python3 -m pip install --upgrade -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "Something went wrong updating the dependencies. It was tested with $SUPPORTED_OS."
    echo "Please check manually."
    exit 1
fi

echo
echo "Seems like everything went well."
echo "You can now start the webservice by executing run.sh."

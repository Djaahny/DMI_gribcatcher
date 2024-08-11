#!/bin/bash

source venv/bin/activate

# Check for the first argument
if [ -z "$1" ]; then
    echo "Usage: dmi_util.sh build, run, test, peek"
    exit 1
fi

# Execute commands based on the argument
case "$1" in
    *)
        python3 DMI_EDS2grib.py
        ;;
esac

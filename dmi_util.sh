#!/bin/bash

# Check for the first argument
if [ -z "$1" ]; then
    echo "Usage: dmi_util.sh build, run, test, peek"
    exit 1
fi

# Execute commands based on the argument
case "$1" in
    build)
        echo "Building Docker image..."
        docker build -t dmi_gribcatcher .
        ;;
    remove)
        echo "Removing Docker image..."
        docker rmi dmi_gribcatcher -f
        ;;
    run)
        echo "Running Docker container..."
        docker run dmi_gribcatcher
        ;;
    test)
        echo "Building and running Docker container..."
        ./dmi_util.sh build
        ./dmi_util.sh run
        ;;
    peek)
        echo "Running Docker container interactively..."
        docker run -it dmi_gribcatcher bash
        ;;
    *)
        echo "Invalid argument: $1"
        echo "Usage: dmi_util.sh build, run, test, peek"
        exit 1
        ;;
esac

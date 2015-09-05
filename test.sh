#!/bin/sh
# Test the scripts and sorno python library in sorno-py-scripts
set -o errexit

./test_sorno.sh "$@"
./test_scripts.sh "$@"

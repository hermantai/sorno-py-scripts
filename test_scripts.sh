#!/bin/sh
# Test the python scripts in sorno-py-scripts

set -o errexit
set -o xtrace

python -m unittest discover scripts $@

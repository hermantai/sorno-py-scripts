#!/bin/sh
# Test the sorno python library

set -o errexit
set -o xtrace

python -m unittest discover sorno $@

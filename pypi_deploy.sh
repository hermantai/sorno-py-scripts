#!/bin/sh
# Deploy sorno-py-scripts to PyPI using twine

set -o errexit
set -o xtrace

python setup.py bdist_egg sdist upload

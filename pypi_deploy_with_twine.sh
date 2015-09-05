#!/bin/sh
# Deploy sorno-py-scripts to PyPI using twine

set -o errexit
set -o xtrace

python setup.py bdist_egg sdist
# The distributions are in the dist folder, so get the two filenames from that
# folder by simply looking at the timestamps of the files. Pick the two latest
# files to be uploaded (the .egg and the .tar.gz files)
twine upload $(ls -tr dist/ |tail -2|sed s:^:dist/:)

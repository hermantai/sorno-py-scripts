#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

dependency_libs = [
    "beautifulsoup4",
    "dropbox",
    "feedparser",
    "gitpython",
    "oauth2client", # for google_api_python_client
    "google_api_python_client",
    "humanfriendly",
    "humanize",
    "lxml",
    # If this does not work, try python3 -m pip install Pillow
    # https://stackoverflow.com/questions/54496599/pip-cant-install-pillow
    "pillow", # PIL
    "PyPDF2",
    "python_dateutil",
    "python_twitter",
    "requests",
    "six",
    "tzlocal",
    "sornobase",
]

script_dir = os.path.dirname(os.path.realpath(__file__))

with open("README.rst", "r") as f:
    readme_text = f.read()

setup(
    name="sorno-py-scripts",
    version="0.48.8",
    description="Herman Tai's python scripts all prefixed with \"sorno_\"",
    long_description=readme_text,
    author="Herman Tai",
    author_email="htaihm@gmail.com",
    license="APLv2",
    url="https://github.com/hermantai/sorno-py-scripts",
    download_url="https://github.com/hermantai/sorno-py-scripts/archive/master.zip",
    packages=[
        "sorno",
    ],
    py_modules=[
        "sorno",
    ],
    scripts=[
        os.path.join("scripts", f)
        for f in os.listdir(os.path.join(script_dir, "scripts"))
        if f.endswith(".py")
    ],  # include all py scripts under the scripts directory
    requires=dependency_libs,
    install_requires=dependency_libs,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
)

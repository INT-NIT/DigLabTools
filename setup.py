#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from setuptools import setup, find_packages
import os

# Extract central version information
with open(os.path.join(os.path.dirname(__file__), "redcap_bridge/VERSION")) as version_file:
    version = version_file.read().strip()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name="DigLabTools",
    version=version,
    packages=find_packages(),
    package_data={
        # If any package contains *.json or *.csv files, include them:
        "": ["*.json", '*.csv', '*.zip'],
    },
    data_files=[('DigLabTools', ['redcap_bridge/VERSION', 'README.md', 'requirements.txt'])],
    author="Julia Sprenger, Jeremy Garcia",
    description="Tools to interact with the DigLab metadata collection standard",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',
    install_requires=requires,
    include_package_data=True,
    python_requires='>=3.8',
    extras_require={
        'test': ['pytest']
    },
    entry_points={
        "console_scripts": [
            "RedCapBridge=redcap_bridge.cli:main",
        ],
    }
)

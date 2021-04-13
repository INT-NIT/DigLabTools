#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from setuptools import setup, find_packages
import os

# Extract central version information
with open(os.path.join(os.path.dirname(__file__), "VERSION")) as version_file:
    version = version_file.read().strip()

with open('requirements.txt') as f:
    requires = f.read().splitlines()


setup(
    name="DigLabTools",
    version=version,
    packages=find_packages(),
    package_data={
        # If any package contains *.json or *.csv files, include them:
        "": ["*.json", '*.csv','*.zip'],
    },

    author="Julia Sprenger, Jeremy Garcia",
    description="Tools to interact with the DigLab metadata collection standard",
    license='MIT',
    install_requires=requires,
    include_package_data=True,
    python_requires='>=3.6',
    extras_require={
        'test': ['pytest']
    }
)

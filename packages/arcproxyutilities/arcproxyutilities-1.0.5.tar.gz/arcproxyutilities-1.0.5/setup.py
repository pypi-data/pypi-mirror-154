#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from codecs import open
import setuptools

# TODO: Confirm this is the right version number you want and it matches your
# HISTORY.rst entry.

VERSION = '1.0.5'

# The full list of classifiers is available at
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
]

# TODO: Add any additional SDK dependencies here
DEPENDENCIES = [
    'kubernetes==11.0.0',
    'pycryptodome==3.12.0',
]

with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()
with open('History.rst', 'r', encoding='utf-8') as f:
    HISTORY = f.read()

setuptools.setup(
    name='arcproxyutilities',
    version=VERSION,
    description='Arc proxy utilities for provisioned clusters',
    author='Microsoft Corporation',
    author_email='k8connect@microsoft.com',
    url='https://msazure.visualstudio.com/CloudNativeCompute/_git/ArcProxyUtilities',
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=CLASSIFIERS,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=DEPENDENCIES
)
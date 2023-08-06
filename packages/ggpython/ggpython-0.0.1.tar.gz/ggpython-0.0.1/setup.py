# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## setup.py
# ## 
# ##############################################################################
# =============================================================================>
# imports default
import os
from importlib import resources

# =============================================================================>
# imports third party
from setuptools import setup, find_packages

# =============================================================================>
# imports local

# =============================================================================> 
# readme
with open('README.md', encoding = 'utf-8') as f:
    README = f.read().replace("\r", "")

# =============================================================================> 
# license
print("--------------------")
with open('LICENSE', encoding = 'utf-8') as f:
    LICENSE = " ".join([i.replace("\n", "") for i in f.readlines()][:2])
    print(LICENSE)

# =============================================================================> 
# requires
print("--------------------")
with open('requirements.txt', encoding = 'utf-8') as f:
    REQUIRES = []
    require = f.readline()
    while require:
        print(require)
        REQUIRES.append(require)
        require = f.readline()
print("--------------------")

# =============================================================================> 
# package data
PACKAGE_DATA = {}

# =============================================================================> 
# author
AUTHOR = "nakashimas"
AUTHOR_EMAIL = "nascor.neco@gmail.com"

# =============================================================================> 
# description
DESCRIPTION = "Tracker Network Wrapper In Python."

# =============================================================================> 
# version
VERSION = "0.0.1"

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities'
]

# =============================================================================> 
setup(
    name = 'ggpython',
    keywords = 'game tracker valorant',
    version = VERSION,
    description = DESCRIPTION,
    long_description = README,
    long_description_content_type = "text/markdown",
    license = LICENSE,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = 'https://github.com/nakashimas/ggpython',
    packages = find_packages(exclude = ('tests', 'docs', 'dest', 'dist')),
    package_data = PACKAGE_DATA,
    install_requires = REQUIRES,
    classifiers = CLASSIFIERS,
    include_package_data = True,
    test_suite = 'tests'
)

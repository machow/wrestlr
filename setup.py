#!/usr/bin/env python

import re
import ast
from setuptools import setup, find_namespace_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('wrestlr/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.md') as f:
    README = f.read()

setup(
    name='wrestlr',
    version=version,
    packages=find_namespace_packages(include = "wrestlr.*"),
    install_requires=['hoof', 'siuba', 'pandas'],
    description='Why debate R vs python, when you could convert R to python?',
    author='Michael Chow',
    author_email='mc_al_github@fastmail.com',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/machow/wrestlr'
    )

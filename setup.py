#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'rgf',
    version = '0.0.1',
    description = 'rgf: red/green/refactor, a BDD framework for writing and running specs.',
    author = 'Matt Patterson',
    author_email = 'matt@reprocessed.org',
    url = 'http://github.com/fidothe/rgf',
    license = 'MIT',
    keywords = 'testing bdd tdd',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'rgf = rgf.core.runner:main',
        ],
    }
)


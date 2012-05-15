#!/usr/bin/env python

from setuptools import setup, find_packages
import os

long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r').read() + '\nChangelog\n=========\n' + open('CHANGELOG', 'r').read()

setup(name = 'rgf',
    version = '0.0.2',
    description = 'rgf: red/green/refactor, a BDD framework for writing and running specs.',
    long_description = long_description,
    use_2to3=True,
    author = 'Matt Patterson',
    author_email = 'matt@reprocessed.org',
    url = 'http://github.com/fidothe/rgf',
    license = 'LICENSE',
    keywords = 'testing bdd tdd',
    classifiers = [
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Topic :: Software Development :: Testing',
    ],
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'rgf = rgf.core.runner:main',
        ],
    }
)


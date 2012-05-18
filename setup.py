#!/usr/bin/env python

from setuptools import setup, find_packages
import os, sys

readme_text = open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r').read()
changelog_text = open(os.path.join(os.path.dirname(__file__), 'CHANGELOG'), 'r').read()
long_description = readme_text  + '\nChangelog\n=========\n' + changelog_text

setup(name = 'rgf',
    version = '0.2.0',
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
            'rgf-%s = rgf.core.runner.main' % sys.version[:3],
        ],
    }
)


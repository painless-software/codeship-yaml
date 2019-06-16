#!/usr/bin/env python
"""
Codeship-YAML, YAML configuration file support for Codeship.
Copyright (C) 2016  Painless Software <info@painless.software>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

import codeship_yaml as package

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development :: Build Tools',
]
KEYWORDS = [
    'build server',
    'continuous integration',
    'continuous delivery',
    'devops',
    'infrastructure',
    'tools',
]


def read_file(*pathname):
    """Read a file defined by its path components"""
    with open(join(dirname(abspath(__file__)), *pathname)) as thefile:
        return thefile.read()


setup(
    name='codeship-yaml',
    version=package.__version__,
    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
    url=package.__url__,
    license=package.__license__,
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    install_requires=read_file('requirements.txt'),
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'codeship-yaml = codeship_yaml.main:main',
        ],
    },
)

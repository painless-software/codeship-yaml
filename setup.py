#!/usr/bin/env python
#
# Codeship-YAML, YAML configuration file support for Codeship.
# Copyright (C) 2016  Painless Software <info@painless.software>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from glob import glob
from os import remove
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand  # noqa
from shlex import split
from shutil import rmtree
from sys import exit

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
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
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


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tox import cmdline
        args = self.tox_args
        if args:
            args = split(self.tox_args)
        errno = cmdline(args=args)
        exit(errno)


class Clean(TestCommand):
    def run(self):
        delete_in_root = [
            'build',
            'dist',
            '.eggs',
            '*.egg-info',
            '.tox',
        ]
        delete_everywhere = [
            '__pycache__',
            '*.pyc',
        ]
        for candidate in delete_in_root:
            rmtree_glob(candidate)
        for visible_dir in glob('[A-Za-z0-9]*'):
            for candidate in delete_everywhere:
                rmtree_glob(join(visible_dir, candidate))
                rmtree_glob(join(visible_dir, '*', candidate))
                rmtree_glob(join(visible_dir, '*', '*', candidate))
                rmtree_glob(join(visible_dir, '*', '*', '*', candidate))


def rmtree_glob(file_glob):
    for fobj in glob(file_glob):
        try:
            rmtree(fobj)
            print('%s/ removed ...' % fobj)
        except OSError:
            try:
                remove(fobj)
                print('%s removed ...' % fobj)
            except OSError as err:
                print(err)


def read_file(*pathname):
    with open(join(dirname(abspath(__file__)), *pathname)) as f:
        return f.read()


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
    tests_require=['tox'],
    cmdclass={
        'clean': Clean,
        'test': Tox,
    },
    entry_points={
        'console_scripts': [
            'codeship-yaml = codeship_yaml.main:main',
        ],
    },
)

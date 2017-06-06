==============================
Codeship-YAML |latest-version|
==============================

|codeship| |health| |python-support| |downloads| |license| |gitter|

YAML configuration file support for `Codeship`_.

+------------+-------------+
|   Syntax Compatibility   |
+============+=============+
+ Travis CI  | |travis-ci| |
+------------+-------------+
+ Shippable  | |shippable| |
+------------+-------------+
+ VexorCI    | |vexor-ci|  |
+------------+-------------+

Background
==========

Many continuous integration services support YAML configuration files in order
to support the `infrastructure as code`_ paradigm.  Codeship, though one of the
most appealing platforms, is missing this feature.  You have to add commands
regarding setup, testing and deployment in your Codeship project settings.
This has various disadvantages, but even though `users are complaining`_
Codeship is not planning to address the issue on its traditional build server
infrastructure.  (Only Codeship's new Docker-based infrastructure will finally
make you more happy.)

Usage
=====

Create a ``codeship.yml`` file in your repository at root level.  The syntax
is inspired by `Travis CI`_ and `Shippable`_, though only limited features are
supported.  Example:

.. code-block:: yaml

   install:
     - pip install flake8
   before_script:
     - touch codeship-yaml-was-here
   script:
     - flake8
   after_success:
     - echo "Now we can deploy"

To make Codeship read and interpret your ``codeship.yml`` file, and execute
the commands in it add the following lines in the **Setup Commands** text box
at *Codeship* > *Select Project...* > *(your project)*, *Project Settings* >
*Test Settings*.

.. code-block:: bash

   pip install codeship-yaml
   codeship-yaml

This will make ``codeship-yaml`` execute the commands you specified in the
default sections in the following section order:

#. ``install``
#. ``before_script``
#. ``script``
#. ``after_success``

More Control
------------

If you want more control over which sections are executed you can specify the
requested section as a parameter.  For example, you could add the following
commands into the below-mentioned text boxes of your Codeship project:

*Project Settings* > *Test Settings* > **Setup Commands**

.. code-block:: bash

   pip install codeship-yaml
   codeship-yaml install

*Project Settings* > *Test Settings* > **Test Commands**

.. code-block:: bash

   codeship-yaml before_script script

*Project Settings* > *Deployment* > **(branch name)**

.. code-block:: bash

   codeship-yaml after_success

Adding custom sections, other than the default ones, to your ``codeship.yml``
file is possible but discouraged (to avoid losing similarity with other build
platforms).  If you want an additional section, which is established on other
platforms already, please consider placing a `pull request`_.

Python 3
========

The build image of Codeship's classic infrastructure supports both `Python
2.7 and 3.4`_, but for Python 3 some outdated packages will make you run into
broken builds (e.g. when you install `packages with environment markers`_ in
setup.py).

To have fully working Python 3.4 support use the following setup commands in
*Project Settings* > *Test Settings* > **Setup Commands**:

.. code-block:: bash

   virtualenv -p $(which python3) "${HOME}/cache/python3_env"
   . "${HOME}/cache/python3_env/bin/activate" && python --version
   pip install --upgrade setuptools && pip list | grep setuptools

Update:
   More Python versions are now supported via a ``python.sh`` script
   provided by Codeship. See the `top of the script`_ for usage instructions.

Contribute
==========

For development we use `tox`_, which handles both static code analysis and
tests for all supported Python versions.  ``tox`` is automatically installed
for the test runs and will work out-of-the-box when you run the tests through
``setup.py``.  Unfortunately, you'll have to install ``virtualenv`` though:

.. code-block:: bash

   $ pip install virtualenv

After making your code changes don't forget to add tests, and simply run:

.. code-block:: bash

   $ python setup.py test

When you place a `pull request`_ all tests are run on the build server
infrastructure of `Codeship`_, `Travis CI`_, `Shippable`_ and `Vexor`_ again.
Please check if they all pass to ensure the syntax stays compatible across the
different build infrastructures.

To remove all build files and folders including Python byte code you can run:

.. code-block:: bash

   $ python setup.py clean

Credits
=======

This project is brought to you by `Painless Software`_, a best-practice
consultancy in software development.  Less pain, more fun.

A big, massive **"Thank you!"** to all contributors:

- `Dave Allie <https://github.com/daveallie>`__ (sectioning and coloring of
  command output)


.. |latest-version| image:: https://img.shields.io/pypi/v/codeship-yaml.svg
   :alt: Latest version on PyPI
   :target: https://pypi.python.org/pypi/codeship-yaml
.. |codeship| image:: https://codeship.com/projects/1ff93f70-dc1f-0133-bbf0-32121d68b74a/status?branch=master
   :alt: Build status
   :target: https://codeship.com/projects/144011
.. |travis-ci| image:: https://travis-ci.org/painless-software/codeship-yaml.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/painless-software/codeship-yaml
.. |shippable| image:: https://api.shippable.com/projects/5701ae1233e2f1203f8cab18/badge?branch=master
   :alt: Build status
   :target: https://app.shippable.com/projects/5701ae1233e2f1203f8cab18
.. |vexor-ci| image:: https://ci.vexor.io/projects/15c50c86-b271-462f-876a-6461ff9debaa/status.svg
   :alt: Build status
   :target: https://ci.vexor.io/ui/projects/15c50c86-b271-462f-876a-6461ff9debaa/builds
.. |health| image:: https://landscape.io/github/painless-software/codeship-yaml/master/landscape.svg?style=flat
   :target: https://landscape.io/github/painless-software/codeship-yaml/master
   :alt: Code health
.. |python-support| image:: https://img.shields.io/pypi/pyversions/codeship-yaml.svg
   :target: https://pypi.python.org/pypi/codeship-yaml
   :alt: Python versions
.. |downloads| image:: https://img.shields.io/pypi/dm/codeship-yaml.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypi.python.org/pypi/codeship-yaml
.. |license| image:: https://img.shields.io/pypi/l/codeship-yaml.svg
   :alt: Software license
   :target: https://www.gnu.org/licenses/gpl-3.0.html
.. |gitter| image:: https://badges.gitter.im/painless-software/codeship-yaml.svg
   :alt: Gitter chat room
   :target: https://gitter.im/painless-software/codeship-yaml

.. _Codeship: https://codeship.com/
.. _infrastructure as code: https://en.wikipedia.org/wiki/Infrastructure_as_Code
.. _users are complaining: http://stackoverflow.com/questions/31772306/doesnt-codeship-support-yaml-configure-file
.. _Travis CI: https://travis-ci.org/
.. _Shippable: https://shippable.com/
.. _Vexor: https://vexor.io/
.. _Python 2.7 and 3.4: https://codeship.com/documentation/languages/python/
.. _packages with environment markers: https://github.com/gtimelog/gtimelog/commit/e42cf0e
.. _top of the script: https://github.com/codeship/scripts/blob/master/languages/python.sh#L2-L10
.. _tox: https://tox.readthedocs.io/en/latest/
.. _pull request: https://github.com/painless-software/codeship-yaml/pulls
.. _Painless Software: https://painless.software/

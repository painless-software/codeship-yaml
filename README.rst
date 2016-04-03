==============================
Codeship-YAML |latest-version|
==============================

|build-status| |health| |downloads| |license| |gitter|

YAML configuration file support for `Codeship`_.

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

Create a ``codeship.yml`` file in your respository at root level.  The syntax
is inspired by `Travis-CI`_ and `Shippable`_, though only limited features are
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
platforms).

Credits
=======

This project is brought to you by `Painless Software`_, a best-practice
consultancy for software development.  Less pain, more fun.


.. |latest-version| image:: https://img.shields.io/pypi/v/codeship-yaml.svg
   :alt: Latest version on PyPI
   :target: https://pypi.python.org/pypi/codeship-yaml
.. |build-status| image:: https://codeship.com/projects/12345678-1234-1234-1234-123456789000/status?branch=master
   :alt: Build status
   :target: https://codeship.com/projects/123456
.. |health| image:: https://landscape.io/github/painless-software/codeship-yaml/master/landscape.svg?style=flat
   :target: https://landscape.io/github/painless-software/codeship-yaml/master
   :alt: Code health
.. |downloads| image:: https://img.shields.io/pypi/dm/codeship-yaml.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypi.python.org/pypi/codeship-yaml
.. |license| image:: https://img.shields.io/pypi/l/codeship-yaml.svg
   :alt: Software license
   :target: https://www.gnu.org/licenses/gpl-3.0.html
.. |gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Gitter chat room
   :target: https://gitter.im/painless-software/codeship-yaml

.. _Codeship: https://codeship.com/
.. _infrastructure as code: https://en.wikipedia.org/wiki/Infrastructure_as_Code
.. _users are complaining: http://stackoverflow.com/questions/31772306/doesnt-codeship-support-yaml-configure-file
.. _Travis-CI: https://travis-ci.org/
.. _Shippable: https://shippable.com/
.. _Painless Software: https://painless.software/

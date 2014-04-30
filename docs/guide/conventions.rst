Conventions
===========


Writing Documentation
---------------------

We do not expect contributors to write docs (this guide), but it is great if they do.

However, please try to use doc strings or comments so your code is easy to follow.

This, combined with tests, will help us include your code, and write docs for it.


Working with Git
----------------

Repositories
++++++++++++

Always work off your own fork of the code.

Branching
+++++++++

We follow GitFlow_ for branch management.

.. _GitFlow: http://nvie.com/posts/a-successful-git-branching-model/

What this means:

* Master branch is for production deployment only - you should not ever be working off it
* Develop branch is for work. Either work directly from it, or, preferably, branch off it into a "feature" branch
* A feature branch is named "feature/[YOUR_FEATURE_NAME]". Pull requests on themed branches like this are nice.

Examples:

* I want to work on a ticket to add "bookmarking" features, then I branch off "develop" into "feature/bookmarks", and when I am finished, I submit a pull request for this branch

* I want to work on a ticket to refactor view logic in the "entities" app, then I branch off "develop" into "feature/entities-refactoring", and when I am finished, I submit a pull request for this branch

Again, see the original post about Git Flow for more good practices:

http://nvie.com/posts/a-successful-git-branching-model/

Some GUI version control apps, such as Source Tree for OS X, integrate Git Flow into the app, making it even easier to follow the principles.




Writing tests
-------------

Overview
++++++++

Open Budgets has a suite of tests, with the goal of moving to 100% coverage of project code.

We view tests as an integral part of contributing code to the project: any code contributions must be accompanied by tests.

A great way to get into the codebase is to run the tests, read the tests, and extend them, refactor them, or raise issues on the issue tracker for potential problems.

Configuration
+++++++++++++

There are no specific configurations for testing. Please see Depenedncies below for more information.

Running Tests
+++++++++++++

To run all the tests of the project::

    python manage.py selftest

Also, when you use devstrap to bootstrap a local environment, you can use the -t flag to run tests::

    python manage.py devstrap -m -t

Dependencies
++++++++++++

Open Budgets tests depend on the following 3rd party packages:

* django
* factory boy

Django
~~~~~~

https://github.com/django/django

Django comes with its own test framework. There is extensive documentation for this on the Django site. Please get very familiar with the docs if you will be contributing code to Open Budgets:

https://docs.djangoproject.com/en/1.5/topics/testing/

How to import::

    from django.test import TestCase

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/tests.py

Factory Boy
~~~~~~~~~~~

https://github.com/dnerdy/factory_boy

Factory Boy is a Python package for creating test objects. It has great support for Django, but can be used in any Python codebase.

We use Factory Boy to create mock objects for models. Our tests use these mock objects, and not fixtures.

All definitions for mock objects are found in "factories.py" modules, per app.

Please refer to the Factory Boy documentation if you will be contrinuting code to Open Budgets:

http://factoryboy.readthedocs.org/en/latest/

How to import::

    import factory

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/factories.py

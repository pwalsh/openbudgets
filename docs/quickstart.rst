Requirements
============

Overview
--------

Open Budget is written in Python and JavaScript.

If you develop web apps in these languages, it is likely that your machine is ready to start work.

Check that you meet these requirements on your machine.

System
~~~~~~

* A unix-like OS (We develop on Ubuntu and Mac OS X)
* `Python <http://python.org/>`_ (2.7.x)
* `Node <http://nodejs.org/>`_
* `Git <http://git-scm.com/>`_
* `Mercurial <http://mercurial.selenic.com/>`_

Python
~~~~~~

* The necessary tools to build Python packages (eg: python-dev on Debian systems)
* `virtualenv <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
* `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_

Node
~~~~

* `volojs <http://volojs.org/>`_


**Please make sure you meet these requirements before moving on to installation.**

If you need instructions on setting up these requirements, see the `dependencies page <http://open-budget.readthedocs.org/en/latest/guide/management/dependencies.html>`_.

Additionally, if you are new to web development with Python, we also recommend Kenneth Reitz's excellent best practices guide, which we attempt to follow:

http://docs.python-guide.org/en/latest/


Installation
------------

Configure hosts
~~~~~~~~~~~~~~~

This project makes use of subdomains to target languages, and for API requests. To enable this functionality fully, you'll need to edit your hosts file on your development machine.

**Ubuntu**::

    sudo nano /etc/hosts

**Mac OS X**::

    sudo nano /private/etc/hosts

Add the following domain mappings for localhost::

    127.0.0.1 obudget.dev www.obudget.dev api.obudget.dev en.obudget.dev he.obudget.dev ar.obudget.dev ru.obudget.dev


Make a virtualenv
~~~~~~~~~~~~~~~~~

**Remember:** See the `dependencies page <http://open-budget.readthedocs.org/en/latest/guide/management/dependencies.html>`_ for more information on using virtualenv and virtualenvwrapper.

Issue the following commands to create a new virtualenv for the project, and then clone the git repository into your virtualenv project directory::

    # create the virtual environment
    mkvirtualenv open-budget

    # create a directory for our project code
    mkdir /srv/projects/open-budget

    # link our project code directory to our virtual environment
    setvirtualenvproject /srv/environments/open-budget /srv/projects/open-budget

    # move to the root of our project code directory
    cdproject

Clone the project repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we have an environment setup, and we are at the root of our project directory, we need to clone the project from Github::

    git clone git@github.com:hasadna/omuni-budget.git .

**Important: Note the "." at the end of the git clone command.**

Install project requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And continuing, we'll install all the project requirements, the Python requirements via pip, and the Javascript requirements via volo::

    pip install -r requirements.txt --use-mirrors

    volo add -noprompt

Bootstrap the project
~~~~~~~~~~~~~~~~~~~~~

Now we have almost everything we need. We can populate the database with our initial data, run our tests, and run a development server::

    python manage.py devstrap -m -t

    python manage.py runserver

Right now you can see the app at the following address in your browser::

    http://obudget.dev:8000/


Contributions
-------------

You can contribute to the project with code, content and ideas. If you have any ideas or suggestions for content, please open a ticket on the issue tracker, or post a topic on the developer discussion group (links on home page of the docs).

If you want to contribute code, please keep these points in mind:

* **Style**: We try to follow PEP-8 Please lint your code before submitting a pull request
* **Tests**: If you write a piece of code, write a test before you submit a pull request, and also make sure your code does not break existing tests
* **Docs**: If you write a piece of code, please make sure it has docstrings to explain the functionality
* **Branching**: We follow the Git Flow method for managing branches. and all development work is done off the **develop** branch

More below.

Style
-----

TODO

Tests
-----

We won't accept code that doesn't have tests for it.

Docs
----

We do not expect contributors to write docs (this guide), but it is great if they do.

However, please try to use doc strings or comments so your code is easy to follow. This, combined with tests, will help us include your code, and write docs for it.

Branching
---------

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

Requirements
============

Overview
--------

Open Budget is written in Python and JavaScript.

If you develop web apps in these languages, it is likely that your machine is ready to start work.

Check that you meet these requirements:

* A unix-like OS (We develop on Ubuntu and Mac OS X)
* `Python <http://python.org/>`_ (2.7.x)
* `Node <http://nodejs.org/>`_
* `Git <http://git-scm.com/>`_
* `Mercurial <http://mercurial.selenic.com/>`_
* `virtualenv <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
* `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_

Please make sure you meet these requirements before moving on to installation, and make sure to read the guide/management/dependencies page for more details.

If you want to get more information on current best practices for developing web apps in Python, Kenneth Reitz has an excellent guide right here:

http://docs.python-guide.org/en/latest/

We highly recommend it, and in general, we try to follow the best practices there.

*Note*: Node.js on Ubuntu 12.10 or greater: the node executable was renamed to nodejs, so add this symbolic link which will help with some of our dependencies::

    ln -s /usr/bin/nodejs /usr/bin/node

Installation
------------

Install required packages
~~~~~~~~~~~~~~~~~~~~~~~~~

**Ubuntu**::

    sudo apt-get install python-dev mercurial

**Fedora**::

    sudo yum install python-devel mercurial

**Mac OS X**

Download from http://mercurial.selenic.com/mac/

Configure hosts
~~~~~~~~~~~~~~~

This project makes use of subdomains to target languages, and for the API. To enable this functionality fully, you'll need to edit your hosts file on your development machine.

**Ubuntu**::

    sudo nano /etc/hosts

**Mac OS X**::

    sudo nano /private/etc/hosts

Add the following domain mappings for localhost::

    127.0.0.1 [whatever else you have]  obudget.dev www.obudget.dev api.obudget.dev en.obudget.dev he.obudget.dev ar.obudget.dev ru.obudget.dev


Make a virtualenv
-----------------

Issue the following commands to create a new virtualenv for the project, and then clone the git repository into your virtualenv project directory::

    mkvirtualenv open-budget

    mkdir /srv/projects/open-budget

    setvirtualenvproject /srv/environments/open-budget /srv/projects/open-budget

    cdproject

    git clone git@github.com:hasadna/omuni-budget.git .

**Important: Note the "." at the end of the git clone command.**

Install volo
------------

`volo <http://volojs.org/>`_ is a tool that automates a lot build and project creation related tasks,
and package management among those. Volo runs on Node.js

To install volo Issue the following command::

    npm install -g volo

For more details see `<https://github.com/volojs/volo#volo>`_

And continuing, we'll install all the project requirements into our virtualenv, populate our initial database, load some development data, run some tests, and run a server for the project::

    pip install -r requirements.txt --use-mirrors

    volo add -noprompt

    python manage.py devstrap -m -t

    python manage.py runserver

Right now you can see the app at the following address in your browser::

    http://obudget.dev:8000/


Contributions
=============

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

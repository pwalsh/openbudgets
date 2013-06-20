Requirements
============

Overview
--------

Open Budget is written in Python and JavaScript.

If you develop web apps in these languages, it is likely that your machine is ready to start work.

Below we walk you through setting up an environment. First, the system requirements to work on the project, and second, the setup of the project itself.

System requirements
-------------------

You system will need to have **Python** (and some system-wide Python packages), **Node.js** (and some system-wide Node.js modules), **Git**, and **Mercurial** (for working with code repositories).

* A unix-like OS
* `Python <http://python.org/>`_ (2.7.x)
* `Node <http://nodejs.org/>`_ (0.8.x)
* `Git <http://git-scm.com/>`_
* `Mercurial <http://mercurial.selenic.com/>`_
* `virtualenv <http://virtualenvwrapper.readthedocs.org/en/latest/>`_ (a Python package for working with multiple dev. environments)
* `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_ (some sugar for virtualenv)
* The necessary tools to build Python packages (eg: python-dev on Debian systems)
* `volojs <http://volojs.org/>`_ (a package manager for client-side resources)

We develop on Ubuntu and Mac OS X. If you use other operating systems with any success, please make a pull request on this file, with any required additions, to support those operating systems.

All setup instructions are tested on Ubuntu and Mac OS X only.

**IMPORTANT: Please make sure you meet these requirements before moving on to the installation of the project.**

Additionally, if you are new to web development with Python, we also recommend Kenneth Reitz's excellent best practices guide, which we attempt to follow:

http://docs.python-guide.org/en/latest/

Installing system requirements
------------------------------

Ubuntu
~~~~~~

Here we go::

    sudo apt-get install python-dev mercurial git-core nodejs python-pip
    sudo pip install virtualenv virtualenvwrapper
    npm install volo -g

Now we'll setup virutalenvwrapper, in our user's .profile file::

    # this goes in ~/.profile
    export WORKON_HOME="/srv/environments"
    export PROJECT_HOME="/srv/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME

Fedora
~~~~~~

Here we go::

    sudo yum install python-devel mercurial

Mac OS X
~~~~~~~~

First, make sure you have XCode installed, **and** Command Line Tools. See here for more info about this:

https://python-guide.readthedocs.org/en/latest/starting/install/osx.html

Secondly, install Homebrew, which is a great package manager for all the *nix goodies you need to develop:

http://mxcl.github.io/homebrew/

To ensure you are ready, try::

    brew

You should see a list of arguments the brew command accepts.

Next, you can choose to use the version of Python that comes with OS X, or you can use a Homebrew managed Python. If you are not sure, just stick with system Python for now::

    # using system Python
    brew install mercurial git node
    sudo easy_install virtualenv
    sudo pip install virtualenvwrapper
    npm install volo -g

    # alternatively, using homebrew Python
    brew install mercurial git node python
    pip install virtualenv virtualenvwrapper
    npm install volo -g

Now we'll setup virutalenvwrapper, in our user's .bash_profile file::

    # this goes in ~/.bash_profile
    export WORKON_HOME="/Users/[YOUR_USER]/Sites/environments"
    export PROJECT_HOME="/Users/[YOUR_USER]/Sites/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME


Installing the project
----------------------

As long as you have met the system requirements above, we're ready to install the project.

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

    pip install -r requirements/base.txt --use-mirrors

    volo add -noprompt

Bootstrap the project
~~~~~~~~~~~~~~~~~~~~~

Now we have almost everything we need. We can populate the database with our initial data, run our tests, and run a development server::

    python manage.py devstrap -m -t

    python manage.py runserver

Right now you can see the app at the following address in your browser::

    http://obudget.dev:8000/


The easy way to working data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project bootstrap loads quite a chunk of the data the app requires - but not everything. Notably, it does not load budget data at this point. The easiest way to add the latest budget data we have is to now, replace your development database with one that is completely populated. We have a set of populated databases here:

https://drive.google.com/#folders/0B4JzAmQXH28mdUpST3lkSzluWnc

Simply grab the latest one by date, download it, rename it local.db and replace the existing local.db in your repo root.

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

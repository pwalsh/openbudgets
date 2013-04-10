Requirements
============

Open Budget is written in Python and JavaScript. If you develop web apps in these languages, it is likely that your machine is ready to start work. Check that you meet these requirements:

* A unix-like OS (We develop on Ubuntu and Mac OS X)
* Python 2.7
* Node.js
* Git
* virtualenv
* virtualenvwrapper

Please make sure you meet these requirements before moving on to installation.

About virtualenv
----------------

Virtual environments are an important tool for Python web development.

We have noticed that even Python developers who have not done web app development before are not familiar with virutalenv. The concept behind virtualenv may also seem unfamiliar to developers coming from other languages.

So, if you haven't used virtualenv before, follow these install instructions, and read more about virtualenv via the links below.

**Ubuntu**::

    sudo apt-get install python-pip

    sudo pip install virtualenv

    sudo pip install virtualenvwrapper


**Mac OS X (you must have a recent XCode install)**::

    sudo easy_install virtualenv

    sudo pip install virtualenvwrapper

Once virtualenv and virtualenvwrapper are installed, you need to configure your shell.

**Ubuntu ~/.profile**::

    export EDITOR=nano
    export WORKON_HOME="/srv/environments"
    export PROJECT_HOME="/srv/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME

**Mac OS X ~/.bash_profile**::

    export EDITOR=nano
    export WORKON_HOME="/Users/[YOUR_USER]/Sites/environments"
    export PROJECT_HOME="/Users/[YOUR_USER]/Sites/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME



Read more about virtualenv_ and virtualenvwrapper_.

.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/

About Node.js
-------------

Open Budget is not a Node.js app, but we do make use of node.js tools in our development environments.

Now we can move on to the project installation.

Installation
============

Configure hosts
---------------

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

And continuing, we'll install all the project requirements into our virtualenv, populate our initial database, load some development data, run some tests, and run a server for the project::

    pip install -r requirements.txt

    volo add

    python manage.py devstrap -t

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

TODO

Docs
----

TODO

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

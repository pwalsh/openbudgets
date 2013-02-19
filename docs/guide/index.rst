Open Budget
===========

A platform for accessible government budget data
------------------------------------------------

This guide is for developers using Open Budget in their own projects, or contributing code to the main repository. It provides instructions for installation, an overview of the code base, some context on factors that influenced the design.

Get involved
------------

**Code**: https://github.com/hasadna/open-muni

**Issues**: https://github.com/hasadna/open-muni/issues

**Docs**: http://open-budget.readthedocs.org/

**Discussion**: https://groups.google.com/forum/?fromgroups=#!forum/open-muni-dev

**HaSadna (Public Knowledge Workshop)**: http://hasadna.org.il/

Global requirements
-------------------

* A unix-like OS (We develop on Ubuntu and Mac OS X)
* Python 2.7
* Git
* virtualenv
* virtualenvwrapper

Please make sure you meet these requirements before moving on to installation.

virtualenv
~~~~~~~~~~

Virtual environments are an important tool for Python web development. If you haven't used them before, follow these install instructions.

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

Now we can move on to the project installation.

Installation
------------

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
~~~~~~~~~~~~~~~~~

Issue the following commands to create a new virtualenv for the project, and then clone the git repository into your virtualenv project directory::

    mkvirtualenv open-muni

    mkdir /srv/projects/open-muni

    setvirtualenvproject /srv/environments/open-muni /srv/projects/open-muni

    cdproject

    git clone git@github.com:hasadna/open-muni.git .

**Important: Note the "." at the end of the git clone command.**

And continuing, we'll install all the project requirements into our virtualenv, populate our initial database, load some development data, run some tests, and run a server for the project::

    pip install -r requirements.txt

    python manage.py syncdb --migrate

    python manage.py test accounts api budgets commons govts interactions pages

    python manage.py loaddata dev/sites.json

    python manage.py loaddata dev/objects.json

    python manage.py runserver

Right now you can see the app at the following address in your browser::

    http://obudget.dev:8000/


Contributions
-------------

You can contribute to the project with code, content and ideas. If you have any ideas or suggestions for content, please open a ticket on the issue tracker, or post a topic on the developer discussion group (links on home page of the docs).

If you want to contribute code, please keep these points in mind:

* **Style**: We try to follow PEP-8 Please lint your code before submitting a pull request
* **Tests**: If you write a piece of code, write a test before you submit a pull request, and also make sure your code does not break existing tests
* **Branching**: We follow the Git Flow method for managing branches. and all development work is done off the **develop** branch

More below.

Style
+++++

TODO

Tests
+++++

TODO

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

* I want to work on a ticket to refactor view logic in the "govts" app, then I branch off "develop" into "feature/govts-refactoring", and when I am finished, I submit a pull request for this branch

Again, see the original post about Git Flow for more good practices:

http://nvie.com/posts/a-successful-git-branching-model/

Some GUI version control apps, such as Source Tree for OS X, integrate Git Flow into the app, making it even easier to follow the principles.


The Code
--------

Introduction
~~~~~~~~~~~~

For the most part, Open Budget is a fairly standard Django project, using Grappelli for a nicer Admin UI/API, and Django REST Framework for the Open Budget Web API.

You can see all the other dependencies in the requirements.txt file, but Django, Grappelli and Django REST are the main frameworks you'll be interacting with when writing code for users of the web app, users of the admin, and users of the web API.

The layout of the project is quite close to the standard Django idiom of an "app" for each distinct area of functionality.

There is a "special" app called "commons" which has code that is used throughout the project as a whole. Here you will find things like general utility functions, mixin classes, and common data models.

Let's get into the details...

Admin
~~~~~

The Admin is highly customized from the default Django CRUD mappings.

**Interface**

We are using Grappelli_ as our admin framework, giving us a more user-friendly UI "out of the box", and a nicer API for customizing Django Admin behaviour.

.. _Grappelli: https://django-grappelli.readthedocs.org/en/latest/

**Data entry**

Data entry should be easy for content editors. That means developers need to do a bit more work so that performing content tasks in the admin is intuitive for these users.

Django's default admin mappings are not enough - your content editor users don't need to know about the relational data structure underneath. In many cases, the answer is to employ ProxyModels_.

.. _ProxyModels: https://docs.djangoproject.com/en/dev/topics/db/models/#proxy-models

A great example of this is the standard User/UserProfile dance in Django. It is far from intuitive for a content editor to have two objects in the admin for what should be "one thing" - the User Profile. Use Proxy Models and win.

See our examples in account.models and account.admin.

Follow this pattern whenever it is required for reasonable data entry by non-technical staff.


Accounts
~~~~~~~~
Everything to do with User Accounts.


Budgets
~~~~~~~


Government entities
~~~~~~~~~~~~~~~~~~~

Localization
~~~~~~~~~~~~

model trans

Schema migration
~~~~~~~~~~~~~~~~

REST API
~~~~~~~~

Commons
~~~~~~~


API docs
--------

Should be autogenerated from docstrings

License
-------

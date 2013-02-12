Open Budget
===========

A platform for transparent budgets at all levels of government.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This guide is for developers using Open Budget in their own projects, or contributing code to the main repository. It provides instrcutions for installation, an overview of the code base, some context on factors that influenced the design.

Get involved
------------

Code: https://github.com/hasadna/open-muni

Issues: https://github.com/hasadna/open-muni/issues

Docs: http://open-budget.readthedocs.org/

Discussion: https://groups.google.com/forum/?fromgroups=#!forum/open-muni-dev

PRD: https://docs.google.com/document/d/1cDOELgc4VQ8iPSr6795g0iMMz_klE5dM_s-y2GXbH7o/

More about HaSadna (Public Knowledge Workshop): http://hasadna.org.il/

Requirements
------------

* A unix-based OS
* Python 2.7
* Git
* virtualenv
* virtualenvwrapper

Please make sure you meet these requirements before moving on to installation. If you have a linux distro or Mac OS X, you likely already have Python 2.7.

Install virtualenv/virtualenvwrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ubuntu**::

    sudo apt-get install python-pip

    sudo pip install virtualenv

    sudo pip install virtualenvwrapper


**Mac OS X (you must have a recent XCode install)**::

    sudo easy_install virtualenv

    sudo pip install virtualenvwrapper


Configure your shell
~~~~~~~~~~~~~~~~~~~~

**~/.bash_profile on Mac OS X, ~/.profile on Ubuntu**::

    export EDITOR=nano

    export WORKON_HOME="/srv/environments"

    export PROJECT_HOME="/srv/projects"

    source /usr/local/bin/virtualenvwrapper.sh

    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME

With these settings, your virtualenvs live at /srv/environments/, and your project code lives at /srv/projects/. Adjust according to your tastes. On Mac OS X, for example, I do /Users/me/Sites/environments/ and /Users/me/Sites/projects/.

Now we can move on and install the project.

Installation
------------

Issue the following commands to create a new virtualenv for the project, and clone the git repository into your project directory::

    mkvirtualenv open-muni

    mkdir /srv/projects/open-muni

    setvirtualenvproject /srv/environments/open-muni /srv/projects/open-muni

    cdproject

    git clone git@github.com:hasadna/open-muni.git .

**Important: Note the "." at the end of the git clone directive.**

And continuing, we'll install all the project requirements into our virtualenv, populate our intial database, and run a server for the project::

    pip install -r requirements.txt

    python manage.py syncdb --migrate

    python manage.py runserver

Right now you can see the app at the following address in your browser::

    http://127.0.0.1:8000/


Contributing code
-----------------

We are following the Git Flow paradigm for managing branches, deployment code, etc. This keeps things ordered and logical and makes it easy to see at a glance what is being worked on, what a pull request is addressing, and so on.

Read more about Git Flow: 

http://nvie.com/posts/a-successful-git-branching-model/

Git Flow (and Open Muni) essentials:

Open Muni always have at least two branches available in the public repo: "master" and "development".

Master is for *production* - you should not ever be working off master. Master is the domain of the repository maintainers only.

Work off development
~~~~~~~~~~~~~~~~~~~~

If you read the post on Git Flow above, you can see the reasoning in the approach. If you want to make small bug fixes, enhancements, do them on your "develop" branch, and then submit a pull request when your code is finished.

Or, create a feature/ branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you are tackling a specific feature, or a larger issue, it is good practice to branch off "develop" into your own dedicated "feature/" branch. Then, when you code is ready, submit a pull request for this branch.

For example, if you want to add a new feature to allow bookmarking of any page. First, make sure you are on the "develop" branch. Then, create a feature branch like so:

git checkout -b feature/bookmarks

Now, write all your code for bookmarks, and when ready, you can submit a pull request for "feature/bookmarks".

Again, see the original post about Git Flow for more:

http://nvie.com/posts/a-successful-git-branching-model/

Some GUI version control apps, such as Source Tree for OS X, integrate Git Flow into the app, making it even easier to follow the principles.


Know the codebase
-----------------

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

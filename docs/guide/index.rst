Open Budget
===========

A platform for accessible government budget data
------------------------------------------------

This guide is for developers using Open Budget in their own projects, or contributing code to the main repository. It provides instructions for installation, an overview of the code base, some context on factors that influenced the design.

Get involved
------------

**Code**: https://github.com/hasadna/omuni-budget

**Issues**: https://github.com/hasadna/omuni-budget/issues

**Docs**: http://open-budget.readthedocs.org/

**Demo**: http://open-budget.prjts.com/

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

    mkvirtualenv open-budget

    mkdir /srv/projects/open-budget

    setvirtualenvproject /srv/environments/open-budget /srv/projects/open-budget

    cdproject

    git clone git@github.com:hasadna/omuni-budget.git .

**Important: Note the "." at the end of the git clone command.**

And continuing, we'll install all the project requirements into our virtualenv, populate our initial database, load some development data, run some tests, and run a server for the project::

    pip install -r requirements.txt

    python manage.py devstrap -t

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
~~~~~

TODO

Tests
~~~~~

TODO

Docs
~~~~~

TODO

Branching
~~~~~~~~~

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

Open Budget is written in Python and JavaScript.

Server side, Django provides the application framework. On top of Django, we've built the Web API using Django REST Framework, and we've heavily customized the Admin interface using Grappelli.

You can see additional server side dependencies in the requirements.txt file at the repository root.

Schema migrations
~~~~~~~~~~~~~~~~~

South, and if/how modeltranslations effects this.


Localization
~~~~~~~~~~~~

A key feature of Open Budget is that everything can be localized and internationalized - including model data.

Our custom code for localization and internationalization is located in the "international" app - this app may evolve into a pluggable app in the future.

For localization of files in the project, we of course use Django's built in localization features.

For localization of model data, we use modeltranslation_, a pluggbale app for Django.

For displaying localized data, we use subdomains_ in combination with a custom InterfaceLanguage_ middleware class, that sets a language key based on either (a) user preference, or (b) the request host.

The major reason we decided to expose localized content via subdomains is that it is still the prefered method for indexing via google (here_).

We want Open Budget content to be highly discoverable, and thus we want Google and other search engines to crawl and rank each language as a distinct entity. We have also added language annotations as per those same guidelines to the same end.

.. _modeltranslation: https://django-modeltranslation.readthedocs.org/en/latest/
.. _InterfaceLanguage: https://github.com/hasadna/open-muni/blob/develop/openbudget/commons/middleware.py#L7
.. _subdomains: http://django-subdomains.readthedocs.org/en/latest/
.. _here: http://googlewebmastercentral.blogspot.co.il/2011/12/new-markup-for-multilingual-content.html


Commons
~~~~~~~

There is an app called commons - it has all sorts of project-wide code.

Budgets and Actuals
~~~~~~~~~~~~~~~~~~~

Budget and Actuals data is always mapped to a BudgetTemplate. Depending on the relations of BudgetTemplateNodes, a template maybe flat or a tree.

Any level of government can have a BudgetTemplate, but all members of the same level must share the same template. It is still unclear if/how to deal with change of template overtime. The Israel Muni use case is quite structured, but we probably want to created something more generic.

Governments
~~~~~~~~~~~

Govts are represented by the GeoPoliticalEntity model, which has realtions with self to build a gvernment structure.

Accounts
~~~~~~~~

Django's user model is extended with a UserProfile.

Interactions
~~~~~~~~~~~~

The Interactions app deals with all functionality related to the way a user can interact with objects in the web app. For example, Star an object, follow and object, contribute to discussion on an object, and so on.

Pages
~~~~~

Pages is a simple app to add generic web pages to the system: think about, privacy, and so on.


Admin
~~~~~

The goal of any admin is to make it easy for content editors, not developers, to add content to a system. By default, the Django admin does not deliver on this promise, but it provides a foundation to build on.

First, we are using the excellent Grappelli_ app as our admin framework, overriding the default Django Admin. Grappelli gives us a more user-friendly UI "out of the box", and a nicer API for customizing Django Admin behaviour. 

In addition, we have added some tweaks to make Grappelli play nicer with RTL language display, and with the modeltranslations app, and some of our own custom views. We also make extensive use of ProxyModels_ to simplify the admin interface for content editors.

If you contribute code that should be exposed in some way to the admin, please consider the end user - the content editor, and use Proxy Models or whatever else is required to make their lives easier.

**An example of using a Proxy Model**

A great example when to use a Proxy Model is the standard User/UserProfile dance in Django.

It is far from intuitive for a content editor to have two objects in the admin for what should be "one thing" - the User. Use Proxy Models and win. See our examples in account.models and account.admin.

.. _Grappelli: https://django-grappelli.readthedocs.org/en/latest/
.. _ProxyModels: https://docs.djangoproject.com/en/dev/topics/db/models/#proxy-models

REST API
~~~~~~~~

We have a REST API based on Django REST Framework.

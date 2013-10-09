Start
==========

Overview
--------

Open Budgets is a web app and web API for storing, accessing, visualizing and comparing budgetary data.

Open Budgets is coded in Python and Javascript. Django is used for the server, and libraries such as Backbone, D3, uijet and JQuery for the client.

The 1.0 release of Open Budgets was developed as a platform for budgetary data of municipalities in Israel. The primary goals being a standardized way to store such data for all municipalities, and for users to be able to make comparative analysis of such data.

The code is not tied to anything in particular with the Israeli municipality use case - Open Budgets is ready for use with any "entity structure" that declares budgets, and potential value can be gained from comparative analysis. Examples could be other governmental systems, large organizations in the non-profit sector, corporations, state university systems, and so on.

Open Budgets is open source software and licensed under a BSD license.

Open Budgets is a project of HaSadna (the Public Knowledge Workshop), a non-profit organization in Israel dedicated to data transparency in government.

Find out more here:

http://hasadna.org.il/en/




Open Budgets is written in Python and JavaScript. If you already develop web apps in these languages, it is likely that your machine is ready to start work. Please check the system requirements below to confirm.

This Quickstart will walk you through setting up the project. We provide basic instructions for setting up system requirements, but this does assume some knowledge of the relevant package managers, use of sudo, etc.

If you find any problems with this Quickstart in configuring your system, please raise a ticket in the projects issue tracker here: https://github.com/hasadna/omuni-budget/issues


System requirements
-------------------

In order to work on the project, your system will need Python, Node.js, Git and Mercurial. You'll also need a handful of Python packages and Node.js modules installed globally.

Our Quickstart only supports Ubuntu and Fedora flavors of Linux, and Mac OS X. If you can test the installation on other systems, please make a pull request updating this Quickstart with the required changes.


**IMPORTANT: Please make sure you meet the system requirements before moving on to the installation of the project.**


Installing system requirements
------------------------------

Use of sudo for any commands is also dependent on how your machine is set up.

Ubuntu
~~~~~~

Here we go::

    # Our core system dependencies
    sudo apt-get install python-dev mercurial git-core nodejs redis-server python-pip

    # Python packages we want installed globally
    sudo pip install virtualenv virtualenvwrapper

    # Node.js modules we want installed globally
    sudo npm install volo -g

Now, make some changes to your user's .profile file for the Python environment::

    # this goes in ~/.profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/[YOUR_USER]/environments"
    export PROJECT_HOME="/home/[YOUR_USER]/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/

Fedora
~~~~~~

Here we go::

    # Our core system dependencies
    sudo yum install nodejs npm python-devel python-virtualenv python-virtualenvwrapper python-pip git mercurial redis

    # Node.js modules we want installed globally
    sudo npm install volo -g

Changes for virtualwrapper in your user's .bashrc (assuming you use bash, please adjust for other shells)::

    # this goes in ~/.bashrc
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/[YOUR_USER]/environments"
    export PROJECT_HOME="/home/[YOUR_USER]/projects"
    source /usr/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/

Mac OS X
~~~~~~~~

First, make sure you have XCode installed, **and** Command Line Tools.

See here for more info about this:

https://python-guide.readthedocs.org/en/latest/starting/install/osx.html

Secondly, install Homebrew, which is a great package manager for all the \*nix goodies you need to develop with:

http://mxcl.github.io/homebrew/

To ensure you are ready, try::

    brew

You should see a list of arguments the brew command accepts.

Next, you can choose to use the version of Python that comes with OS X, or you can use a Homebrew managed Python.

If you are not sure, just stick with system Python for now::

    # using system Python
    brew install mercurial git node redis
    sudo easy_install virtualenv
    sudo pip install virtualenvwrapper
    npm install -g volo


    # alternatively, using homebrew Python
    brew install mercurial git node redis python
    pip install virtualenv virtualenvwrapper
    npm install volo -g

Now, make some changes to your user's .bash_profile file for the Python environment::

    # this goes in ~/.bash_profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/Users/[YOUR_USER]/Sites/environments"
    export PROJECT_HOME="/Users/[YOUR_USER]/Sites/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/

Installing the project
----------------------

As long as you have met the system requirements above, we're ready to install the project.

Configure hosts
~~~~~~~~~~~~~~~

This project makes use of subdomains to target languages, and for API requests.

To enable this functionality fully, you'll need to edit your hosts file on your development machine.

**Ubuntu & Fedora**::

    sudo nano /etc/hosts

**Mac OS X**::

    sudo nano /private/etc/hosts

Add the following domain mappings for localhost::

    127.0.0.1 open-budgets.dev www.open-budgets.dev api.open-budgets.dev en.open-budgets.dev he.open-budgets.dev ar.open-budgets.dev ru.open-budgets.dev

Make a virtualenv
~~~~~~~~~~~~~~~~~

We are going to setup the project in a new Python virtual environment. If you are not familiar wth virtualenv, or the accompanying tool, virtualenvwrapper, see the following for more information:

http://docs.python-guide.org/en/latest/dev/virtualenvs/

We are going to create a new virtual environment, create another directory for our project code, make a connection between the two, and then, clone the project code into its directory.

Ubuntu & Fedora
+++++++++++++++

Here we go::

    # create the virtual environment
    mkvirtualenv [PROJECT_NAME]

    # create a directory for our project code
    mkdir /home/[YOUR_USER]/Sites/projects/[PROJECT_NAME]

    # link our project code directory to our virtual environment
    setvirtualenvproject /home/[YOUR_USER]/environments/[PROJECT_NAME] /home/[YOUR_USER]/Sites/projects/[PROJECT_NAME]

    # move to the root of our project code directory
    cdproject

OS X
++++

Here we go::

    # create the virtual environment
    mkvirtualenv [PROJECT_NAME]

    # create a directory for our project code
    mkdir /Users/[YOUR_USER]/Sites/projects/[PROJECT_NAME]

    # link our project code directory to our virtual environment
    setvirtualenvproject /Users/[YOUR_USER]/Sites/environments/[PROJECT_NAME] /Users/[YOUR_USER]/Sites/projects/[PROJECT_NAME]

    # move to the root of our project code directory
    cdproject

Note
++++

Later when you want to work on the project use::
    workon [PROJECT_NAME]

For more information on virtualenvwrapper:

    http://www.doughellmann.com/projects/virtualenvwrapper/



Clone the project repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we have an environment setup, and we are at the root of our project directory, we need to clone the project from Github::

    git clone https://github.com/hasadna/omuni-budget.git .

**Important: Note the "." at the end of the git clone command.**

Install project requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And continuing, we'll install all the project requirements, the Python requirements via pip, and the Javascript requirements via volo::

    pip install -r requirements/base.txt --use-mirrors

    # If you see ParseError when invoking volo, keep trying, it eventually works. We are going to replace it.
    volo add -noprompt

Bootstrap the project
~~~~~~~~~~~~~~~~~~~~~

Now we have almost everything we need.

We can populate the database with our initial data, run our tests, and run a development server::

    # syncdb, migrate and run tests
    python manage.py devstrap -m -t

    # start the server
    python manage.py runserver

Right now you can see the app at the following address in your browser::

    http://obudget.dev:8000/

Lastly, For some functionality, you'll need to adjust settings.local with some settings for your environment. For example, email username and password. **Never commit your changes to settings.local**.

The easy way to working data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project bootstrap loads some initial data the app requires.

To get entity and sheet data (the Israel government structure, and the muni budgets, in the current case), grab our latest local.db file and replace your current development database with it.

You can always get the latest file here:

https://drive.google.com/#folders/0B4JzAmQXH28mNXBxdjdzeEJXb2s

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

best practices
--------------

Additionally, if you are new to web development with Python, we also recommend Kenneth Reitz's excellent best practices guide, which we attempt to follow:

http://docs.python-guide.org/en/latest/

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

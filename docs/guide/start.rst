Start
=====

.. image:: https://travis-ci.org/prjts/openbudgets.png
   :alt: Build Status
   :target: https://travis-ci.org/prjts/openbudgets


.. image:: https://coveralls.io/repos/prjts/openbudgets/badge.png?branch=develop
   :alt: Coverage Status
   :target: https://coveralls.io/r/prjts/openbudgets?branch=develop


Open Budgets is a web app and web API for storing, accessing, visualizing and comparing budgetary data.

Open Budgets is written in Python and Javascript, and is open source software released under a BSD license.

Open Budgets is a project of the **Public Knowledge Workshop**, a non-profit organization in Israel dedicated to data transparency in government.

Stack
=====

Server
------

The server is written in Python using Django and Django REST Framework.


Client
------

The client makes use of D3, jQuery, Uijet, and Backbone.


System requirements
===================

Open Budgets has been developed on Mac OS X and Ubuntu, and should be trivial to deploy to any *nix environment.

We also provide basic instructions for Windows installations, but we do not recommend this approach.

Essentially, the project requires an OS equipped with **Python**, **Postgresql**, **Git** and **Mercurial**.

**Node.js** is an optional dependency if you'll like to use Javascript build tools.

**Redis** is an optional dependency for development environments, but is required for production deployments.

Below we give a basic, opinionated system setup for a number of OSes.

Experienced users may choose to vary from the following instructions.

**IMPORTANT: Ensure you have the minimal system requirements before moving on to install of the project.**


Ubuntu
------

**NOTE:** Use of `sudo` for any command is very dependent on your setup.

Execute the commands without it if you know you don't need it.

Install::

    # required dependencies
    sudo apt-get install python-dev python-pip postgresql postgresql-contrib postgresql-server-dev-all mercurial git-core
    sudo pip install virtualenv virtualenvwrapper

    # optional dependencies in development, required in production
    sudo apt-get install redis-server

    # optional dependencies
    sudo apt-get install nodejs
    sudo npm install -g volo bower less


That's all the packages we need for the system, now we need to configure the user's .profile.

Configure::

    # this goes in ~/.profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/{YOUR_USER}/environments"
    export PROJECT_HOME="/home/{YOUR_USER}/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/


Fedora
------

**NOTE:** Use of `sudo` for any command is very dependent on your setup.

Execute the commands without it if you know you don't need it.

Here we go::

    # required dependencies
    sudo yum install python-devel python-pip python-virtualenv python-virtualenvwrapper python-pip postgresql postgresql-contrib postgresql-server-dev-all git mercurial

    # optional dependencies in development, required in production
    sudo yum install redis

    # optional dependencies
    sudo yum install nodejs npm
    sudo npm install -g volo bower less


That's all the packages we need for the system, now we need to configure the user's .bashrc (assuming you use bash, please adjust for other shells).

Configure::

    # this goes in ~/.bashrc
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/{YOUR_USER}/environments"
    export PROJECT_HOME="/home/{YOUR_USER}/projects"
    source /usr/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/


Mac OS X
--------

First, make sure you have XCode installed with Command Line Tools.

Secondly, install Homebrew, which is a great package manager for all the \*nix goodies you need to develop with:

http://mxcl.github.io/homebrew/

To ensure you are ready, try::

    brew

You should see a list of arguments the brew command accepts.

Next, you can choose to use the version of Python that comes with OS X, or you can use a Homebrew managed Python.

If you are not sure, just stick with system Python setup for now.

Install::

    # using system Python
    brew install mercurial git node redis
    sudo easy_install virtualenv
    sudo pip install virtualenvwrapper
    npm install -g volo bower less


    # alternatively, using homebrew Python
    brew install mercurial git node redis python
    pip install virtualenv virtualenvwrapper
    npm install -g volo bower less


That's all the packages we need for the system, now we need to configure the user's .bash_profile.

Configure::

    # this goes in ~/.bash_profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/Users/{YOUR_USER}/Sites/environments"
    export PROJECT_HOME="/Users/{YOUR_USER}/Sites/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/


Windows
-------

**Note:** We have assisted some users to configure Windows for Python web development, but we don't consider this to be a complete set of instructions, or even the best way to proceed. If you can provide a foolproof Windows setup, please make a pull request on this file.

Follow this guide to install Python:

http://docs.python-guide.org/en/latest/starting/install/win/

Install Postgresql:

http://www.enterprisedb.com/products-services-training/pgdownload#windows

Install Git (version control and dependency management):

http://git-scm.com/download/win

Install Mercurial (version control and dependency management):

http://mercurial.selenic.com/wiki/Download

Install Pillow
https://pypi.python.org/pypi/Pillow/2.1.0#downloads

Optional, install Node.js:

http://nodejs.org/download/


You'll probably have to check this out too:

http://adambard.com/blog/installing-fabric-under-windows-7-64-bit-with/


Installing the project
======================

As long as you have met the system requirements above on your chosen OS, we're ready to install the project.


Configure hosts
---------------

This project makes use of subdomains to target languages, and for API requests.

To enable this functionality fully, you'll need to edit your hosts file on your development machine.

**Ubuntu & Fedora**::

    sudo nano /etc/hosts

**Mac OS X**::

    sudo nano /private/etc/hosts

Add the following domain mappings for localhost::

    127.0.0.1 openbudgets.dev www.openbudgets.dev en.openbudgets.dev he.openbudgets.dev ar.openbudgets.dev ru.openbudgets.dev

Make a virtualenv
-----------------

We are going to setup the project in a new Python virtual environment.

If you are not familiar wth virtualenv or virtualenvwrapper, see the following article:

http://docs.python-guide.org/en/latest/dev/virtualenvs/

We are going to:

* Create a new virtual environment
* Create another directory for our project code
* Make a connection between the two
* Clone the project code into its directory

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
----------------------------

Now we have an environment setup, and we are at the root of our project directory, we need to clone the project from Github::

    git clone https://github.com/hasadna/omuni-budget.git .

**Important: Note the "." at the end of the git clone command.**

Install project requirements
----------------------------

And continuing, we'll install all the project requirements, the Python requirements via pip, and the Javascript requirements via volo::

    pip install -r requirements/base.txt --use-mirrors

    # If you see ParseError when invoking volo, keep trying, it eventually works. We are going to replace it.
    volo add -noprompt

Bootstrap the project
---------------------

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
----------------------------

The project bootstrap loads some initial data the app requires.

To get entity and sheet data (the Israel government structure, and the muni budgets, in the current case), grab our latest local.db file and replace your current development database with it.

You can always get the latest file here:

https://drive.google.com/#folders/0B4JzAmQXH28mNXBxdjdzeEJXb2s

Simply grab the latest one by date, download it, rename it local.db and replace the existing local.db in your repo root.

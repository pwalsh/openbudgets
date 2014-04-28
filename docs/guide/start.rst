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

The client is written in Javascript makes use of Uijet, Backbone, JQuery, and D3.

System requirements
===================

Open Budgets has been developed on Mac OS X, Ubuntu and Debian. It should be trivial to deploy to any *nix environment.

We also provide basic instructions for Windows installations, but we do not recommend this approach.

The project *requires* an OS equipped with **Python**, **Postgresql**, **Git** and **Mercurial**.

There are additional dependencies for production, and for working with static resource management:

* **Node.js** is an optional dependency if you'd like to use Javascript build tools.

* **Redis** is an optional dependency for development environments, but is required for production deployments.

Below we give a basic, opinionated system setup for a number of OSes.

Experienced users may choose to vary from the following instructions.

**IMPORTANT: Ensure you have the minimal system requirements before moving on to install of the project.**


Ubuntu & Debian
-------------

**NOTE:** Use of `sudo` for any command is very dependent on your setup.

Execute the commands without it if you know you don't need it.

Install::

    # required dependencies
    sudo apt-get install python-dev python-pip postgresql postgresql-contrib postgresql-server-dev-all mercurial git-core
    sudo pip install virtualenv virtualenvwrapper

    # optional dependencies in development, required in production
    sudo apt-get install redis-server

    # optional dependencies for working with static resources
    sudo apt-get install nodejs npm
    sudo npm install -g bower less


That's all the packages we need for the system, now we need to configure your user .profile.

Configure::

    # this goes in ~/.profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/{YOUR_USERNAME}/environments"
    export PROJECT_HOME="/home/{YOUR_USERNAME}/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME

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
    sudo npm install -g bower less


That's all the packages we need for the system, now we need to configure your user .bashrc (assuming you use bash, please adjust for other shells).

Configure::

    # this goes in ~/.bashrc
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/{YOUR_USERNAME}/environments"
    export PROJECT_HOME="/home/{YOUR_USERNAME}/projects"
    source /usr/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME

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

    # USING THE BUILTIN PYTHON WITH MAC OS X
    brew install mercurial git node postgresql redis
    sudo easy_install virtualenv
    sudo pip install virtualenvwrapper
    npm install -g bower less


    # ALTERNATIVELY, USING HOMEBREW PYTHON
    brew install mercurial git node postgresql redis python
    pip install virtualenv virtualenvwrapper
    npm install -g bower less

That's all the packages we need for the system. But we need some extra configuration for Postgresql::

    Create the LaunchAgents directory
    mkdir -p ~/Library/LaunchAgents

    # Configure postgresql to launch on system start
    ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents

    # Initialize the postgresql database
    initdb /usr/local/var/postgres -E utf8

    # Create a user with your username on Mac OS X
    createuser {YOUR_USERNAME}

    # Create a database with your username on Mac OS X (for convenience only, not required)
    createdb {YOUR_USERNAME}

Postgresql configured and ready to go. You can verify this with the following command, listing the databases on your system::

    psql -l

Now, we need to configure your user .bash_profile::

    # this goes in ~/.bash_profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/Users/{YOUR_USERNAME}/code/environments"
    export PROJECT_HOME="/Users/{YOUR_USERNAME}/code/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME

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
===================

As long as you have met the system requirements above on your chosen OS, we are ready to install the project.


Configure hosts
-------------

Open Budgets makes use of subdomains to target languages. To enable this functionality fully, you'll need to edit your hosts file on your development machine.

**Ubuntu, Debian & Fedora**::

    sudo nano /etc/hosts

**Mac OS X**::

    sudo nano /private/etc/hosts

Add the following domain mappings for localhost::

    127.0.0.1 openbudgets.dev www.openbudgets.dev en.openbudgets.dev he.openbudgets.dev ar.openbudgets.dev ru.openbudgets.dev

Make a virtualenv
---------------

We are going to setup the project in a new Python virtual environment.

If you are not familiar with virtualenv or virtualenvwrapper, see the following article:

http://docs.python-guide.org/en/latest/dev/virtualenvs/

We are going to:

* Create a new virtual environment
* Create a directory for our project code
* Make a connection between the two
* Clone the project code into its directory


Ubuntu, Debian & Fedora
~~~~~~~~~~~~~~~

Here we go::

    # Create the virtual environment
    mkvirtualenv {PROJECT_NAME}

    # Create a directory for our project code
    mkdir /home/{YOUR_USERNAME}/projects/{PROJECT_NAME}

    # Link our project code directory to our virtual environment
    setvirtualenvproject /home/{YOUR_USERNAME}/environments/{PROJECT_NAME} /home/{YOUR_USERNAME}/projects/{PROJECT_NAME}

    # Move to the root of our project code directory
    cdproject

    # Clone the project
    # Important: Note the **"."** at the end of the git clone command.
    git clone https://github.com/hasadna/openmuni-budgets.git .



OS X
~~~~

Here we go::

    # Create the virtual environment
    mkvirtualenv {PROJECT_NAME}

    # Create a directory for our project code
    mkdir /Users/{YOUR_USERNAME}/code/projects/{PROJECT_NAME}

    # Link our project code directory to our virtual environment
    setvirtualenvproject /Users/{YOUR_USERNAME}/code/environments/{PROJECT_NAME} /Users/{YOUR_USERNAME}/code/projects/{PROJECT_NAME}

    # Move to the root of our project code directory
    cdproject

    # Clone the project
    # Important: Note the "." at the end of the git clone command.
    git clone https://github.com/hasadna/openmuni-budgets.git .


Using virtualenvwrapper
--------------------

virtualenvwrapper provides a nice, human-friendly API over virtualenv commands.

To activate an environment::

    workon {PROJECT_NAME}

To deactivate an environment::

    deactivate


virtualenvwrapper does a whole lot more. See here for the full rundown:

http://www.doughellmann.com/projects/virtualenvwrapper/


Project dependencies
--------------------

All the project dependencies are managed by pip. To get them, run the following command::

    # when setting up for the first time:
    pip install --upgrade -r requirements.txt

We are now ready to start looking at the codebase.


Interacting with the project
-------------------------

We make use of **Fabric**, a great Python tool, for running tasks on the command line. You can treat Fabric as a general CLI for interacting with the project.

The tasks exposed through the Fabric interface cover concerns ranging from code deployment to running the projects tests locally.

Here, we will cover the important commands for developing Open Budgets.

For a more in depth overview, see the Quilt package (a dependency of the project that we wrote) and/or the fabfile package in the codebase.

**Note:** In many cases, our `fab` tasks simply wrap CLI commands for:

* `git`
* `python manage.py`
* `redis-server`
* `psql` and associated CLIs like `createdb` and `dropdb`.

You can *always* use the original CLIs - nothing is hidden. We simply prefer the way that using `fab` standardizes the interface for the developer/user.

First, you can get a list of all available Fabric tasks with the following command::

    fab -l

Next, we'll do a sanity check to make sure we have everything we need. Run the following command::

    fab e local.sanity

If you have any obvious problems, the output of this command will tell you about them.

**NOTE:** What does `e` do?

e is a helper function that sets the current environment. Each environment has its own configuration variables, and the environment is *targeted* with the `e` helper.

By default, `e` with no params picks up the `local` environment - it is shorthand for `e:local`.


Ok, so contining, let's bootstrap the environment. Run the following commands::

    # create a database user for the project
    fab e local.db.createuser

    # build out the project
    fab e local.bootstrap:initial=yes

Now, Let's start the server:

    # This just wraps `python manage.py runserver`, so use that if you prefer
    fab e local.app.start


For now, open the following URL in your browser and you should see the application::

    http://openbudgets.dev:8000/


Fabric Tasks
~~~~~~~~~~

Here are the most common tasks you'll use for development.

bootstrap
+++++++++

Get familiar with the `fab e local.bootstrap` command.

It makes working in your development environment much easier, and abstracts away a bunch of tasks related to rebuilding your database and building out initial data.


Run it::

    # default bootstrap
    fab e local.bootstrap

    # new install when no database exists
    fab  e local.bootstrap:initial=yes


migrate
+++++++

The `fab e local.migrate` command wraps Django/South's syncdb/migrate.

Run it::

    fab e local.migrate


test
++++

The `fab e local.test` command runs the project's test suite.

Run it::

    fab e local.test


mock
++++

The `fab e mock` command builds out a set of dummy data.

Run it::

    fab e mock


dock.* commands
+++++++++++++++

The set of `dock.*` commands are for working with a data repository, and based on a library we extracted from our code called Dock.

**dock.local.clone**

Get the repository from a webserver and install it locally

Run it::

    fab e dock.local.clone

**dock.local.push**

Push changes in the local data repository back to the master

Run it::

    fab e dock.local.push

**dock.local.pull**

Pull changes from a webserver to an existing data repository

Run it::

    fab e dock.local.pull

**dock.local.load**

Load data from the repository into the Open Budgets database.

Run it::

    fab e dock.local.load


db.* commands
+++++++++++++++

The set of `db.*` commands are for working with the database instance.

**local.db.create**

Create a new database for the project.

Run it::

    fab e local.db.create


**local.db.drop**

Drop (delete) the database for the project

Run it::

    fab e local.db.drop


**local.db.rebuild**

Drop the existing database and create a new one for the project.

Run it::

    fab e local.db.rebuild

**local.db.createuser**

Create the default user for the Open Budgets database.

Run it::

    fab e local.db.createuser

**local.db.dump**

Dump data from the database into a Postgresql dump file.

Run it::

    fab e local.db.dump


environ.* commands
+++++++++++++++

The set of `environ.*` commands are for working with the project environment.

**local.environ.ensure**

Ensure that all project dependencies are installed and up-to-date.

Run it::

    fab e local.environ.ensure


Chaining commands
+++++++++++++++++

Commands can be chained. This is very useful! Some common chained commands we use::

    # bootstrap, test, and build out a mock database
    fab e local.bootstrap local.test mock

    # bootstrap, test, and build out a real database
    fab e local.bootstrap local.test dock.local.load


More commands
+++++++++++++

There are many more commands we invoke via the `fab` CLI, including `remote.*` equivalents to most of those mentioned above, for task execution on remote machines.

If you are developing Open Budgets, we urge you to get familiar will this toolset.

You are welcome to make pull requests for more useful fab commands.


Working with data
-----------------

The normal bootstrapping command (`fab e local.bootstrap`) gives the bare minimum data that the project requires to work.

You can also populate the database with a set of mock data (`fab e mock`) just to get a feel for the project.

But ultimately, you want to work with real data.

The Open Budgets project has a set of mechanisms for working with and importing real data.

It is important to become familiar with these features if you want to develop and deploy your own instance of Open Budgets.

By default, the process for working with data and getting it into the database is like this:

* Content editors prepare data according to our required data formats (See the "Specifications" section of the documentation)
* When the data is ready, it is exported to CSV files, and added to the data repository (See the "Specifications" section of the documentation)
* The data is programmatically loaded from the data repository into the database. Once an object is saved to the database, it writes back a unique identifier to the object in the data repository. This is a persistent ID for the life of the instance.

If you are working on an instance of Open Budgets that already has a populated data repository configured, simply run the following command to build out the database::

    fab e dock.local.clone
    fab e local.bootstrap dock.local.pull dock.local.load

**Note:** Loading data like this can take a long time, **if** your dataset includes sheet data, due to the types of checks that run to validate data before it is written to the database. Be *very* patient.

Alternatively, the maintainers of your instance may take data snapshots that are directly importable to Postgresql.

For Open Muni Budgets, the Open Budgets project for Israel Municipalities, we keep such files publicly accessible here:

https://drive.google.com/#folders/0B4JzAmQXH28mM2dtbmJlSDFyUm8

Chose a recent directory based on the naming of the directory (DDMMYYYY), and download an appropriate .sql file to load into Postgresql.

You can load the file via the psql CLI or, place it in the project's 'tmp' directory with the name db_dump.sql, and run the following command (ensure your database is clean before this, by running `fab local.bootstrap`)::

    fab e local.db.load

Similarly, if you want to create a dump file from your working database, run the following command::

    fab e local.db.dump

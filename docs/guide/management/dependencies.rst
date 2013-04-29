Dependencies
============

Overview
--------

Open Budget is written in Python and JavaScript.

System Requirements
-------------------

Make sure your development and/or production server meets these minimal requirements:

* A unix-like OS (We develop and test on Ubuntu and Mac OS X)
* `Python 2.7 <http://python.org/download/>`_
* `Node.js <http://nodejs.org/>`_
* `Git <http://git-scm.com>`_
* virtualenv
* virtualenvwrapper

Python Virtual Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~

Open Budget is not a Node.js app, but we do make use of node.js tools in our development environments.

Make sure you have version **0.8+** installed.

Project Requirements
--------------------

Python
~~~~~~

Python dependencies are managed with pip.

pip install -r requirements.txt

will read the file and install the required dependencies.

Javascript
~~~~~~~~~~

JavaScript dependencies are managed with volo. packages.json in the root of the repository described the package dependencies.

volo add

will read the file and install the required dependencies.

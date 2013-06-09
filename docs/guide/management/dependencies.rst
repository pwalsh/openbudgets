Dependencies
============

Overview
--------

Open Budget is written in Python and JavaScript.

System Requirements
-------------------

Make sure your development and/or production server meets these minimal requirements:

* A unix-like OS (We develop on Ubuntu and Mac OS X)
* `Python <http://python.org/>`_ (2.7.x)
* `Node <http://nodejs.org/>`_
* `Git <http://git-scm.com/>`_
* `Mercurial <http://mercurial.selenic.com/>`_
* The necessary tools to build Python packages (eg: python-dev on Debian systems)
* `virtualenv <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
* `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
* `volojs <http://volojs.org/>`_


Install required packages
~~~~~~~~~~~~~~~~~~~~~~~~~

**Ubuntu**::

    sudo apt-get install python-dev mercurial git-core nodejs python-pip
    sudo pip install virtualenv virtualenvwrapper
    npm install volo -g

**Fedora**::
?

    sudo yum install python-devel mercurial

**Mac OS X**::

    # requires homebrew: http://mxcl.github.io/homebrew/

    brew install mercurial git node
    sudo easy_install virtualenv
    sudo pip install virtualenvwrapper
    npm install volo -g

    # OR, ADVANCED, ONLY if you want to use homebrew python
    brew install mercurial git node python
    pip install virtualenv virtualenvwrapper
    npm install volo -g


Configure virtualenvwrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Make sure you have version **0.8+** or higher installed.

*Note*: Node.js on Ubuntu 12.10 or greater: the node executable was renamed to nodejs, so add this symbolic link which will help with some of our dependencies::

    ln -s /usr/bin/nodejs /usr/bin/node

About volo
----------

`volo <http://volojs.org/>`_ is a tool that automates a lot build and project creation related tasks,
and package management among those. Volo runs on Node.js

For more details see `<https://github.com/volojs/volo#volo>`_

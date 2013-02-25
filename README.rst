Open Budget for Municipalities
==============================

The Open Budget project is a web app and web API for municipality budgets, and related contextual data.

.. image:: https://travis-ci.org/prjts/open-muni.png

Get involved
------------

Code: https://github.com/hasadna/omuni-budget

Issues: https://github.com/hasadna/omuni-budget/issues

Docs: http://open-budget.readthedocs.org/

Demo: http://open-budget.prjts.com/

Discussion: https://groups.google.com/forum/?fromgroups=#!forum/open-muni-dev

HaSadna (Public Knowledge Workshop): http://hasadna.org.il/

5 min install
-------------

Make sure you have the latest version of virtualenv installed, and set it up so you have a directory for your envs, and a directory for your projects.

We are using subdomains extensively, for languages and for the API.

So first, edit your hosts file and add some aliases for 127.0.0.1::

    127.0.0.1 [whatever else you have] he.obudget.dev en.obudget.dev ar.obudget.dev ru.obudget.dev api.obudget.dev obudget.dev www.obudget.dev

With virtualenv setup properly on your machine, do something like::

    mkvirtualenv open-muni

    mkdir /srv/projects/open-muni

    setvirtualenvproject /srv/environments/open-muni /srv/projects/open-muni

    cdproject

    git clone git@github.com:hasadna/open-muni.git .

**Important: Note the "." at the end of the git clone directive.**

Now, you need to set up your settings_local file which is a file that is not in version control. It should be something like this:

https://gist.github.com/pwalsh/4994244


And continuing::

    pip install -r requirements.txt

    python manage.py devstrap -t

    python manage.py runserver

Now go to obudget.dev:8000 in your browser

Now see the docs for full documentation.

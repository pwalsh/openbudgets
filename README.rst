Open Muni
=========

The Open Muni project is a web app and web API for municipality budgets, and related contextual data.

Get involved
------------

Code: https://github.com/hasadna/open-muni

Issues: https://github.com/hasadna/open-muni/issues

Discussion: https://groups.google.com/forum/?fromgroups=#!forum/open-muni-dev

Product requirements: https://docs.google.com/document/d/1cDOELgc4VQ8iPSr6795g0iMMz_klE5dM_s-y2GXbH7o/edit#

More about HaSadna (Public Knowledge Workshop): http://hasadna.org.il/


Installation
------------

See the docs directory for full docs. It is sphinx, so::

    make html

there.

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

And continuing::

    pip install -r requirements.txt

    python manage.py syncdb --migrate

    python manage.py loaddata dev/sites.json

    python manage.py loaddata dev/objects.json

    python manage.py runserver

Now go to obudget.dev:8000 in your browser

Now see the docs for full documentation.

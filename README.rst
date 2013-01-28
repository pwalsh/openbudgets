Open Muni
=========

The Open Muni project is a web app and web API for municipality budgets, and related contextual data.

Get involved
============

Code: https://github.com/hasadna/open-muni

Issues: https://github.com/hasadna/open-muni/issues

Discussion: https://groups.google.com/forum/?fromgroups=#!forum/open-muni-dev

Product requirements: https://docs.google.com/document/d/1cDOELgc4VQ8iPSr6795g0iMMz_klE5dM_s-y2GXbH7o/edit#

More about HaSadna (Public Knowledge Workshop): http://hasadna.org.il/


Quickstart
===========

A simple guide to get started coding.

Build a local environment
-------------------------

Make sure you have the latest version of virtualenv installed, and set it up so you have a directory for your envs, and a directory for your projects. 

eg:

/srv/environments/
/srv/projects/

With virtualenv setup properly on your machine, do the following::

mkvirtualenv open-muni

mkdir /srv/projects/open-muni

setvirtualenvproject /srv/environments/opem-muni /srv/projects/opem-muni

cdproject

git clone git@github.com:hasadna/open-muni.git .

Important: Note the "." at the end of the git clone directive.

pip install -r requirements.txt

python manage.py syncdb --migrate

python manage.py runserver


Open Muni repository practices
------------------------------

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

Search
======

Overview
--------

Open Budgets has a simple feature for end users to discover content via keyword entry. Several text fields across the project models are included in search and it is trivial to add more as required. A single search results page shows the matching results for a query, no matter what the source model of the result, making it simple for common users to get anywhere they need to go in the app.

Open Budgets search is implemented through Haystack, a popular Django extension that provides a common interface to several "search backends". For the backend, we use Whoosh.


Search is built with Haystack on top of a Whoosh search backend. Whoosh is an easy to deploy and highly portale file-based search backend written in Python.

Configuration
-------------

Global
~~~~~~

The main configuration for Open Budgets search is done via the project settings:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/settings/base.py

Here we define the search backend via HAYSTACK_CONNECTIONS, and we also define the scehdules for updating and rebuilding the search index, via CELERYBEAT_SCHEDULE.

Indexes
~~~~~~~

Configuration of data for the search index is per Haystack requirements. Any app that has a search_indexes.py in it's package has models that are registered for search.

Please refer to the Haystack documentation for information on how to make these configurations:

http://django-haystack.readthedocs.org/en/latest/

At present, the following models are indexed:

* Budgets
* Actuals
* Budget Items
* Actual Items
* Entities

Dependencies
------------

Open Budgets search depends on the following 3rd party packages:

* Haystack
* Whoosh
* Celery

Haystack
~~~~~~~~

https://github.com/toastdriven/django-haystack

Haystack is a 3rd party Django app that provides a common interface to a number of search backends. This makes it easy to integrate search into an app, and swap out the search engine with any supported backend, or even add a custom backend.

http://django-haystack.readthedocs.org/en/latest/

How to import::

    from haystack import indexes

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/search_indexes.py

Whoosh
~~~~~~

https://bitbucket.org/mchaput/whoosh/wiki/Home

Whoosh is a file-based search engine written in Python. It is lightweight and easy to use, making it a great solution for simple search tasks.

In Open Budgets, Whoosh is completely behind-the-scenes, and only ever accessed by Haystack.

http://whoosh.readthedocs.org/en/latest/

Celery
~~~~~~

https://github.com/celery/celery

Celery is a very popular python package for task queues.

Celery also has a crontab implementation, making it an ideal replacement for "cron-like" scheduled tasks in Python apps (which is relvant to us here, in our search implementation).

We use Celery in other Open Budgets use cases, but for search, we use Celery Beat to update and rebuild the search indexes at regular intervals.

http://docs.celeryproject.org/en/latest/index.html

How to import::

    from celery.schedules import crontab

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/settings/base.py

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/commons/tasks.py

Project Code
------------

There is no specific custom code for this feature.

All the code in the codebase simply follows settings for Haystack and Celery.

Templates
---------

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/commons/templates/search

We implement a custom search results page.

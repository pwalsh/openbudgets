Admin
=====

Overview
--------

Open Budgets has a dedicated administration interface, based on Django's built-in admin. In addition to the standard CRUD mappings that Django provides over models, we have custom admin views for our data importers.

We are using django-grappelli, which is a 3rd party package that extends the functionality of Django's admin, and adds a more modren and user-friendly skin for the UI.

The goal of an admin interface is to make it as simple as possible for content editors to work with data, so we are maing every effort to go beyond standard Django Admin CRUD mappings, and make the admin more intuitive for these users.

Contributions to Open Budgets should keep this in mind. We consider a feature broken if it is implemented with no thought for how content administrators will interact with the feature via the admin.

Configuration
-------------

For configuration of the admin, please refer directly to the documentation for the Django Admin, and for Grappelli:

https://django-grappelli.readthedocs.org/en/latest/

https://docs.djangoproject.com/en/1.5/ref/contrib/admin/

These sources will guide you through the possibilities of the admin interface.

In addition, you can see our custom dashboard configuration, which controls the way that sections of the admin are displayed by default on the dahsboard page:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/dashboard.py

Dependencies
------------

Open Budgets' admin depends on the no 3rd party packages.

Django
~~~~~~

https://github.com/django/django

Django comes with a bunch of "contrib" apps that provide common web application functionality. The "admin" app is one of those, and our admin sits on this.

https://docs.djangoproject.com/en/dev/ref/contrib/admin/

How to import::

    from django.contrib import admin

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/admin.py

Project Code
------------

RTL
---

Grappelli has basic support for RTL, and we are committed to improving this support via our testing with Hebrew and Arabic in Open Budgets. If you identify speciufic issues regarding RTL support, fix the problem and submit a pull request, or, open a new issue on the issue tracker.

Data Translations
-----------------

Database
~~~~~~~~

TBA.

Codebase
~~~~~~~~

All strings in the codebase are translated via Django's built in features, on top of gettext. When then use Rosetta to expose these files for editing via the admin.

Proxy Models
------------

We make use of ProxyModels_ to custom the admin interface for user accounts. Proxy Models are a great feature of Django, so you should take a look at the docs, and our implementation to see the usefulness.

See our use of Proxy Models here:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/models.py

On top of a normal user account, we have proxies for Core Team users, Content Team users, and Public users. Thus, they appear to content editors as different entities, when in fact they are all just user accounts, and in our case, each type belongs to a different group.

If you contribute code that should be exposed in some way to the admin, please consider the end user - the content editor, and *use Proxy Models* or whatever else is required to make their lives easier.

.. _ProxyModels: https://docs.djangoproject.com/en/dev/topics/db/models/#proxy-models

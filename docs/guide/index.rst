Orientation
===========

Open Budget is written in Python and JavaScript.

Server side, Django provides the application framework. On top of Django, we've built the Web API using Django REST Framework, and we've heavily customized the Admin interface using Grappelli.

You can see additional server side dependencies in the requirements.txt file at the repository root.


Code Management
===============

How we organize and manage our code base.

Dependencies
------------

TODO: pip and volo

Repositories
------------

Git branching

Schema migrations
-----------------

South, and if/how modeltranslations effects this.


Design goals
============

Some of the broader design goals that influenced how we approach Open Budget.

Natively localized
------------------

TODO

Generic implementation
----------------------

TODO

Comparison as meaning-making
----------------------------

TODO


Project apps
============

As a brief overview....

ui and api routes.....

Accounts
--------

Django's user model is extended with a UserProfile.

Budgets
-------

Budget and Actuals data is always mapped to a BudgetTemplate. Depending on the relations of BudgetTemplateNodes, a template maybe flat or a tree.

Any level of government can have a BudgetTemplate, but all members of the same level must share the same template. It is still unclear if/how to deal with change of template overtime. The Israel Muni use case is quite structured, but we probably want to created something more generic.

Contexts
--------

TODO

Entities
--------

Govts are represented by the Entity model, which has realtions with self to build a gvernment structure.

Interactions
------------

The Interactions app deals with all functionality related to the way a user can interact with objects in the web app. For example, Star an object, follow and object, contribute to discussion on an object, and so on.

International
-------------

A key feature of Open Budget is that everything can be localized and internationalized - including model data.

Our custom code for localization and internationalization is located in the "international" app - this app may evolve into a pluggable app in the future.

For localization of files in the project, we of course use Django's built in localization features.

For localization of model data, we use modeltranslation_, a pluggbale app for Django.

For displaying localized data, we use subdomains_ in combination with a custom InterfaceLanguage_ middleware class, that sets a language key based on either (a) user preference, or (b) the request host.

The major reason we decided to expose localized content via subdomains is that it is still the prefered method for indexing via google (here_).

We want Open Budget content to be highly discoverable, and thus we want Google and other search engines to crawl and rank each language as a distinct entity. We have also added language annotations as per those same guidelines to the same end.

.. _modeltranslation: https://django-modeltranslation.readthedocs.org/en/latest/
.. _InterfaceLanguage: https://github.com/hasadna/open-muni/blob/develop/openbudget/commons/middleware.py#L7
.. _subdomains: http://django-subdomains.readthedocs.org/en/latest/
.. _here: http://googlewebmastercentral.blogspot.co.il/2011/12/new-markup-for-multilingual-content.html

Pages
-----


Pages is a simple app to add generic web pages to the system: think about, privacy, and so on.

Transport
---------

TODO

REST API
========

TODO

Commons
=======

TODO

including devstrap


Initial and test data
=========================

TODO

Settings
========

TODO

Admin
=====

The goal of any admin is to make it easy for content editors, not developers, to add content to a system. By default, the Django admin does not deliver on this promise, but it provides a foundation to build on.

First, we are using the excellent Grappelli_ app as our admin framework, overriding the default Django Admin. Grappelli gives us a more user-friendly UI "out of the box", and a nicer API for customizing Django Admin behaviour.

In addition, we have added some tweaks to make Grappelli play nicer with RTL language display, and with the modeltranslations app, and some of our own custom views. We also make extensive use of ProxyModels_ to simplify the admin interface for content editors.

If you contribute code that should be exposed in some way to the admin, please consider the end user - the content editor, and use Proxy Models or whatever else is required to make their lives easier.

**An example of using a Proxy Model**

A great example when to use a Proxy Model is the standard User/UserProfile dance in Django.

It is far from intuitive for a content editor to have two objects in the admin for what should be "one thing" - the User. Use Proxy Models and win. See our examples in account.models and account.admin.

.. _Grappelli: https://django-grappelli.readthedocs.org/en/latest/
.. _ProxyModels: https://docs.djangoproject.com/en/dev/topics/db/models/#proxy-models

Documentation
=============

You are reading it. Powered by Sphinx and hosted on Read the Docs.

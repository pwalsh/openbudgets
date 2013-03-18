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

Python
~~~~~~

Python dependencies are managed with pip.

pip install -r requirements.txt

will read the file and install the required dependencies.

JavaScript
~~~~~~~~~~

JavaScript dependencies are managed with volo. packages.json in the root of the repository described the package dependencies.

volo add

will read the file and install the required dependencies.

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


The Budgets app contains all code related to budgets. This means budget templates and their nodes, budgets and their items, and actuals and their items. Budget, Actual and Budget Templates all should be imported by file - see the Transport app for more information on importing datasets, and see the specs for preparing files for import.

Only administrators with access priveledges can add and edit budget data. Any user or visitor can export budget data.

Why?
~~~~

Modeling budgets for a range of use cases is a difficult problem. Things to consider include how budgets are structured, and how budgets change over time in the way they are classified.

Open Budget provides a platform for comparing budget and actual data of entities that are related. We thus presume some type of consistent order, across entities and over time, and an implementation goal is to provide this type of consistency as appropriate, while still allowing for change in ways that do not break comparative analysis.

How
---

There are three main models: BudgetTemplate, Budget, and Actual.

Each is essentially a container for related nodes: BudgetTemplateNodes in the case of BudgetTemplates, and Items in the case of Budgets and Actuals.

The relations between these models have been designed to suit a number of use cases, as explained below.

Supported use cases
~~~~~~~~~~~~~~~~~~~

**1. Budgets, and Actuals, are declared according to a static BudgetTemplate**

The simplest use case, the system of classification for a budget is known (the BudgetTemplate). A given Budget or Actual will have items that map exactly to the BudgetTemplateNodes of the BudgetTemplate.

Working with data that fits this use case is a matter of:

* Importing a BudgetTemplate into Open Budget
* For an Entity that 'has' this BudgetTemplate, enter a new Budget and/or Actual.
* All the items of the budget or actual should have a 'code' that corresponds to a 'code' in the BudgetTemplate (every node has a code)
* It is ok for a Budget to not have an entry for every node in a template, but expected that the Budget will not have codes that are not in the template


#TODO: EXAMPLE CSV FILE AND AN EXPLICIT TEST FOR THIS

**2. Budgets, and Actuals, are declared according to a static BudgetTemplate, where the Budget Template applies for a given period of time**

This use case is almost identical to the first one, but we want to emphasis it for clarity. A BudgetTemplate has an optional "period_start" attribute, which is a date object. If set, this budget template applies from this date forwards, until it meets the next subseqeunt BudgetTemplate object, or none.

For example, we could have, for "Israeli Municipalities", a BudgetTemplate with a period_start of 1994. If there are no other BudgetTemplates for "Israeli Municipalities", then any Budget or Actual entered into the system with a date of 1994 or after, should comply with this BudgetTemplate.

A Budget with say, a date of 1980, would not be able to be entered - it would have no applicable BudgetTemplate.

Let's say we added another BudgetTemplate to the system for "Israeli Municipalities", with a period_start of 2007. Now, the previous BudgetTemplate would apply for 1994 - 2006. Budgets and Actuals with dates of 2007 and after would use the new template.

* Add logic to check forwards and backwards.

#TODO: EXAMPLE CSV FILE AND AN EXPLICIT TEST FOR THIS

**3. Budgets, and Actuals have a BudgetTemplate, but can also introduce new Nodes that to not exist in the 'official' template**

This is the Israeli Municipality use case as it currently exists:

There is an official BudgetTemplate that all munis must adhere to. In addition to the "official template", munis can add additional "nodes", *where these nodes are children of an existing node*.

#TODO: EXAMPLE CSV FILE AND AN EXPLICIT TEST FOR THIS

**4. Budgets and Actuals have a Template in a way that matches use cases 1, 2, or 3 above, but the relative position of a node changes over time**

TODO

#TODO: EXAMPLE CSV FILE AND AN EXPLICIT TEST FOR THIS

**5. Budgets and Actuals have a Template in a way that matches use cases 1, 2, or 3 above, but the name of a node changes over time**

TODO

#TODO: EXAMPLE CSV FILE AND AN EXPLICIT TEST FOR THIS

**6. Budgets and Actuals have a Template that is barely consistent in structure (at least in a long view over time), and node codes change in *meaning* over time**

TODO

#TODO: EXAMPLE CSV FILE AND AN EXPLICIT TEST FOR THIS

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

The Transport app contains all code related to getting data into and out of the system via files. Only administrators with access priveledges can import data into the system. Any user or visitor can export any data.

Why?
~~~~

Content editors can always use the Admin interface to edit and add data, but this ranges from impractical to impossible when it comes to large, complex datasets like budget and actual reports.

Transport deals with this problem by providing easy to use interfaces for content editors and developers to get large amounts of data into and out of Open Budget through file import and export.

What?
~~~~~

The primary file format for importing data is CSV, and we provide exports in CSV and XLSX formats. Other formats can be added as required. Feel free to open an issue describing a use case, or, even better, make a pull request adding support for your preferred file format(s).

Supported use cases
~~~~~~~~~~~~~~~~~~~

Open Budget V1 supports the importing of Budget Templates, Budgets and Actuals, and the export of all public data. Here we'll talk more about importing, which is by far the most essential and most difficult problem.

Importing Budget Templates
++++++++++++++++++++++++++

Open Budget supports consistent budget classification schemes, where each "type" of "entity" would share (more or less) the same scheme.

We call these classification schemes "Budget Templates". For more information on how Budget Templates are implemented, please refer to the section on the "Budgets" app in "Project apps".

Here we'll presume you are familiar with how the internal machinery works, and get right down to importing a Budget Template.

The first step is to create a CSV file that describes your Budget Template in a way that the transport importer can understand. We have publushed a spec describing a valid Budget Template CSV file here.

Budget Template CSV files can be imported in one of two ways:

1. Via the interactive importer wizard available in the Admin.

2. Via the commandline, following the file naming convention.

Each method has pros and cons. In general, we suggest using the interactive importer wizard until you are dealing with test data.



Importing Budgets and Actuals
+++++++++++++++++++++++++++++

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

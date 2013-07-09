API
===

Overview
--------

Open Budget has a web API to expose all public data stored in an instance.

The API is currently at v1.

The API allows developers to build apps and visualizations on top of Open Budget data.

Data from the API is returned in JSON format.

Additionally, the API is web-browsable - simply go to any API end point in your browser and navigate the API via an HTML interface.

Configuration
-------------

The Open Budget API is built on top of Django REST Framework (DRF), with Django OAuth Toolkit providing access via oauth2 tokens.

All instance-wide configuration is done via the project settings, through the settings that REST Framework and OAuth Toolkit expose:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/settings/base.py

The default settings look something like this::

    # REST FRAMEWORK CONF
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.OAuth2Authentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.AllowAny',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
        ),
        'PAGINATE_BY': 250,
        'PAGINATE_BY_PARAM': 'page_by'
    }

    # OAUTH TOOLKIT CONF
    CORS_ORIGIN_ALLOW_ALL = True

Dependencies
------------

The Open Budget web API depends on the following 3rd party packages:

* Django REST Framework
* Django OAuth Toolkit


Django REST Framework
~~~~~~~~~~~~~~~~~~~~~

https://github.com/tomchristie/django-rest-framework

Django REST Framework has extensive documentation, and also a very active and helpful mailing list for the project. If you want to help develop the Open Budget API, start there for a good understanding of DRF first.

http://django-rest-framework.org/

https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework

How to import::

    from rest_framework import serializers

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/serializers.py

Django OAuth Toolkit
~~~~~~~~~~~~~~~~~~~~


https://github.com/evonove/django-oauth-toolkit

Django OAuth Toolkit is an actively developed package for integrating oauth2 into Django apps.

https://django-oauth-toolkit.readthedocs.org/en/latest/index.html

https://groups.google.com/forum/?fromgroups#!forum/django-oauth-toolkit


API Endpoints
-------------

All endpoints are relative to the API subdomain of the instance domain.

For example, if an Open Budget instance is installed on openmuni.org.il:

* API root: https://api.openmuni.org.il/
* API version: https://api.openmuni.org.il/v1/
* API endpoint: https://api.openmuni.org.il/v1/budgets/


Writing an API Client
---------------------

When writing an API client, is is best to use as little hard coded endpoints to the Open Budget API as possible. This will make it easier for you to update your client to support changes and new versions of the API.

Considering this, we suggest a design along these lines:


Don't hardcode endpoints.

Hardcoding endpoints makes your client brittle in the face of API changes.
Instead, hardcode two variables along these lines:

API_INDEX = "https://api.domain.com/"

API_VERSION = "v1"

This provides your client will all the information it needs to get the correct endpoints on intialization, by follow a flow as follows:


1. On initialization, hit the API_INDEX, and get the URL for v1 from the returned JSON object.

The returned object will look something like this:

{"v1": "https://api.domain.com/v1/"}


2. Hit the version endpoint, which itself returns all its available endpoints.

The returned object will look something like this:

{"entities":"http://api.domain.com/v1/entities/","budgets":"http://api.domain.com/v1/budgets/"}


3. Store the endpoints in an API_ROUTES variable, and use that for API calls.

Something like this:

API_ROUTES = {"entities":"http://api.domain.com/v1/entities/","budgets":"http://api.domain.com/v1/budgets/"}

API_ROUTES.entities # all entities

API_ROUTES.budgets # all budgets


Using the API
-------------

The web API sticks to a RESTful architecture, and returns all data in JSON format.

In production, the API is served over HTTPS only - make sure your client code is compatible with this.

Introduction
~~~~~~~~~~~~

The API features distinct endpoints for each resource type.

Hitting an endpoint direct returns a list of that type.

Appending a resource ID returns a detail view for that resource.

Each list view takes a number of possible query parameters to filter, order, and paginate the list.

All query parameters can be chained.

The common pattern is:

* **?page_by=[INT]** - paginate the results by the given integer. Defaults to 1000.
* **?ordering=[(-)FIELD_NAME]** - order results by the given field. Prepend "-" to the field name to reverse the order. Available field names are listed below per endpoint.
* **?search=[STRING]** - filter the results according to matches for the search query. Available searchable fields are listed, below per endpoint.
* **?[FIELD_NAME]=[VALUE]** - Filter based on value of a field. Depending on the field, value could be an integer, a string, or "true"/"false" for boolean matches. Available fields are listed below, per endpoint.
Also note, pluralized field names (e.g: "parents" can take multiple comma-separated values).


Domains
~~~~~~~

Description
+++++++++++

The domains endpoint provide access to all domain data.

Endpoints
+++++++++

* /domains/
* /domains/[id]/

Allowed Methods
+++++++++++++++

All domains endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Example: https://api.example.com/v1/domains/?page_by=250

Filters
+++++++

* has_divisions [true/false] - returns domains that have divisions
* has_entities [true/false] - returns domains that have entities

Example: https://api.example.com/v1/domains/?has_entities=false

Ordering
++++++++

Order results by the following fields:

* **id**
* **name**
* **created_on**
* **last_modified**

Example: https://api.example.com/v1/domains/?ordering=id,-name

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of all domains.

Example: https://api.example.com/v1/domains/?search=Government


Divisions
~~~~~~~~~

Description
+++++++++++

The divisions endpoint provide access to all division data.

Endpoints
+++++++++

* /divisions/
* /divisions/[id]/

Allowed Methods
+++++++++++++++

All divisions endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Example: https://api.example.com/v1/divisions/?page_by=50

Filters
+++++++

* budgeting [true/false] - returns divisions that are budgeting
* has_entities [true/false] - returns divisions that have entities
* domains [INT, list of comma-separated INT] - returns divisions of the given domain id(s).
* indexes [INT, list of comma-separated INT]  - returns divisions of the given index(es).

Example: https://api.example.com/v1/divisions/?has_entities=false

Ordering
++++++++

Order results by the following fields:

* **id**
* **name**
* **created_on**
* **last_modified**

Example: https://api.example.com/v1/divisions/?ordering=created_on

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of all divisions.

Example: https://api.example.com/v1/divisions/?search=Shumron

Entities
~~~~~~~~

Description
+++++++++++

The entities endpoint provide access to all entity data.

Endpoints
+++++++++

* /entities/
* /entities/[id]/

Allowed Methods
+++++++++++++++

All entities endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Example: https://api.example.com/v1/entities/?page_by=800

Filters
+++++++

* budgeting [true/false] - returns entities that are budgeting
* has_sheets [true/false] - returns entities that have sheets
* divisions [INT, list of comma-separated INT] - returns entities of the given division id(s).
* parents [INT, list of comma-separated INT]  - returns entities of the given parent entity id(s).

Example: https://api.example.com/v1/entities/?parents=3,79,120

Ordering
++++++++

Order results by the following fields:

* **id**
* **name**
* **created_on**
* **last_modified**

Example: https://api.example.com/v1/entities/?ordering=name,id

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of all entities.
* **description** - The description field of all entities.

Example: https://api.example.com/v1/entities/?search=Tel%20Aviv





Sheets
++++++

The sheets endpoints provide access to all budget/actual sheet data. There are endpoints to navigate via sheet objects, and to navigate via sheet item objects. The appropriate strategy will depend on what you are trying to achieve.

**Methods**

All sheets endpoints are read-only, via GET.

**Endpoints**

* /sheets/
* /sheets/[id]/
* /sheets/items/
* /sheets/items/[id]/

**Filter**

Use the following query parameters to customize the sheet list endpoint.

* **'entity'** - return all budgets that belong to the given entity.
* **'template'** - return all budgets that use a given template.

**Search**

Use the search query parameter on the sheet list endpoint to search for free text search over sheets. Search works over the following fields:

* **Period** - the period_start and period_end fields of all budgets
* **Description** - the description fields of all budgets, including translations
* **Entity name** - the name of the entity of this budget, including translations

**Pagination**

* Default: 250
* Custom: Pass an integer to the **page_by** parameter



Ordering
++++++++

Use the following values to the 'ordering' parameter, to sort results by the matching field. prepend the value with - for reverse ordering.

* **period_start**
* **created_on**
* **last_modified**




Templates
~~~~~~~~~

Description
+++++++++++

The templates endpoints provide access to all template data.

Endpoints
+++++++++

* /templates/
* /templates/[id]/
* /templates/nodes/
* /templates/nodes/[id]/

Allowed Methods
+++++++++++++++

All actuals endpoints are read only via GET.

Pagination
++++++++++

* **Default:** 250
* **Custom:** use the 'page_by' parameter, passing an integer

Filters
+++++++

Use the following query parameters to customize the template list endpoint.

* **'divisions'** - return all budgets that belong to the given entity.
* **'budgets'** - return the template used by a given budget.
* **'actuals'** - return the template used by a given actual.

Ordering
++++++++

Use the following values to the 'ordering' parameter, to sort results by the matching field. prepend the value with - for reverse ordering.

* **period_start**
* **created_on**
* **last_modified**

Search
++++++

Search works over the following fields:

* **Name** - the name fields of all templates, including translations
* **Description** - the description fields of all templates, including translations




Contexts
~~~~~~~~

Description
+++++++++++

The contexts endpoints provide access to all context data.

Endpoints
+++++++++

* /contexts/
* /contexts/[id]/

Allowed Methods
+++++++++++++++

All contexts endpoints are read only via GET.

Pagination
++++++++++

* **Default:** 250
* **Custom:** use the 'page_by' parameter, passing an integer

Filters
+++++++

Use the following query parameters to customize the contexts list endpoint.

* **'entity'** - return all contexts of a given entity.

Ordering
++++++++

Use the following values to the 'ordering' parameter, to sort results by the matching field. prepend the value with - for reverse ordering.

* **created_on**
* **last_modified**

Search
++++++

Not applicable at present.

Comments
~~~~~~~~

Description
+++++++++++

The comments endpoints provide access to all comments data.

Endpoints
+++++++++

* /comments/
* /comments/[id]/

Allowed Methods
+++++++++++++++

Comments can be created by posting to the list endpoint.

All other comments endpoints are read only via GET.

Pagination
++++++++++

* **Default:** 250
* **Custom:** use the 'page_by' parameter, passing an integer

Filters
+++++++

Use the following query parameters to customize the comments list endpoint.

* **'model'** - return all comments on a given model. Current possible values are budget_item and actual_item

Ordering
++++++++

Use the following values to the 'ordering' parameter, to sort results by the matching field. prepend the value with - for reverse ordering.

* **model**
* **created_on**
* **last_modified**

Search
++++++

Search works over the following fields:

* **Comment** - the comment fields of all comments.

Projects
~~~~~~~~

Description
+++++++++++

The projects endpoints provide access to all project data.

Endpoints
+++++++++

* /projects/
* /projects/[id]/

Allowed Methods
+++++++++++++++

Projects can be created by posting to the list endpoint.

Only authenticated users can create a project.

Projects can be viewed, updated and deleted from the project detail endpoint.

Only authenticated project owners have permission to update or delete an existing project.

Pagination
++++++++++

* **Default:** 250
* **Custom:** use the 'page_by' parameter, passing an integer

Filters
+++++++

Use the following query parameters to customize the comments list endpoint.

* **'author'** - return all projects by a given author.

Search
++++++

Search works over the following fields:

* **Name** - the name fields of all templates, including translations
* **Description** - the description fields of all templates, including translations

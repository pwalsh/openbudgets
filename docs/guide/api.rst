API
===

Overview
--------

Open Budgets has a web API to expose all public data stored in an instance.

The API is currently at v1.

The API allows developers to build apps and visualizations on top of Open Budgets data.

Data from the API is returned in JSON format.

Additionally, the API is web-browsable - simply go to any API end poUUID in your browser and navigate the API via an HTML UUIDerface.

Configuration
-------------

The Open Budgets API is built on top of Django REST Framework (DRF), with Django OAuth Toolkit providing access via oauth2 tokens.

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

The Open Budgets web API depends on the following 3rd party packages:

* Django REST Framework
* Django OAuth Toolkit


Django REST Framework
~~~~~~~~~~~~~~~~~~~~~

https://github.com/tomchristie/django-rest-framework

Django REST Framework has extensive documentation, and also a very active and helpful mailing list for the project. If you want to help develop the Open Budgets API, start there for a good understanding of DRF first.

http://django-rest-framework.org/

https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework

How to import::

    from rest_framework import serializers

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/sheets/serializers.py

Django OAuth Toolkit
~~~~~~~~~~~~~~~~~~~~


https://github.com/evonove/django-oauth-toolkit

Django OAuth Toolkit is an actively developed package for UUIDegrating oauth2 UUIDo Django apps.

https://django-oauth-toolkit.readthedocs.org/en/latest/index.html

https://groups.google.com/forum/?fromgroups#!forum/django-oauth-toolkit


API endpoints
-------------

All endpoints are relative to the API subdomain of the instance domain.

For example, if an Open Budgets instance is installed on openmuni.org.il:

* API root: https://api.openmuni.org.il/
* API version: https://api.openmuni.org.il/v1/
* API endpoint: https://api.openmuni.org.il/v1/sheets/


Writing an API Client
---------------------

When writing an API client, is is best to use as little hard coded endpoints to the Open Budgets API as possible. This will make it easier for you to update your client to support changes and new versions of the API.

Considering this, we suggest a design along these lines:


Don't hardcode endpoints.

Hardcoding endpoints makes your client brittle in the face of API changes.
Instead, hardcode two variables along these lines:

API_INDEX = "https://api.domain.com/"

API_VERSION = "v1"

This provides your client will all the information it needs to get the correct endpoints on UUIDialization, by follow a flow as follows:


1. On initialization, hit the API_INDEX, and get the URL for v1 (API_VERSION) from the returned JSON object.

The returned object will look something like this:

{"v1": "https://api.domain.com/v1/"}


2. Hit the version endpoint, which itself returns all its available endpoints.

The returned object will look something like this:

{"entities":"http://api.domain.com/v1/entities/","budgets":"http://api.domain.com/v1/budgets/"}


3. Store the endpoints in an API_ROUTES variable, and use that for API calls.

Something like this:

API_ROUTES = {"Entities":"http://api.domain.com/v1/entities/","Sheets":"http://api.domain.com/v1/sheets/","Sheet Items":"http://api.domain.com/v1/sheet/items/"}

API_ROUTES.entities # all entities

API_ROUTES.budgets # all budgets


Using the API
-------------

The web API sticks to a RESTful architecture, and returns all data in JSON format.

In production, the API is served over HTTPS only - make sure your client code is compatible with this.

UUIDroduction
~~~~~~~~~~~~

The API features distinct endpoints for each resource type.

Hitting an endpoint direct returns a list of that type.

Appending a resource ID returns a detail view for that resource.

Each list view takes a number of possible query parameters to filter, order, and paginate the list.

All query parameters can be chained.

The common pattern is:

* **?page_by=[UUID]** - paginate the results by the given UUIDeger. Defaults to 1000.
* **?ordering=[(-)FIELD_NAME]** - order results by the given field. Prepend "-" to the field name to reverse the order. Available field names are listed below per endpoint.
* **?search=[STRING]** - filter the results according to matches for the search query. Available searchable fields are listed, below per endpoint.
* **?[FIELD_NAME]=[VALUE]** - Filter based on value of a field. Depending on the field, value could be an UUIDeger, a string, or "true"/"false" for boolean matches. Available fields are listed below, per endpoint.

Also note, pluralized field names (e.g: "parents" can take multiple comma-separated values).


Domains
~~~~~~~

Description
+++++++++++

The domains endpoint provide access to all domain data.

endpoints
+++++++++

* /domains/
* /domains/[uuid]/

Allowed Methods
+++++++++++++++

All domains endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* has_divisions [true/false] - returns domains that have divisions
* has_entities [true/false] - returns domains that have entities

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **name**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of all domains.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/domains/?page_by=25

http://openmuni.org.il/api/v1/domains/?has_divisions=false

http://openmuni.org.il/api/v1/domains/?has_entities=true

http://openmuni.org.il/api/v1/domains/?search=Government

http://openmuni.org.il/api/v1/domains/?ordering=id,-name


Divisions
~~~~~~~~~

Description
+++++++++++

The divisions endpoint provide access to all division data.

endpoints
+++++++++

* /divisions/
* /divisions/[uuid]/

Allowed Methods
+++++++++++++++

All divisions endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* budgeting [true/false] - returns divisions that actually declare budgets
* has_entities [true/false] - returns divisions that have entities
* domains [UUID, list of comma-separated UUID] - returns divisions of the given domain id(s).
* indexes [UUID, list of comma-separated UUID]  - returns divisions of the given index(es).

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **name**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of all divisions.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/divisions/?budgeting=false

http://openmuni.org.il/api/v1/divisions/?has_entities=true

http://openmuni.org.il/api/v1/divisions/?domains=1

http://openmuni.org.il/api/v1/divisions/?indexes=1,3

http://openmuni.org.il/api/v1/divisions/?search=מחוז

http://openmuni.org.il/api/v1/divisions/?search=מ

http://openmuni.org.il/api/v1/divisions/?ordering=-id


Entities
~~~~~~~~

Description
+++++++++++

The entities endpoints provide access to all entity data.

endpoints
+++++++++

* /entities/
* /entities/[uuid]/

Allowed Methods
+++++++++++++++

All entities endpointss are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* budgeting [true/false] - returns entities that are budgeting
* has_sheets [true/false] - returns entities that have sheets
* divisions [UUID, list of comma-separated UUID] - returns entities of the given division id(s).
* parents [UUID, list of comma-separated UUID]  - returns entities of the given parent entity id(s).

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **name**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of all entities.
* **description** - The description field of all entities.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/entities/?budgeting=false

http://openmuni.org.il/api/v1/entities/?has_sheets=true

http://openmuni.org.il/api/v1/entities/?domains=1

http://openmuni.org.il/api/v1/entities/?divisions=1,3

http://openmuni.org.il/api/v1/entities/?parents=3,79,120

http://openmuni.org.il/api/v1/entities/?search=Tel%20Aviv

http://openmuni.org.il/api/v1/entities/?search=Tel

http://openmuni.org.il/api/v1/entities/?ordering=-created_on


Sheets
~~~~~~

Description
+++++++++++

The sheets endpoint provide access to all sheet data.

endpoints
+++++++++

* /sheets/
* /sheets/[uuid]/

Allowed Methods
+++++++++++++++

All sheets endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* entities [UUID, list of comma-separated UUID] - returns sheets of the given entity id(s).
* divisions [UUID, list of comma-separated UUID] - returns sheets under the given division id(s).
* templates [UUID, list of comma-separated UUID] - returns sheets using the given template id(s).
* budget_gt [DEC] - returns sheets with a budget amount greater than the given amount.
* budget_gte [DEC] - returns sheets with a budget amount greater than or equal to the given amount.
* budget_lt [DEC] - returns sheets with a budget amount less than  the given amount.
* budget_lte [DEC] - returns sheets with a budget amount less than or equal to the given amount.
* actual_gt [DEC] - returns sheets with an actual amount greater than the given amount.
* actual_gte [DEC] - returns sheets with an actual amount greater than or equal to the given amount.
* actual_lt [DEC] - returns sheets with an actual amount less than  the given amount.
* actual_lte [DEC] - returns sheets with an actual amount less than or equal to the given amount.
* periods [UUID, list of comma-separated UUID] - returns sheets matching the given period(s).
* latest [true/false] - returns the latest sheet only, based on period

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **entity__name**
* **period_start**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **entity_name** - The name field of the entities of all sheets.
* **description** - The description field of all sheets.
* **period_start** and **period_end** - The applicable dates for all sheets.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/sheets/?entities=45,90,91

http://openmuni.org.il/api/v1/sheets/?divisions=3,4

http://openmuni.org.il/api/v1/sheets/?templates=2

http://openmuni.org.il/api/v1/sheets/?search=Tel%20Aviv

http://openmuni.org.il/api/v1/sheets/?ordering=-created_on


Sheet Items
~~~~~~~~~~~

Description
+++++++++++

The sheet items endpoint provide access to all sheet item data.

endpoints
+++++++++

* /sheets/items/
* /sheets/items/[uuid]/

Allowed Methods
+++++++++++++++

All sheets endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* with_ancestors [true/false] - returns a nested anscestors object with each item. Prefer alternative query strategies on large querysets if possible.
* has_comments [true/false] - returns sheet items that have associated comments.
* codes [STR, list of comma-separated STR] - returns sheet items that use the given code(s).
* direction ["revenue"/"expenditure"] - returns sheet items that are either revenue of expenditure.
* parents [STR or "none", list of comma-separated UUID, or "none"] - returns sheet items that are children of the given parent sheet item identifier(s). If "none" is passed, returns items with no parent.
* nodes [STR, list of comma-separated STR] - returns sheet items that are related to the given node.
* sheets [UUID, list of comma-separated UUID] - returns sheet items belonging to the given sheet(s).
* entities [UUID, list of comma-separated UUID] - returns sheet items of the given entity id(s).
* divisions [UUID, list of comma-separated UUID] - returns sheet items under the given division id(s).
* budget_gt [DEC] - returns sheet items with a budget amount greater than the given amount.
* budget_gte [DEC] - returns sheet items with a budget amount greater than or equal to the given amount.
* budget_lt [DEC] - returns sheet items with a budget amount less than  the given amount.
* budget_lte [DEC] - returns sheet items with a budget amount less than or equal to the given amount.
* actual_gt [DEC] - returns sheet items with an actual amount greater than the given amount.
* actual_gte [DEC] - returns sheet items with an actual amount greater than or equal to the given amount.
* actual_lt [DEC] - returns sheet items with an actual amount less than  the given amount.
* actual_lte [DEC] - returns sheet items with an actual amount less than or equal to the given amount.
* periods [UUID, list of comma-separated UUID] - returns contexts matching the given period(s).
* comparable [true/false] - returns sheet items filtered by the comparable flag.

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **sheet__entity__name**
* **node__code**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **sheet__entity__name** - The name field of the entity of the sheets.
* **node__code** - The code field of the item node.
* **node__name** - The name field of the item node.
* **period_start** and **period_end** - The applicable dates for all sheets.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/sheets/items/?has_discussion=true

http://openmuni.org.il/api/v1/sheets/items/?direction=revenue

http://openmuni.org.il/api/v1/sheets/items/?parents=1,4,5

http://openmuni.org.il/api/v1/sheets/items/?parents=none

http://openmuni.org.il/api/v1/sheets/items/?codes=6,1

http://openmuni.org.il/api/v1/sheets/items/?entities=65,99

http://openmuni.org.il/api/v1/sheets/items/?divisions=4,5

http://openmuni.org.il/api/v1/sheets/items/?search=Tel%20Aviv

http://openmuni.org.il/api/v1/sheets/items/?ordering=-created_on

http://openmuni.org.il/api/v1/sheets/items/?budget_gt=10000000&direction=revenue

http://openmuni.org.il/api/v1/sheets/items/?actual_lt=100000&direction=expenditure

http://openmuni.org.il/api/v1/sheets/items/?budget_lte=1000000

Templates
~~~~~~~~~

Description
+++++++++++

The templates endpoint provide access to all template data.

endpoints
+++++++++

* /templates/
* /templates/[uuid]/

Allowed Methods
+++++++++++++++

All templates endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* entities [UUID, list of comma-separated UUID] - returns sheets of the given entity id(s).
* divisions [UUID, list of comma-separated UUID] - returns sheets under the given division id(s).
* domains [UUID, list of comma-separated UUID] - returns templates using the given domain id(s).

* Default (no filter) - by default, a list of templates that are explicitly assigned to a division is returned. In a future iteration, we'll have to improve the way template "inheritance" works to change this.

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **name**
* **period_start**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of the templates.
* **description** - The description field of the templates.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/templates/?domains=1

http://openmuni.org.il/api/v1/templates/?divisions=5

http://openmuni.org.il/api/v1/templates/?entities=101

http://openmuni.org.il/api/v1/templates/?search=Tel%20Aviv

http://openmuni.org.il/api/v1/templates/?ordering=-period_start


Template Nodes
~~~~~~~~~~~~~~

Description
+++++++++++

The template nodes endpoint provide access to all template data.

endpoints
+++++++++

* /templates/nodes/
* /templates/nodes/[uuid]/

Allowed Methods
+++++++++++++++

All template nodes endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Filters
+++++++

* entities [UUID, list of comma-separated UUID] - returns sheets of the given entity id(s).
* divisions [UUID, list of comma-separated UUID] - returns sheets under the given division id(s).
* domains [UUID, list of comma-separated UUID] - returns templates using the given domain id(s).
* parents [UUID, list of comma-separated UUID, "none"] - returns nodes that are children of the given item id(s). If "none" is passed, returns nodes with no parent.
* comparable [true/false] - returns template nodes filtered by the comparable flag.
* Default (no filter) - by default, a list of templates that are explicitly assigned to a division is returned. In a future iteration, we'll have to improve the way template "inheritance" works to change this.

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **name**
* **description**
* **created_on**
* **last_modified**

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of the templates.
* **description** - The description field of the templates.

Example queries
+++++++++++++++

http://openmuni.org.il/api/v1/templates/nodes/?templates=1

http://openmuni.org.il/api/v1/templates/nodes/?entities=4,5

http://openmuni.org.il/api/v1/templates/nodes/?search=Tel%20Aviv

http://openmuni.org.il/api/v1/templates/nodes/?ordering=last_modified

http://openmuni.org.il/api/v1/templates/nodes/?parents=100,101

http://openmuni.org.il/api/v1/templates/nodes/?parents=none

Contexts
~~~~~~~~

Description
+++++++++++

The contexts endpoint provide access to all contextual data.

endpoints
+++++++++

* /contexts/
* /contexts/[uuid]/

Allowed Methods
+++++++++++++++

All contexts endpoints are read only via GET.

Pagination
++++++++++

Implements API defaults.

Example: http://openmuni.org.il/api/v1/contexts/?page_by=100

Filters
+++++++

* entities [UUID, list of comma-separated UUID] - returns contexts of the given entity id(s).
* divisions [UUID, list of comma-separated UUID] - returns contexts under the given division id(s).
* domains [UUID, list of comma-separated UUID] - returns contexts using the given domain id(s).
* periods [UUID, list of comma-separated UUID] - returns contexts matching the given period(s).

Example: http://openmuni.org.il/api/v1/contexts/?entity=4,5

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **entity__name**
* **period_start**
* **created_on**
* **last_modified**

Example: http://openmuni.org.il/api/v1/contexts/?ordering=id,last_modified

Search
++++++

Filter list by searching over the following fields:

* **data** - The data field of the contexts.
* **entity__name** - The name of the context entities.

Example: http://openmuni.org.il/api/v1/contexts/?search=Pension


Projects
~~~~~~~~

Description
+++++++++++

The projects endpoints provide access to all project data.

endpoints
+++++++++

* /projects/
* /projects/[uuid]/

Allowed Methods
+++++++++++++++

Projects can be created by posting to the list endpoint.

Only authenticated users can create a project.

Projects can be viewed, updated and deleted from the project detail endpoint.

Only authenticated project owners have permission to update or delete an existing project of their own.

Pagination
++++++++++

Implements API defaults.

Example: http://openmuni.org.il/api/v1/projects/?page_by=100

Filters
+++++++

None.

Ordering
++++++++

Order results by the following fields:

* **uuid**
* **created_on**
* **last_modified**

Example: https://api.example.com/v1/projects/?ordering=id,last_modified

Search
++++++

Filter list by searching over the following fields:

* **name** - The name field of the projects.
* **description** - The description field of the projects.
* **author name** - The name fields of the author of the projects.
* **owner name** - The name fields of the owner of the projects.

Example: https://api.example.com/v1/projects/?search=Education

API
===

Overview
--------

Open Budget has a web API to expose all data stored in an instance. One the the defining goals of the project is to provode a common standard for retrieving budgetary data in a given context.

In addition, we use the web API ourselves for all single page apps in the code base (Admin Data Importer, Visualization Framework, Query Builder).

Configuration
-------------

See the documentation for Django REST Framework for configuration details (links in dependencies below).

Dependencies
------------

The Open Budget API is built with Django REST Framework. You can find extensive documentation, and also a very active and helpful mailing list for the project:

**Code:** https://github.com/tomchristie/django-rest-framework

**Docs:** http://django-rest-framework.org/

**List**: https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework

In particular, please refer to these parts of the DRF docs if you want to work on developing the Open Budget API:

http://django-rest-framework.org/api-guide/serializers.html

http://django-rest-framework.org/api-guide/generic-views.html

http://django-rest-framework.org/api-guide/authentication.html

Project Code
------------

All project code is contained in the api package, adjacent to apps:

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/api

API Browser
~~~~~~~~~~~

Django REST Framework provides an API browser out of the box. This is a *very* handy tool for understanding how the API works. The API browser is accessible at the same end points as the API itself - just visit in your browser. See it on the demo project:

http://api.open-budget.prjts.com/

Serializers
~~~~~~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/api/serializers.py

Please make sure you are familiar with serializers in Django REST Framework:

http://django-rest-framework.org/api-guide/serializers.html

For the most part, we use Hyperlinked Model Serializers.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/api/views.py

Standard views for Django/DRF returning serialized objects.

URLs
~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/api/urls.py

A standard django urls object to map views.

Middleware
~~~~~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/api/middleware.py

Some copy/paste middleware at the moment.

TODO: YEHONATAN - clean this up.

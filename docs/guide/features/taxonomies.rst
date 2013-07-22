Taxonomies
==========

Overview
--------

Open Budget aims to have support for taxonomies of Budget and Actual data.

A "taxonomy" is, in our case, an alternate classification system for items in a budget.

Taxonomies can provide topically-driven views of budget data that break out of the restrictions of the budget template itself. In particular, taxonomies can be a powerful tool for experts with particular domain knowledge. One can envisage scenarios where an expert could, for example, create a taxonomy to look at a given budget through the lens of "Children's Health".

Feature Status
--------------

Taxonomies have been implemented in the server. the 0.3 tag of Open Budget exposes a few demo taxonomies to the UI in user accounts, budget pages, and dedicated taxonomy pages.

Subsequent tags have removed taxonomies fromt he UI as they are not in the current project's scope.

TODO: After the current iteration of the project, we hope that the taxonomies feature can be picked up and implemented.

At present, a taxonomy has a foreign key to BudgetTemplates. This relation suggests that taxonomies should be created as alternative ways to "read" a template, and thereby, any budget or actual that maps to such a template, can map to a taxonomy.

We initially did this as it enables us to more easily use taxonomies for comparision.

It may be better to consider further implications of this relation as we progress with documenting some real use cases. Perhaps taxonomies should map directly to given budgets/actuals.

Configuration
-------------

There is no particular configuration for taxonomies.

Dependencies
------------

Open Budget taxonomies depend on the following 3rd party packages:

* taggit

Taggit
~~~~~~

https://github.com/alex/django-taggit

Django taggit is a tagging framework. We have used the taggit API to adapt the defult implementation to our taxonomy use case.

http://django-taggit.readthedocs.org/en/latest/

How to import::

    from taggit.models import ItemBase as TaggitItemBase

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/taxonomies/models.py

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/taxonomies/models.py

Taxonomy
++++++++

Taxonomy is a container object that groups together tags.

Tag
+++

Any Tag belongs to a given taxonomy and has a name and a slug.

TaggedNode
++++++++++

TaggedNode relates a tag to any object. The assumption (as noted by the naming of the class), is that it will be a BudgetTemplateNode. This is not however, directly enforced.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/taxonomies/views.py

Standard views to expose a taxonomy detail page and a tag detail page.

URLs
~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/taxonomies/urls.py

Standard urls to expose a taxonomy detail page and a tag detail page.

Templates
~~~~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/taxonomies/templates/taxonomies

A tag detail view, to see a specific tag in a taxonomy. This shows the items that have been tagged.

A taxonomy detail view, to see a taxonomy and all the new tags it declares.

Entities
========

Overview
--------

Open Budgets has a flexible system for supporting budgeting entities, be they corporations, governments, non-profits, and even all of the above in the same Open Budgets instance.

To achieve this, we have a system that declares certain entity relations where a *Domain* is the overall context for an entity, *Divisions* are logical, distinct divisions in a domain (according to the business logic of the domain), and *Entities* are the actual entities that are present in the domain.

How it works
~~~~~~~~~~~~

In explaining the Domain/Division/Entity relations, we'll demonstrate with concrete examples of Israeli governmental system - the major context for the first iteration of Open Budgets.

Domain
++++++

A Domain is the ultimate context for the entities in the system. There can in fact be multiple domains, each describing different "entity systems", but this has not been actualized in views and templates of the current codebase.

To explain by example, imagine we want to use Open Budgets for the Budget and Actual data of municipalities in Israel (our first use case).

In this case, our Domain is "Government", or more precisely, "Israel Government". (Remember, in terms of the data model, we could have a single instance of Open Budgets with an "Israel Government" Domain and an "Australian Government" Domain.)

Let's move on to see how we break up (divide) this domain according to its actual structure.

Division
++++++++

A Division describes some type of logical division for a domain - it could be administrative, geographical, ad hoc - anything that makes sense according to the Domain's internal logic.

For our "Israel Government" example, we look at the structure of the government, and see how it breaks down from the national to local level.

We see that in Israel, the government has the following official administrative divisions:

* State
* District
* Sub-District
* City Muncipality
* Local Muncipality
* Regional Muncipality

Now, we cannot assume that each division is a node in a strict hierarchical tree.

For example, in the Israeli case, some of our City Municipalities belong directly to a District, yet most of them belong directly to sub-districts.

Another example: the three "municipality" types are at an equal level in the "tree", and the distinction is based on things like square meterage and population.

So, instead of having a parent relationship to self, we have a more flexible index field, which is an integer, where 0 represents the top level, and subsequent numbering the subsequent levels.

Explicitly, in our Israeli case, the division structure is as follows:

* State: 0
* District: 1
* Sub-District: 2
* City Municipality: 3
* Local Municipality: 3
* Regional Municipality: 3

We also note that note that not all entities declare budgets. In the Israel Government example, the State declares budgets, and the Municipality types declare budgets.

The other levels of government serve purely administrative roles. So, our DomainDivision model has a boolean flag "budgeting", to indicate if entities of this division declare budgets. This flag is a helper for views and templates, when querying over entities for sheet (budget) data.

Entity
++++++

Our Domain and Division models provide scope the Entity objects.

An entity is any "unit", "group", or, well, "entity" in the Domain.

In our Israel Government case, we have an entity "Israel" (which belongs to the "State" domain division), and we have a number of entities that belong to the "City Municipality" domain division, such as "Tel Aviv", "Jerusalem", "Haifa", "Ra'anana" and so on.

Let' take another example to illustrate entities, with a completely different Domain/Division/Entity set. We'll take an example from the corporate world.

Say we have a Domain "Google Corp", a corporation big enough to theoretical have a complex administrative structure all of its own.

We might have the following structure for "Google Corp":

* Global: 0 [entity: "Google"]
* Region: 1 [entities: "USA", "UK", "Australia", "Israel"]
* Department: 2 [entities: "Marketing",parent:US; "Marketing",parent:UK; and so on]

Configuration
-------------

There are no configuration options for Entities.

Dependencies
------------

There are no dependencies for Entities.

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/entities/models.py

Above, in "How it works", we describe the relationship between the Domain, Division and Entity models.

While Domain and DomainDivision provide the context for entities, it is actually the Entity model where most of the important stuff happens. Budgets and Actuals ultimately belong to this or that entity.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/entities/views.py

The views are straight forward views to return list and detail views of entities.

URLs
~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/entities/urls.py

The urls are straight forward views to return list and detail views of entities, sheets, sheet items, and templates.

Templates
~~~~~~~~~

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/apps/entities/templates/entities

Simple templates for entity list and detail views.

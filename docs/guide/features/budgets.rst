Budgets
=======

Overview
--------

Open Budget has a lot of features, but it is all for the purpose of working with budgetary data.

We explictly support Budgets and Actuals, where the Budget/Actual applies for a period of time (commonly a year, but we don't enforce any particular period in the data model).

Additionally and importantly, we work with a concept of "Budget Templates".

One of the main goals of Open Budget is **comparative analysis of comparable entities**.

Our approach to handling this reasonably is that comparable entities should share the same Budget Template (we also have flexibility for variation from the template, but more on that later).

So, there are three major models in our implementation: *Budgets*, *Actuals*, and *Budget Templates*.

All code for dealing with budgetary data can be found in the "budgets" app.

Features
--------

Budget Templates
~~~~~~~~~~~~~~~~

A BudgetTemplate (which has BudgetTemplateNode children) describes the structure of a given Budget or Actual.

Budgets and Actuals
~~~~~~~~~~~~~~~~~~~

A Budget or an Actual (which have BudgetItem and ActualItem children respectively) contains all data for a budget or an actual of a given entity for the declared *period*.

Context and Assumptions
-----------------------

Modeling budget data for comparative analysis presents a bunch of challenges. So, here we will document the context of our decisions, the assumptions that our decisions are based upon, and finally, the use cases we expect to support.

Primary considerations
~~~~~~~~~~~~~~~~~~~~~~

* Open Budgets is designed for comparative analysis of budgets
* In order to compare, we have to assume some commonality between budgets of entities we are comparing
* Even fairly structured budgets will change their structure over time.
* Change of a budget structure could be that "items" or "nodes" of the budget are added, removed, moved and merged
* To enter data into the system, the data must first comply with a format specification we define

Israeli Municipality Use Case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The current scope of Open Budgets is to serve as a platform for the budgetary data of Israeli municipalities specifically.
* Budget data must adhere to the offical template for Israel Muni budgets, issues by the Ministry of the Interior
* The official Template describes a fixed structure, but also allows for "custom" nodes, that are children of "official" nodes, in certain conditions

Supported Use Cases
~~~~~~~~~~~~~~~~~~~

In order to support the Israeli Muni use case, and with an eye to a generic implementation of budget storage and comparative analysis, we have identified the following use cases we support.

1. Data adheres to a static template
++++++++++++++++++++++++++++++++++++

The simplest use case, the structure for a budget is known and adhered to exactly.

In this case, each BudgetItem or ActualItem will map exactly to a BudgetTemplateNode that exists in the default BudgetTemplate for that entity.

A workflow for this use case:

* An admin user writes the Budget Template, according to our specifications for import, and imports this template into the system
* An admin enters a Budget or Actual that conforms to the Budget Template (meaning, each item in the Budget or Actual has a "code" that maps to a node in the Budget Template).
* Not every node needs to have an item. But, every item shoudl have a node.

2. Data adheres to a static template, scope by period
++++++++++++++++++++++++++++++++++++++++++++++++++

Almost exactly the same as the previous use case, but where there are multiple Budget Templates for the given entity, but each one is unique to a specific period of time.

For example, one template could apply for 1980 - 1990, and a another one from 1991 - 2013.

A workflow for this use case:

* Exactly as above, but the Budget or Actual being entered must reflect the structure of the period in which it belongs.
* So, a Budget for 1990 would be mapped to the first template above, and a budget for 1991 would be mapped to the second template above.

**Mapping across Budget Templates**

TODO: Need to check this further and specify when forwards/backwards is useful, and when it will not be.

Presuming a high degree of commonality between Budget Template 1 and Budget Template 2, the nodes of each template can be mapped to each other, indicating equivalence, so that queries can be made across templates.

3. Data adheres to template, but can also introduce new child nodes
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This is the main use case we need to support for Israel Municipality budgets, where there is an official budget template, and, a a certain depth in the "template tree", individual munis can further break down budget items with their own (compliant) codes, which are children, or children of children, of nodes in the template.

Unsupported Use Cases
~~~~~~~~~~~~~~~~~~~~~

We'd like to support these use cases, but more conde contributions, refactoring, testing, and so on. Some of these use cases are partially supported but compeltely untested.

4. Relative position of nodes in a tree can change over time
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Meaning and name does not change.

5. Name of a node changes over time, but meaning does not
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TODO

6. Meaning of a node code changes over time
+++++++++++++++++++++++++++++++++++++++++++

TODO

7. Budget has no obvious consistency, but expert can map nodes
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TODO

Configuration
-------------

There are no specific configuration options for budgets.

Dependencies
------------

There are no dependencies for budgets.

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/models.py

BudgetTemplate
++++++++++++++

BudgetTemplate is a container object that describes the structure of a Budget or an Actual.

In our current use case, there is an "official" template issued by the Israel Ministry of the Interior, which is supposed to be used by municipalities when creating a budget.

In theory, there is no requirement that BudgetTemplate refers to some official template.

The main consideration here is the separation of structure (template) from data (budget and actual).

This let's us build an infrastructure for comparative analysis across comparable budgeting entities (those that more or less work to the same "template"), and over time (we map changes to a template over time via forwards and backwards relations on nodes).

Note that BudgetTemplate has a divisions field, relating any given template to one or more DomainDivisions. This is how we know if given entities are "comparable".

If they (more or less) follow the same budget template, they are comparable. In our use case, our entities belong to the division "City Municipalities", and thus all share the template for City Municipalities.

If we find later that "Local Municipalities" and "Regional Municipalities", for example, also follow the same template, then we will be able to do comparative analysis across these different entity types.

BudgetTemplateNode
++++++++++++++++++

BudgetTemplateNodes are the actual items, categories, sections that make a budget template. via a parent relation to self, we can express a tree-like classification system.

Any node has to be either of the type REVENUE or EXPENDITURE.

It is possible in some budget templates that REVENUE nodes have a direct relation to EXPENDITURE nodes. This is a feature present in the Israeli Municipality use case, for some nodes and not others. We implement this via the 'inverse" field.

TODO: Backwards, forwards, templates: YEHONATAN

BudgetTemplateNodeRelation
++++++++++++++++++++++++++

A through table for the relations between nodes and templates. We have our own custom through table because we want to enforce unique contraints that we can't acheive with Django's default m2m implementation.

with the unique constraints on this table and on BudgetTemplateNode, the following must be unique together:

code, parent, name, template

Sheet (Budget and Actual)
+++++++++++++++++++++++++

Sheet is the model for the Budget or Actual "container" objects.

BudgetItem and ActualItem both inherit from SheetItem, and simply intoduce fields and methods to get to Budget or Actual objects respectively.

A Sheet has a period for which it is applicable, and a template that it adheres to. Any sheet object is either a Budget or an Actual for a given entity.

SheetItem (BudgetItem and ActualItem)
+++++++++++++++++++++++++++++++++++++

SheetItem is the model for items in a Budget or Actual.

BudgetItem and ActualItem both inherit from SheetItem, and simply intoduce fields and methods to get to Budget or Actual objects respectively.

SheetItems are grouped together by a FK relation to a Budget or an Actual.

Sheet Items are mapped to a template via the node field. SheetItems simply delcare an amount, and a description text if available.


Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/views.py

A set of standard views to return all objects in the budgets app to templates.

URLs
~~~~

No urls.

Templates
~~~~~~~~~

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/apps/budgets/templates/budgets

A set of standard templates for list and detail views of all models in the budgets app.

Budgets
=======

Overview
--------

The Interactions app deals with all functionality related to the way a user can interact with objects in the web app. For example, Star an object, follow and object, contribute to discussion on an object, and so on.

Configuration
-------------


Dependencies
------------


Project Code
------------

Models
~~~~~~

Forms
~~~~~

Views
~~~~~

URLs
~~~~

Templates
~~~~~~~~~

Template Tags
~~~~~~~~~~~~~



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
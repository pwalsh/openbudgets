Sources
=======

Overview
--------

Open Budgets supports adding sources for any data added to the system. A "source" in this case is a file, or a webpage (or a number of files/web pages) that served as raw data for the dataset n Open Budgets.

This gives the ability to trace where data came from, and save those data sources in Open Budgets, in case they should in the future become inaccessible from the original source.

In the current codebase, we distinguish between two types of sources, *Reference Sources*, which are added by Open Budgets admins along with data that is added to the system, and *Auxiliary Sources*, which authenticated users can add in relation to a given dataset in Open Budgets, to enrich the context of that data.

Note: Due to time contraints, we have not exposed any UI for Auxiliary Sources for the current version of the codebase.

Configuration
-------------

There is no particular configuration for sources.

Sources are implemented via generic relations, so adding reference sources to a model that currently does not expose them, is a matter of following Django conventions for generic relations, and exposing forms in the admin.

Dependencies
------------

There are no dependencies for sources.

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/sources/models.py

We have an abtract DataSource model, which is inherited by ReferenceSource and AuxSource.

A DataSource has a set of fields that allows the content admin to add a file to the system, add a URL for the source of the file =, and write notes on the data source.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/sources/views.py

A standard Django URl file to expose detail views of given resources.

URLs
~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/sources/urls.py

A standard Django URl file to expose detail views of given resources.

Templates
~~~~~~~~~

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/apps/sources/templates/sources

Simple templates to expose detail views of given sources.


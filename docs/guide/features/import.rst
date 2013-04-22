Import
======

Overview
--------

Open Budget has a set of data importers, making it easy to get budget data into the system. Code for the data importers is located in the "transport" app.

Importing data is currently only exposed to Admin users (but anyone can export data in a range of formats). Imported data must be validated before it is exposed via the app and the API.

For this iteration of the project, the importer supports importing Budget Templates, Budgets, and Actuals.

Features
--------

Simple Importer
~~~~~~~~~~~~~~~

Mostly for development.

Data Importer
~~~~~~~~~~~~~

Importer.



Configuration
-------------

There is no specific configuration guide for the importers. However, the DataImporter class takes a number of keyword arguments on initialization which can be used to customize the import.

Dependencies
------------

The transports app, which handles all importing logic, depends on the following 3rd party packages:

* tablib

Tablib
~~~~~~

https://github.com/kennethreitz/tablib

Tablib is a great python package for manipulating tabular datasets. We use it to get data from files, and manipulate that data before hitting the database. We also use Tablib in other places to export data in supported file formats.

http://docs.python-tablib.org/en/latest/

How to import::

    from tablib import import_set

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/transport/incoming.py

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/transport/models.py

String
++++++

The string model serves a simple but very important purpose, due to the multilingual nature of Open Budget. Using the string model, an administrator can map alias string to the strings required for headers in data files for import.

The required Strings are loaded to the database in the initial_data fixture.

Alias strings can be added as children of a required string.

We ship a set of alias strings in the language key fixtures.

More can be added at will.

On import, the strings (String objects and from the file headers) are stripped of spaces and forced to lower case, to map aliases to the parent strings.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/transport/views.py

FileImportView
++++++++++++++

This view takes a file and passes it to incoming.DataImporter.

ImportSuccessView
+++++++++++++++++

This view is returned on a successful import.

FileExportView
++++++++++++++

TBD: Refactor along the lines of FileImportView, where here, we'll take a DB query and pass it to outgoing.DataExporter, which will be our class for all exporting code.

Forms
~~~~~

FileImportForm
++++++++++++++

A simple form that takes a file only.

This form is used in the DataImportView, requires that the filename follows the naming conventions for file only import. This view is present for ease of use in development, where filling in a form of meta.


Incoming
~~~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/transport/incoming.py

The incoming module has code for getting data from files that users upload, validing the data, saving clean datasets as files, and ultimately, written new data to the database.

At present, the DataImporter class is responsible for all this functionality.

DataImporter
++++++++++++

The DataImporter class takes a file structured according to our data import specifications, processes the data, and enters it into our data storage.


Outgoing
--------

Functions and classes to get data out of the system. We currently have data elsewhere to export to CSV and Excel.

TBD: Get all output code to here, and reuse this.

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



Open Budget supports consistent budget classification schemes, where each "type" of "entity" would share (more or less) the same scheme.

We call these classification schemes "Budget Templates". For more information on how Budget Templates are implemented, please refer to the section on the "Budgets" app in "Project apps".

Here we'll presume you are familiar with how the internal machinery works, and get right down to importing a Budget Template.

The first step is to create a CSV file that describes your Budget Template in a way that the transport importer can understand. We have publushed a spec describing a valid Budget Template CSV file here.

Budget Template CSV files can be imported in one of two ways:

1. Via the interactive importer wizard available in the Admin.

2. Via the commandline, following the file naming convention.

Each method has pros and cons. In general, we suggest using the interactive importer wizard until you are dealing with test data.


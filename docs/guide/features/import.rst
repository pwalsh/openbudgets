Import
======

Overview
--------

Open Budget has a set of data importers, making it easy to get budget data into the system. Code for the data importers is located in the "transport" app.

Importing data is currently only exposed to Admin users (but anyone can export data in a range of formats). Imported data must be validated before it is exposed via the app and the API.

There are in fact two ways to import data: via an interactive, user-facing importer, and also via a commandline importer.

For the most part, the commandline importers are for bootstrapping an instance. Our main focus is on the interactive importer, and improving that. The focus of this section of the documentation is on the interactive importer.

At this stage, the interactive import works with Templates and Sheets.


Dependencies
------------

The transports app, which handles all importing logic, depends on the following 3rd party packages:

* tablib

Tablib
~~~~~~

https://github.com/kennethreitz/tablib

Tablib is a great Python package for manipulating tabular datasets.

We use it to get data from files, and manipulate that data before hitting the database.

We also use Tablib in other places to export data in supported file formats.

http://docs.python-tablib.org/en/latest/

How to import::

    from tablib import import_set

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/transport/incoming/importers/tablibimporter.py

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

The current implementation take arguments for model, object and format, and returns a file of the data. model in the current case can only be budget or actual.

TODO: Refactor along the lines of FileImportView, where here, we'll take a DB query and pass it to outgoing.DataExporter, which will be our class for all exporting code.

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

TODO: Get all output code to here, and reuse this.

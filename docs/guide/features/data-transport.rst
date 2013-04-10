Data Transport
==============

The Transport app contains all code related to getting data into and out of the system via files. Only administrators with access priveledges can import data into the system. Any user or visitor can export any data.

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


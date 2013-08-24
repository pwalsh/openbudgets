Data Import
===========

Overview
--------

Open Budgets deals with large datasets. A primary focus of the project is to make it easy to import large datasets in bulk. There is still much work to do here, but we have a good start.

Importing datasets requires preparation. First and foremost, the data needs to be in a file format that Open Budgets can understand. At present, this means in CSV format, with the file encoded in UTF-8. Additionally, each single CSV file must describe only one, and a complete, dataset.

We have an ongoing community project at present to allow support direct import from a Google Spreadsheet, bypassing the need to save to a CSV file.

At present, the following datasets can be imported in bulk:

* Templates (via interactive import only)
* Sheets (via interactive import only)
* Domains (via command line import only)
* Divisions (via command line import only)
* Entities (via command line import only)
* Contexts (via command line import only)

This section of the documentation deals with the file structure we specify for each importable dataset.

For more information on the actual importing mechanisms, please see the "Import" page of the "Features" section of the guide.

Dependencies
------------

To create an importable file of the correct type, you'll need to use any spreadsheet app that can output as CSV in UTF-8 encoding.

We work with Google Docs, which is a great choice for creating and collaborating on the files before importing.

Workflow
--------

I'll describe our current workflow. It is not optimal, and not required, but it is "how we do things" at present.

1. Get some source data
~~~~~~~~~~~~~~~~~~~~~~~

The first step, of course, is to get some source data. Source data comes from a range of sources, depending on the dataset. For example, in the Israel Municipality case, "Context" data comes from the Central Bureau of Statistics, and "Budget" data comes from each individual municipality.

2. Enter source data into required data structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is very rare that the source data will come in a format that is importable.

Further, the vast majority of source data features errors.

So, we currently do a manual process (this can, in large part, be automated) of taking the source data, and converting it to an importable structure.

We currently use Google Docs exclusively for this task. There are several advantages to using Google Docs. Obviously, collaboration is easy. Additionally, it opens the possibility of adding data validations that can help prevent data entry errors. We currently employ several data validations on "Sheet" datasets.

3. Initial validation  of data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the data is in a Google Spreadsheet, we review the data in comparison to the source, and, if the dataset has validations, we review for validation warnings. For example, we use cross-document validations between "Template" and "Sheet" docs, to check that budgets follow the template they are supposed to.

4. Create importable file
~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, we still need a CSV file for importing data. Therefore, we export CSV files from Google Docs, one file per dataset.

5. Import data into database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We then take this exported CSV and import, either via the interactive importer or via the command line importer.

In the commandline importer, import into the database will fail if the dataset is not valid.

In the interactive importer, a validation process takes place before any attempt to put data into the database. If the dataset is invalid for any reason, the user will get notification, along with specific instructions for the invalid data.


Specifications
--------------

Common
~~~~~~

Basic Requirements
++++++++++++++++++

* A compliant CSV file that is UTF-8 encoded
* Data that matches the exact expected input for the dataset you want to import
* One single datapoint per cell - no overloading of cells for multiple data points

Header Requirements
+++++++++++++++++++

* The first row in any CSV file must be for "Headers", where the header describes the data in its column.
* Only one row can be a header - the importer does not support multiple header rows.
* There are specific "strings", or, "keywords" that each dataset expects to find as headers. Unknown headers mean that data cannot be imported.
* Alias keywords can be created via the admin to map to out required header keywords. This can help if, for example, non-english data source providers prefer headers in a different language - see the features/import page for more information on this feature.

Data Requirements
+++++++++++++++++

The importer does a range of validations on data to be imported, but there are always corner cases or use cases we perhaps did not predict.

To make things easier, check the following in your source file before trying to import:

* Each column in your file is a valid data column for the dataset you are trying to import
* Where columns are required for import (for example, "code" in Templates), the import will be prevented if an item is missing a required value - check and double-check that your dataset is complete

Template
~~~~~~~~

A Template describe a structure for budget sheets.

There can be multiple templates, applicable at different points in time, and applicable to different Divisions in a Domain. For example, one template for Israel Municipalities between 1994 and 2013, another from 2014 - 2018, and another template for the Israel State from 2010-2011.

When importing a  template, every row in the file must be a distinct Template Node.

In addition, you'll fill out some form fields on import that provide us with other required metadata for the dataset: Name of the template, what divisions it applies to, and the period of time for which it is valid.

All headers are required, even if some columns may be completely empty (because not all **data** is required).

Please see the example Template Format worksheet:

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdGllRS1EWFB2aFF3Qk5DbHgyakE4Q0E#gid=4

And, here is an example dataset, the Israel Municipality Budget template, applicable from 1994 onwards:

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdC12X3FrWi13VjU4bnh4dnZJekNTQXc#gid=4


Sheet
~~~~~

A Sheet describes budget and actual data for a given Entity, in a given period.


As with importing a Template, you'll fill out some form fields on import that provide us with other required metadata for the dataset: Name of the entity the Sheet is for, period of the Sheet, a description text for the budget, and so on.

All headers are required, even if some columns may be completely empty (because not all **data** is required).

Please see the example Sheet Format worksheet:

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdHQySzVLLVdTUzhQWnJKdGJnSW11eWc#gid=4

And, here is an example dataset, all Sheets for Gush Etzion, a municipality in Israel:

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdFB0TFQxOVk4ZkNKRFVQaFgwWHQ3d3c#gid=7

Note how, for Sheets, we create a "Data" worksheet will all data we have. This is done also to help with data validation - seeing common patterns in item codes over time, checking that an item code has the same name over time, and so on. We then generate, from this "Data" worksheet, specific worksheets for each period we have data on. It is these auto-generated sheets that are importing into the database.


Example Files
-------------

Please refer to our public drive folder for all data format and structures:

https://drive.google.com/#folders/0B4JzAmQXH28md2FHUUJvZXZvb0U

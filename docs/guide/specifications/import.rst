CSV file imports
================

Overview
--------

Open Budget can import most of its core datasets in bulk, and this is certainly an area we'd like to see the community help develop even further.

Importing datasets requires preparation. The data needs to be in a *file type* we support (CSV only at this stage), and follow our *file format* for the dataset being imported.

The following datasets can be imported in bulk:

* Budget Templates
* Budgets
* Actuals
* Entities
* Contexts

This section of the documentation deals with the file formats we specify for each importable dataset. For more information on the importing mechanisms, please see the "Import" page of the "Features" section of the guide.

Dependencies
------------

To create an importable file of the correct type, you'll need to use any spreadsheet app that can output as CSV in UTF-8 encoding. We work with Google Docs, which is a great choice for creating and collaborating on the files before importing.

Specifications
--------------

Common
~~~~~~

Basic Requirements
++++++++++++++++++

* a compliant CSV file that is UTF-8 encoded
* data that matches the exact expected input for the dataset you want to import
* one single datapoint per cell - no overloading of cells for multiple data points

Header Requirements
+++++++++++++++++++

* The first row in any CSV file must be for "Headers", where the header describes the data in its column.
* Only one row can be a header - the importer does not support multiple header rows.
* There are specific "strings", or, "keywords" that each dataset expects to find as headers. Unknown headers mean that data cannot be imported.
* Alias keywords can be created via the admin to map to out required header keywords. This can help if, for example, non-english data source providers prefer headers in a different language - see the features/import page for more information on this feature.

Data Requirements
+++++++++++++++++

The importer does a range of validations on data to be imported, but there are always corner cases or use cases we perhaps did not predict. To make things easier, check the following in your source file before trying to import:

* Each column in your file is a valid data column for the dataset you are trying to import
* Where columns are required for import (for example, "code" for budget templates), the import will be prevented if an item is missing a required value - check and double-check that your dataset is complete

Budget Template
~~~~~~~~~~~~~~~

When importing a budget template, every row in the file must be a distinct Budget Template Node.

In addition, you'll fill out some form fields on import that provide us with other required metadata for the dataset: Name of the template, what entities it applies to, and the period of time for which it is valid.

All headers are required, even if some columns may be completely empty (because not all **data** is required).

The headers, and their data requirements, are:

* Name:          REQUIRED, string
* Code:          REQUIRED, string
* Parent:        NOTREQUIRED, string that must match another items Code
* Parent Scope:  NOTREQUIRED, pipe-separated strings, from left to right, parent's parent to top of tree
* Direction      REQUIRED: "EXPENDITURE" or "REVENUE"
* Inverse:       NOTREQUIRED, string that must match another items Code, inverse must have opposite direct to the item
* Inverse Scope: NOTREQUIRED, pipe-separated strings, from left to right, parent's parent to top of tree
* Description:   NOTREQUIRED, string

The following values are **the bare minimum requirement** for each item:

* Name
* Code
* Direction

The "Description" field is purely optional, dependent on whether your budget template has descriptions for each node in the template.

The additional fields in the file are for cases where the template is tree-like (Some nodes are parents/children of other nodes), and where some nodes have explicit inverse relations (a given node or group of nodes on one side, say EXPENDITURE, is directly related to a node or group on the other, REVENUE).

Parent/Child relations then raises a new issue - because some Budget Templates do not adhere to a system where the "code" for a given node is truly unique in the whole template, there are cases where we need a "disambiguation key" to know which parent a child relates to. Hence, we have a "scope" field that puts potentially conflicting nodes in context. "Parent Scope" and "Inverse Scope".

So:

If your template structure has conflicting codes (eg: two codes called "202", but they are in fact different, as they are under different parents), the following additional fields are required:

* Parent

And lastly, if a parent or an inverse is a conflicting code, the following fields are required:

* Parent Scope

or

* Inverse Scope

Budget/Actual
~~~~~~~~~~~~~

For all intents and purposes, the file format for Budgets and Actuals are the same, and we will now refer to importing a "Sheet" to refer to both, and "Sheet Items" to refer to the actual items in a budget or actual.

As with importing a Budget Template, you'll fill out some form fields on import that provide us with other required metadata for the dataset: Name of the entity the budget is for, period of the budget, a description text for the budget, and so on.

All headers are required, even if some columns may be completely empty (because not all **data** is required).

The headers, and their data requirements, are:

* Code:          REQUIRED, string
* Code Scope:          NOTREQUIRED, string
* Amount:        REQUIRED, number
* Description:  NOTREQUIRED, string
* Custom Code: NOTREQUIRED, TRUE OR FALSE
* Direction      REQUIRED WITH CUSTOM CODE TRUE: "EXPENDITURE" or "REVENUE"
* Parent:        NOTREQUIRED, string that must match another items Code
* Parent Scope:  NOTREQUIRED, pipe-separated strings, from left to right, parent's parent to top of tree
* Inverse:       NOTREQUIRED, string that must match another items Code, inverse must have opposite direct to the item
* Inverse Alias: NOTREQUIRED, pipe-separated strings, from left to right, parent's parent to top of tree

The following values are **the bare minimum requirement** for each item:

* Code
* Amount

The "Description" field is purely optional, dependent on whether your budget items have descriptions.

Other fields depend on the CUSTOM CODE field. If this is FALSE or blank, the other fields are completely ignored.

If this is TRUE, then the other fields are required according to all the logic of the Template importer rules for these fields.

Files
-----

We have files hosted on google docs for ease of viewing and use. If you want to use one of these files as a starting point for your own file, please ensure that in the end, to import, you download as CSV.

**CSV is the only import format we support at present**

Budget Template: Blank
++++++++++++++++++++++

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdGllRS1EWFB2aFF3Qk5DbHgyakE4Q0E#gid=4

Budget Template: Israeli Muni 1994 to Now
+++++++++++++++++++++++++++++++++++++++++

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdC12X3FrWi13VjU4bnh4dnZJekNTQXc#gid=4

Budget Template: Unit Test File
+++++++++++++++++++++++++++++++

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdC0xLXNDQnd4OVN0elIzMW5SYXNkSnc#gid=5

Budget/Actual: Blank
++++++++++++++++++++

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdHQySzVLLVdTUzhQWnJKdGJnSW11eWc#gid=4

Budget/Actual: Israel Muni Mock
+++++++++++++++++++++++++++++++

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdG44Xzd0NDB3UERvT2gtY2UyUWQxd3c#gid=4

Budget/Actual: Unit Test File
+++++++++++++++++++++++++++++++

https://docs.google.com/spreadsheet/ccc?key=0AoJzAmQXH28mdFFuc0MybjV0cnptT1R3TURrMjlIT0E#gid=4

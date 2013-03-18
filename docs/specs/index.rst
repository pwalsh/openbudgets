CSV file imports
================

There are some common rules and considerations for importing data via CSV files. We'll discuss these first.

Headers
-------

The importer expects headers in a certain format

- support for aliases via String in admin

- ignore_unknown_headers - support for ignore unknown headers, where header that do not find a mapping to the model being imported can simly be ignored, instead of cuasing an import to fail.

- ignore_invalid_rows - if set to True, will just skip over invalid rows and import other rows. This will still check validaity of relations, so, if something else realtes to an invalid row, the imort will still fail.

- after import, you'll get a response that shows the rows of data that were skipped.

- importer checks the whole dataset is valid, according to the business logic, before hitting the database.

Data
----

TODO

Budget Template import files
============================

The following headers are required:

Name | Code | Parent | Direction | Inverse | Description

* Name and code must be unique together across the table.

* Values are required for name, code, and direction

TODO

Budget and Actual import files
==============================

TODO

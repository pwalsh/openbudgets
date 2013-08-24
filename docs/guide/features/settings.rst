Settings
========

Overview
--------

Open Budgets has some global settings of its own to configure an Open Budgets instance.

General
-------

TEMP_FILES_DIR
~~~~~~~~~~~~~~
A place to write and read temporary files.

Accounts
--------

OPENBUDGET_CORE_TEAM_ID
~~~~~~~~~~~~~~~~~~~~~~~
The group ID for core team accounts. These users have permission to do anything.

OPENBUDGET_CONTENT_TEAM_ID
~~~~~~~~~~~~~~~~~~~~~~~~~~
The group ID for content team accounts. These users have permission to do access the admin and add/edit data.

OPENBUDGET_PUBLIC_ID
~~~~~~~~~~~~~~~~~~~~
The group ID for public accounts. These users have forward facing permissions, but no admin access.

Budgets
-------

OPENBUDGET_PERIOD_RANGES
~~~~~~~~~~~~~~~~~~~~~~~~
Supported budget ranges for this instance. Used in various places to specify date selection forms and several methods to extract budget periods.

options - ('monthly', 'quarterly', 'half-yearly', 'yearly', 'bi-yearly')

Can support none or many.


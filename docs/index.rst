Introduction
============

.. image:: https://travis-ci.org/prjts/openbudgets.png
   :alt: Build Status
   :target: https://travis-ci.org/prjts/openbudgets


.. image:: https://coveralls.io/repos/prjts/openbudgets/badge.png?branch=develop
   :alt: Coverage Status
   :target: https://coveralls.io/r/prjts/openbudgets?branch=develop


Open Budgets is a web app and web API for the storage, access, visualization of budgetary data.

In particular, Open Budgets has been designed ground up to allow for and promote the comparison of such data *over time*, and *across budgeting entities*.

Open Budgets is written in Python and Javascript, and is open source software released under a BSD license.

The code was initially written for the "Open Municipalities" umbrella project at the `Public Knowledge Workshop ("HaSadna")`_.


Design goals
============

Some important high-level design goals have influenced how we approach Open Budgets.

* Standardized API and formats for budget-related data
* Comparative analysis across related budgeting entities
* Full multilingual support across all data
* Discussion and user interaction build into the core data model


Current status
==============

Open Budgets is currently under development by a small team of volunteers.

Until now, the project has centered around the opening of local government data in Israel.

This is an ongoing initiative and influences the development priorities of this project.

In parallel, we are working on tidying up the system for wider use, including preparing other example datasets.


Get involved
============

You can contribute to the project with content, code, and ideas!

Start at one of the following channels:

`Roadmap`_: This is the best place to get an idea of what is going on right now.

`Discussion`_: A mailing list for project announcements and discussion.

`Documentation`_: An overview of the features that are currently in place.

`Issues`_: See the development tasks in the pipeline, or file a bug.

`Code`_: Go here if you love Python and JavaScript and want to dive into the code.

`Translation`_: i18n is a 1st class citizen here.

`Sandbox`_: The sandbox installation is currently offline. We hope to change that soon.


Table of contents
=================

.. toctree::
   :maxdepth: 3

   guide/quickstart
   guide/tutorial
   guide/features
   guide/api
   guide/ui
   guide/conventions
   guide/specifications


Indices and tables
==================

* :ref:`modindex`
* :ref:`search`


.. _`Public Knowledge Workshop ("HaSadna")`: http://www.hasadna.org.il/en/
.. _`Roadmap`: https://trello.com/b/bNnpPi70/open-budgets-roadmap
.. _`Discussion`: openbudgets@librelist.com
.. _`Documentation`: http://docs.openbudgets.io/
.. _`Issues`: https://github.com/openbudgets/openbudgets/issues
.. _`Code`: https://github.com/openbudgets/openbudgets
.. _`Translation`: https://www.transifex.com/projects/p/openbudgets/
.. _`Sandbox`: http://sandbox.openbudgets.io/

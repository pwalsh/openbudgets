Internationalization
====================

Overview
--------

.. image:: https://www.transifex.com/projects/p/open-budgets/resource/app-strings/chart/image_png
   :alt: Translation Status
   :target: https://www.transifex.com/projects/p/open-budgets

Open Budgets has advanced support for internationalization and localization in both the codebase and the database.

By default, Open Budgets ships with support for English, Hebrew, Arabic and Russian. This provides a starting point for multilingual instances that feature both LTR and RTL languages. Customization of supported languages is done via the project's settings files.

Configuration
-------------
All configuration of Open Budgets internationalization support is done via the project settings:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/settings/base.py

Customizing the default supported languages is easy, but it really should be done before any data is entered into the system, as these settings directly determine how modeltranslation will work on the database.

Language Settings
~~~~~~~~~~~~~~~~~

To customize language support for a new Open Budgets instance, you'll want to go to the LANGUAGES tuple in the base settings file.

*The first language in the tuple is always the default language of the instance*.

The default settings look something like this::

    # openbudget.settings.base.py

    gettext = lambda s: s
    LANGUAGES = (
        ('en', gettext('English')),
        ('he', gettext('Hebrew')),
        ('ar', gettext('Arabic')),
        ('ru', gettext('Russian')),
    )
    LANGUAGE_CODE = LANGUAGES[0][0]

Domain Settings
~~~~~~~~~~~~~~~

Each supported language must be mapped to one or more subdomains. We use subdomains for two reasons:

1. It is optimal for search indexing, and the preferred method for delivering multilingual content as per the Google Webmaster Guidelines.

2. If future use patterns require (scalability, etc.), it can be easier to separate language and API support across different instances of Open Budgets.

The default settings for subdomains look something like this::

    # openbudget.settings.base.py

    SUBDOMAIN_URLCONFS = {
        '': 'openbudget.ui.urls',
        'www': 'openbudget.ui.urls',
        'en': 'openbudget.ui.urls',
        'he': 'openbudget.ui.urls',
        'ar': 'openbudget.ui.urls',
        'ru': 'openbudget.ui.urls',
        'api': 'openbudget.api.urls',
    }

By itself, this configuration doesn't actually set a language for any of those subdomains. That is done in the InterfaceLanguage middleware:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py

Notes
~~~~~
* In the current implementation, an authenticated user's language setting, accessed by user.get_profile().language will always take precedence over any language/subdomain mapping
* The server (including the development server!) must be able to serve on these subdomains. The quickstart explains how to configure your machine for this.

Dependencies
------------

Open Budgets' internationalization features depend on a number of 3rd party python packages.

* django
* subdomains

Django
~~~~~~

https://github.com/django/django

Open Budgets sits on the Django web framework and uses its built in features for internationalization and localization. Please refer to the relevant Django documentation if you are not familiar with Django:

https://docs.djangoproject.com/en/1.5/topics/i18n/

How to import::

    from django.utils.translation import ugettext_lazy

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py

SubDomains
~~~~~~~~~~

https://github.com/tkaemming/django-subdomains

We use SubDomains to support multiple subdomains in a single Open Budgets instance, where, each supported language has a mapping to at least one subdomain.

How to import::

    from subdomains.utils import get_domain

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py

Project Code
------------

International App
~~~~~~~~~~~~~~~~~

International is our custom app to centralize our internationalization code.

How to import::

    from openbudget.apps.international.utilities import get_language_key

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py

International Middleware
++++++++++++++++++++++++

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py

LanguageInterface
*****************

The LanguageInterface middleware sets the language for a given request.

* If the user is authenticated, it gets the user's preferred language and uses it
* Otherwise, it returns the language that is mapped to the subdomain of the requesting host

Templates
*********

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/apps/international/templates/international/partials

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/templatetags/international.py

language_switch
+++++++++++++++

The language_switch templatetag outputs a small snippet of HTML with links to alternate language versions of the currently viewed page.


multilingual_meta
+++++++++++++++++

The multilingual_meta templatetag is used in the base template of the app, providing language meta tags according to Google Webmaster guidelines for related links to the same content in different languages.

More information about the guidelines can be found here_.

.. _here: http://googlewebmastercentral.blogspot.co.il/2011/12/new-markup-for-multilingual-content.html

Other
*****

There are a few other areas in the project that have language-related code.

Base Template
+++++++++++++

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/commons/templates/base.html

The base template is inherited by all other app templates. It uses the LANGUAGE_CODE variable to set the current document language as per HTML specifications, and the LANGUAGE_BIDI variable to determine whether the RTL or LTR stylesheet should be loaded.

Stylesheets
+++++++++++

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/commons/static/css

For a more complete description of our stylesheets, see the interface/ui section of the guide.

As for the relation to language:

All our CSS is written in LESS, and sits on top of a modular toolkit for LESS called Adaptabl. Adaptabl provides a bunch of helper mixins, media queries, and BIDI support in the core. So, our stylesheets are support LTR and RTL out of the box.

Internationalization
====================

Open Budget has advanced support for internationalization and localization.

The main repository for Open Budget currently ships with support for English, Hebrew, Arabic and Russian, providing a starting point for multilingual instances that will support both RTL and LTR languages.

Settings
--------

Customization of supported languages is a trivial task, performed on setup of a new Open Budget instance. It *should* be done before any data is entered into the system, as these settings directly determine how modeltranslation will work on the database.

All internationalization and localization setup is done via the project settings package, preferably in the base settings, which are inherited by other settings files, such as settings.local:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/settings/base.py

**Customization**

*Languages*

When configuring a new instance of Open Budget, you'll first want to customize the languages your instance will support. This is done via the LANGUAGES tuple.

The first language in the LANGUAGES tuple is always the default language. It is possible to just have a single language in the LANGUAGES tuple.

By default, the LANGUAGES tuple (and other constants that depend on it) looks like this::

    # openbudget.settings.base.py

    # LANGUAGE CONF
    gettext = lambda s: s
    LANGUAGES = (
        ('en', gettext('English')),
        ('he', gettext('Hebrew')),
        ('ar', gettext('Arabic')),
        ('ru', gettext('Russian')),
    )
    LANGUAGE_CODE = LANGUAGES[0][0]
    MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE

*Domains*

It is also required to map a language to a subdomain or multiple sobdomains. We use subdomains for two reasons:

1. It is optimal for search indexing, and the preferred method for delivering multlilingual content as per the Google Webmaster Guidelines.

2. If future use patterns require (scalability etc.), it can be easier to separate language support across different applications.

By default, subdomains are configured something like this::

    # openbudget.settings.base.py

    # SUBDOMAIN CONF
    SUBDOMAIN_URLCONFS = {
        '': 'openbudget.ui.urls',
        'www': 'openbudget.ui.urls',
        'he': 'openbudget.ui.urls',
        'en': 'openbudget.ui.urls',
        'ru': 'openbudget.ui.urls',
        'ar': 'openbudget.ui.urls',
        'api': 'openbudget.api.urls',
    }

This subdomain configuration is then used in our InterfaceLanguage middleware, which maps requesting hosts to supported languages::

    # openbudget.apps.international.middleware.py

    from openbudget.apps.international.utilities import get_language_key

    class InterfaceLanguage(object):
        """Returns a LANGUAGE_CODE object for the request context"""
        def process_request(self, request):
            domain = get_domain()
            host = request.get_host()
            user = request.user
            lang = get_language_key(host, domain, user)
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()

    # openbudget.apps.international.utilities.py

    def get_language_key(host, domain, user):
        if not user.is_anonymous():
            value = user.get_profile().language
        else:
            current_subdomain = host[:-len(domain) - 1]
            default_language = settings.LANGUAGE_CODE
            valid_languages = [l[0] for l in settings.LANGUAGES]
            valid_subdomains = list(settings.SUBDOMAIN_URLCONFS)
            default_language_domains = []

            for d in valid_subdomains:
                if (d is default_language) or (d not in valid_languages):
                    default_language_domains.append(d)

            if current_subdomain in default_language_domains:
                value = default_language
            else:
                value = current_subdomain

        return value


**Note**: Notice that with the above code, the language setting of an authenticated user will override any other language setting logic, and thus such users will always see content in their language of choice (provided of course, that translations exist).

Code
----

The internationalization implementation is build using several 3rd party packages, and some custom code for this project.

Dependencies
~~~~~~~~~~~~

* django
* modeltranslation
* subdomains

Django
++++++

https://github.com/django/django

Of course, Django ships with many features for internationalization and localization, and all additional features in Open Budget ultimately sit on this base. Please refer to the relevant Django documentation if you are not familiar with Django:

https://docs.djangoproject.com/en/1.5/topics/i18n/

example import::

    from django.utils.translation import ugettext_lazy

code implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py


ModelTranslation
++++++++++++++++

https://github.com/deschler/django-modeltranslation

We use ModelTranslation for translatable data stored in the database.

example import::

    from modeltranslation.translator import translator

code implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/translation.py


SubDomains
++++++++++

https://github.com/tkaemming/django-subdomains

We use SubDomains so we can explicitly set language contexts based on the requesting subdomain.

example import::

    from subdomains.utils import get_domain

code implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py


Custom
~~~~~~

International
+++++++++++++

* openbudget.apps.international

International is our custom app to centralize our internationalization code.

**Middleware**

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/middleware.py

*Language Interface*

The LanguageInterface middleware sets the language for a given request.

* If the user is authenticated, it gets the user's prefered language, and uses that for the context language.
* Otherwise, it looks at the requesting domain, and, based on the settings of the Open Budget instance, returns the correct language for that domain.

**Templates**

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/apps/international/templates/international/partials

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/international/templatetags/international.py

We have template tags for internationalization, and some templates for use with the template tags.

*Language Switch*

The language_switch templatetag outputs a small snippet of HTML with links to the currently viewed page in different supported languages.

*Multilingual Meta*

The multilingual_meta templatetag is used in the base template of the app. It provides language meta tags according to Google Webmaster guidelines for related links to the same content in different languages. More information about the guidelines can be found here_.

.. _here: http://googlewebmastercentral.blogspot.co.il/2011/12/new-markup-for-multilingual-content.html

Other
+++++

There are a few other areas in the project that have language related code specifically.

**Base Template**

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/commons/templates/base.html

The base template is inherited by all other app templates. It uses LANGUAGE_CODE to set the current document language as per html specifications, and LANGUAGE_BIDI, to determine whether the RTL or LTR stylesheet should be loaded.

**Stylesheets**

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/commons/static/css

For more information on our stylesheets, see the interface/ui section of the guide.

The CSS for the app is completely direction aware (RTL and LTR).

Our CSS is actually written in LESS and compiled to CSS.

We are using a small, modular toolkit for LESS called Adaptabl, which provides a bunch of helper mixins, media queries, and BIDI support in the core.

The Adaptabl repository can be found here:

https://github.com/prjts/adaptabl

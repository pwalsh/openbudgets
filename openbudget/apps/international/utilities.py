from openbudget.settings import base as settings


def get_language_key(host, domain, user):
    """Invoked in middleware to customize request.LANGUAGE_CODE

    A language key is returned according to the following logic:

    * If user is authenticated, set language to the user's language preference, no matter what the domain.
    * If user is anonymous, get the language key from the domain (we are using django-subdomains for language
        specific domains)
    * If the domain doesn't have an explicit language key we return the default language.
    """
    # Get lang from authenticated user
    if not user.is_anonymous():
        value = user.language

    # Get lang based on request host and global language settings
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


def translated_fields(*args, **kwargs):
    """Given field names, returns a list of related translated field names.

    TODO: use the translation registry files to *ensure* that the passed field
     is actually registered for translation, using model=None kwarg.
    """

    target_codes = [lang[0] for lang in settings.LANGUAGES]
    target_codes.remove(settings.MODELTRANSLATION_DEFAULT_LANGUAGE)

    value = []
    for field in args:
        value.extend([field + '_' + code for code in target_codes])

    return value

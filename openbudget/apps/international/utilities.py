from modeltranslation.translator import translator
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


def translated_fields(model):
    """Given a model, returns a list of translated field names for it.

    The returned list excludes the extra field created for the default language.

    """

    options = translator.get_options_for_model(model)
    fields = [f.name for l in options.fields.values() for f in l]

    for i, f in enumerate(fields):
        if f.endswith(settings.MODELTRANSLATION_DEFAULT_LANGUAGE):
            del fields[i]

    return fields

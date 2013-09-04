"""International templatetags.

Requires:
* django-subdomains - this can easily be removed by directly querying the Sites table.
"""
from django.conf import settings
from django.template import Library
from subdomains.utils import get_domain


register = Library()


@register.inclusion_tag('international/partials/_language_switch.html')
def language_switch(full_path):
    """returns a language switching widget"""
    domain = get_domain()

    data = []
    for l in settings.LANGUAGES:
        tmp = {}
        tmp['key'] = l[0]
        tmp['url'] = 'http://' + l[0] + '.' + domain + full_path
        data.append(tmp)

    value = {'languages': data}

    return value


@register.inclusion_tag('international/partials/_multilingual_meta.html')
def multilingual_meta(full_path):
    """Returns a list of multilingual metatags according to Google Webmaster guidelines"""
    domain = get_domain()

    data = []
    for l in settings.LANGUAGES:
        tmp = {}
        tmp['key'] = l[0]
        tmp['url'] = 'http://' + l[0] + '.' + domain + full_path
        data.append(tmp)

    value = {'languages': data}

    return value

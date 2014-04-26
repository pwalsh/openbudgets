"""International middleware.

Requires:
* django-subdomains - this dependency can be removed by directly querying Sites.

"""


from django.utils import translation
from subdomains.utils import get_domain
from openbudgets.apps.international.utilities import get_language_key


class InterfaceLanguage(object):

    """Returns a LANGUAGE_CODE object for the request context"""

    def process_request(self, request):
        domain = get_domain()
        host = request.get_host()
        user = request.user
        lang = get_language_key(host, domain, user)
        translation.activate(lang)
        request.LANGUAGE_CODE = translation.get_language()

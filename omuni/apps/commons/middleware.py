"""Custom middleware for Omuni"""

from django.utils import translation


class InterfaceLanguage(object):
    """Returns a LANGUAGE_CODE object for the request context"""
    def process_request(self, request):
        # In future we might use host to determine language
        # e.g., en.omuni.org.il / he.omuni.org.il / ar.omuni.org.il

        # For now, we are just hardcoded to English
        translation.activate('en')

        request.LANGUAGE_CODE = translation.get_language()

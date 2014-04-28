from itertools import chain
from django.conf import settings
from django.conf.urls import url, include


def get_patterns():

    patterns = []

    with_api = settings.OPENBUDGETS_API['enable']
    with_ui = settings.OPENBUDGETS_UI['enable']
    with_admin = settings.OPENBUDGETS_ADMIN['enable']
    api_base = settings.OPENBUDGETS_API['base']
    api_base_without_ui = settings.OPENBUDGETS_API['base_without_ui']
    ui_base = settings.OPENBUDGETS_UI['base']
    admin_base = settings.OPENBUDGETS_ADMIN['base']

    def get_api(base=api_base):

        from openbudgets.api import urls

        patterns = [
            url(r'^{0}'.format(base), include(urls))
        ]

        return patterns

    def get_ui(base=ui_base):

        from openbudgets.ui import urls

        patterns = [
            url(r'^{0}'.format(base), include(urls))
        ]

        return patterns

    def get_admin(base=admin_base):

        from django.contrib import admin
        admin.autodiscover()

        patterns = [
            url(r'^{0}'.format(base), include(admin.site.urls)),
        ]

        return patterns

    if all([with_api, with_ui, with_admin]):
        patterns.extend(chain.from_iterable([get_admin(), get_api(), get_ui()]))

    elif all([with_api, with_ui]) and not with_admin:
        patterns.extend(chain.from_iterable([get_api(), get_ui()]))

    elif with_ui:
        patterns.extend(get_ui())
        if with_admin:
            patterns.extend(get_admin())

    elif with_api:
        patterns.extend(get_api(api_base_without_ui))
        if with_admin:
            patterns.extend(get_admin())

    elif with_admin:
        patterns.extend(get_admin())

    return patterns


urlpatterns = get_patterns()

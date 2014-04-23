from django.conf.urls import url, include
from django.views.generic import TemplateView
from openbudgets.commons.views import OBudgetSitemap


sitemaps = {'site': OBudgetSitemap}


urlpatterns = [

    url(r'^accounts/',
        include('openbudgets.apps.accounts.urls.ui')),

    url(r'^entities/',
        include('openbudgets.apps.entities.urls.ui')),

    url(r'^sheets/',
        include('openbudgets.apps.sheets.urls.ui')),

    url(r'^tools/',
        include('openbudgets.apps.tools.urls.ui'),),

    url(r'^transport/',
        include('openbudgets.apps.transport.urls')),

    url(r'^robots\.txt',
        TemplateView.as_view(template_name='robots.txt')),

    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    url(r'^',
        include('openbudgets.apps.pages.urls')),

    # TODO: this feature is not in use currently
    # url(r'^interactions/',
    #     include('openbudgets.apps.interactions.urls')),


    # TODO: this feature is not in use currently
    # url(r'^taxonomies/',
    #     include('openbudgets.apps.taxonomies.urls')),



    # TODO: this feature is not in use currently
    # url(r'^sources/',
    #     include('openbudgets.apps.sources.urls')),

]

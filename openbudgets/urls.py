from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from openbudgets.commons.views import OBudgetSitemap, OBudgetSearchView
admin.autodiscover()


sitemaps = {
    'site': OBudgetSitemap,
}


urlpatterns = patterns('',

    url(r'^admin/',
        include(admin.site.urls)),

    url(r'^accounts/',
        include('openbudgets.apps.accounts.urls.ui')),

    url(r'^api/',
        include('openbudgets.apps.api.urls')),

    url(r'^entities/',
        include('openbudgets.apps.entities.urls.ui')),

    url(r'^sheets/',
        include('openbudgets.apps.sheets.urls.ui')),

    url(r'^interactions/',
        include('openbudgets.apps.interactions.urls')),

    url(r'^tools/',
        include('openbudgets.apps.tools.urls.ui'),),

    url(r'^taxonomies/',
        include('openbudgets.apps.taxonomies.urls')),

    url(r'^transport/',
        include('openbudgets.apps.transport.urls')),

    url(r'^sources/',
        include('openbudgets.apps.sources.urls')),

    url(r'^search/',
        OBudgetSearchView(), name='search'),

    url(r'^comments/',
        include('django.contrib.comments.urls')),

    url(r'^robots\.txt',
        TemplateView.as_view(template_name='robots.txt')),

    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    url(r'^grappelli/',
        include('grappelli.urls')),

    url(r'^',
        include('openbudgets.apps.pages.urls')),

)

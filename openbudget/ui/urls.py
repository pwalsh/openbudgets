from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from openbudget.commons.views import OBudgetSitemap, OBudgetSearchView
admin.autodiscover()


sitemaps = {
    'site': OBudgetSitemap,
}


urlpatterns = patterns('',
    url(r'^admin/',
        include(admin.site.urls)
    ),
    url(r'^accounts/',
        include('openbudget.apps.accounts.urls')
    ),
    url(r'^entities/',
        include('openbudget.apps.entities.urls')
    ),
    url(r'^budgets/',
        include('openbudget.apps.budgets.urls')
    ),
    url(r'^interactions/',
        include('openbudget.apps.interactions.urls')
    ),
    url(r'^taxonomies/',
        include('openbudget.apps.taxonomies.urls')
    ),
    url(r'^transport/',
        include('openbudget.apps.transport.urls')
    ),
    url(r'^sources/',
        include('openbudget.apps.sources.urls')
    ),
    url(r'^search/',
        OBudgetSearchView(),
        name='search'
    ),
    url(r'^comments/',
        include('django.contrib.comments.urls')
    ),
    url(r'^robots\.txt',
        TemplateView.as_view(template_name='robots.txt')
    ),
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),
    url(r'^grappelli/',
        include('grappelli.urls')
    ),
    url(r'^rosetta/',
        include('rosetta.urls')
    ),
    url(r'^',
        include('openbudget.apps.pages.urls')
    ),
)

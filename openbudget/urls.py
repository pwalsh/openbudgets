from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from openbudget.commons.views import OmuniSitemap
admin.autodiscover()


sitemaps = {
    'site': OmuniSitemap,
}

urlpatterns = patterns('',

    url(r'^admin/',
        include(admin.site.urls)
    ),
    url(r'^accounts/',
        include('openbudget.accounts.urls')
    ),
    url(r'^budgets/',
        include('openbudget.budgets.urls')
    ),
    url(r'^govts/',
        include('openbudget.govts.urls')
    ),
    url(r'^interactions/',
        include('openbudget.interactions.urls')
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
        include('openbudget.pages.urls')
    ),

)

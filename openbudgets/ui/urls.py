from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap as sitemap_view
from openbudgets.apps.accounts.urls import ui as account_urls
from openbudgets.apps.entities.urls import ui as entity_urls
from openbudgets.apps.sheets.urls import ui as sheet_urls
from openbudgets.apps.tools.urls import ui as tool_urls
from openbudgets.apps.transport import urls as transport_urls
from openbudgets.apps.pages import urls as page_urls
from openbudgets.commons.views import OBudgetSitemap


sitemaps = {'site': OBudgetSitemap}


urlpatterns = [

    url(r'^accounts/', include(account_urls)),

    url(r'^entities/', include(entity_urls)),

    url(r'^sheets/', include(sheet_urls)),

    url(r'^tools/', include(tool_urls),),

    url(r'^transport/', include(transport_urls)),

    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt')),

    url(r'^sitemap\.xml$', sitemap_view, {'sitemaps': sitemaps}),

    url(r'^', include(page_urls)),

    # TODO: this feature is not in use currently
    # url(r'^interactions/', include(interaction_urls)),

    # TODO: this feature is not in use currently
    # url(r'^taxonomies/', include(taxonomy_urls)),

    # TODO: this feature is not in use currently
    # url(r'^sources/', include(source_urls)),

]

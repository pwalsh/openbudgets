from itertools import chain
from django.contrib.sitemaps import Sitemap
from openbudgets.apps.pages.models import Page


class OBudgetSitemap(Sitemap):
    """Returns an XML Sitemap for consumption by search engines and other crawlers"""

    changefreq = "never"
    priority = 0.5

    def items(self):
        pages = Page.objects.all()
        # Add more objects here based on what we want in the sitemap.xml, and chanin them in the items list below.

        items = list(chain(pages))
        return items

    def lastmod(self, obj):
        return obj.last_modified

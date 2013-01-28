"""Custom context processors for Omuni"""

from django.contrib.sites.models import Site


def get_site(request):
    """Returns a Site object for the global request context"""
    # If we will later map multiple hosts to the project
    #host = request.get_host()
    #site = Site.objects.get(domain=host)

    # But, for now
    site = Site.objects.get(pk=1)

    return {'site': site}

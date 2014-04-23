from django.conf.urls import include, url
from django.views.generic import TemplateView
from oauth2_provider import urls as auth_urls
from openbudgets.api.views import api_index
from openbudgets.api.v1 import urls as v1_urls


urlpatterns = [

    url(r'^$', api_index, name='api'),

    url(r'^auth/', include(auth_urls)),

    url(r'^v1/', include(v1_urls),),

    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt')),

]

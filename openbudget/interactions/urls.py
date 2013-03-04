from django.conf.urls import patterns, include, url
from openbudget.interactions.views import ICommentFeed, toggleable_interaction


urlpatterns = patterns('',

    url(r'^feed/(?P<model>[-\w]+)/(?P<uuid>[-\w]+)/discussion\.atom$',
        ICommentFeed(),
        name='comment_feed'
    ),
    url(r'^toggle/$',
        toggleable_interaction,
        name='toggleable_interaction'
    ),

)

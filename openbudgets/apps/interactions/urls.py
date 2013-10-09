from django.conf.urls import patterns, include, url
from openbudgets.apps.interactions.views import CommentFeed, toggleable_interaction


urlpatterns = patterns('',

    url(r'^feed/(?P<model>[-\w]+)/(?P<uuid>[-\w]+)/discussion\.atom$',
        CommentFeed(), name='comment_feed'),

    url(r'^toggle/$',
        toggleable_interaction, name='toggleable_interaction'),

)

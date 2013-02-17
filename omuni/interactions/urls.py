from django.conf.urls import patterns, include, url
from omuni.interactions.views import CommentFeed


urlpatterns = patterns('',

    url(r'^feed/(?P<model>[-\w]+)/(?P<uuid>[-\w]+)/discussion\.atom$',
            CommentFeed(),
            name='comment_feed'
        ),

)

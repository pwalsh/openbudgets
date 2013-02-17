from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.forms import CommentForm
from omuni.interactions.models import IComment


class ICommentForm(CommentForm):
    #title = forms.CharField(max_length=300)

    def get_comment_model(self):
        return IComment

    def get_comment_create_data(self):
        data = super(ICommentForm, self).get_comment_create_data()
        # TODO: Gotta automagically know what type it should be
        # and set accordingly
        data['of_type'] = 'post'
        return data

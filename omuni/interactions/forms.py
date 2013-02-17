from django import forms
from django.contrib.comments.forms import CommentForm
from omuni.interactions.models import Remark


class RemarkForm(CommentForm):
    #title = forms.CharField(max_length=300)

    def get_comment_model(self):
        return Remark

    def get_comment_create_data(self):
        data = super(RemarkForm, self).get_comment_create_data()
        #data['title'] = self.cleaned_data['title']
        return data

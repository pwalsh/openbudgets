from modeltranslation.translator import translator, TranslationOptions
from openbudget.interactions.models import Comment


class CommentTransOps(TranslationOptions):
    fields = ('comment',)


translator.register(Comment, CommentTransOps)

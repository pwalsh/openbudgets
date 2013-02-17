from modeltranslation.translator import translator, TranslationOptions
from omuni.interactions.models import Comment


class CommentTransOps(TranslationOptions):
    fields = ('comment',)


translator.register(Comment, CommentTransOps)

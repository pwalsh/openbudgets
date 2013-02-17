from modeltranslation.translator import translator, TranslationOptions
from omuni.interactions.models import Remark


class RemarkTransOps(TranslationOptions):
    fields = ('comment',)


translator.register(Remark, RemarkTransOps)

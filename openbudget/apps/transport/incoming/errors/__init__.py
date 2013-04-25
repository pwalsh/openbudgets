from django.utils.translation import ugettext_lazy as _


class DataAmbiguityError(object):

    def __init__(self, rows=None):
        self.rows = rows or ('Unknown', 'Unknown')

    def __unicode__(self):
        return _('Data Ambiguity Error')

    @property
    def message(self):
        return _('Source contains siblings with same code in rows: %s, %s') % self.rows

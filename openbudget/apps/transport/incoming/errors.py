from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _


class DataSyntaxError(object):

    def __init__(self, row='Unknown', columns=None, values=None):
        self.row = row
        self.columns = columns or ('Unknown',)
        self.values = values or ('Unknown',)

    def __unicode__(self):
        return _('Data Syntax Error')

    @property
    def message(self):
        return _('Syntax error found in row: %s; and columns: %s; with values: %s') %\
               (self.row, ', '.join(self.columns), ', '.join(self.values))


class DataAmbiguityError(object):

    def __init__(self, rows=None):
        self.rows = rows or ('Unknown', 'Unknown')

    def __unicode__(self):
        return _('Data Ambiguity Error')

    @property
    def message(self):
        return _('Source contains siblings with same code in rows: %s, %s') % self.rows


class MetaParsingError(object):

    def __init__(self, reason='Unknown'):
        self.reason = reason

    def __unicode__(self):
        return _('Meta Parsing Error')

    @property
    def message(self):
        return _('Source meta data invalid for reason: %s') % self.reason


class DataValidationError(object):

    def __init__(self, reasons=None, row='Unknown'):
        self.reasons = reasons
        self.row = row

    def __unicode__(self):
        return _('Data Validation Error')

    @property
    def message(self):
        reasons = 'Unknown'

        if self.reasons:
            reasons = []
            for key, message in self.reasons.iteritems():
                if key == NON_FIELD_ERRORS:
                    key = 'others'

                reasons.append('%s: %s' % (key, message))

        return _('Source data invalid in row: %s; for reasons: %s') % (self.row, ' AND '.join(reasons))


class NodeDirectionError(object):

    def __init__(self, rows=None):
        self.rows = rows or ('Unknown', 'Unknown')

    def __unicode__(self):
        return _('Node Direction Error')

    @property
    def message(self):
        return _("Inverse node's direction is not opposite of item in row: %s; and inverse in row: %s") % self.rows


class ParentScopeError(object):

    def __init__(self, row='Unknown'):
        self.row = row

    def __unicode__(self):
        return _('Parent Scope Error')

    @property
    def message(self):
        return _("Parent scope is missing or not resolvable in row: %s") % self.row

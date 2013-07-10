from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _


class DataInputError(object):

    def __init__(self, row=None, columns=None, values=None):
        if row is None:
            row = 'Unknown'
        self.row = row
        self.columns = columns or ['Unknown']
        self.values = values or ['Unknown']

    def to_json(self):
        return {
            'row': self.row,
            'columns': self.columns,
            'values': self.values,
            'message': self.message
        }

    @property
    def _message(self):
        return _('Error found in row: {row}; and columns: {columns}; '
                 'with values: {values}')

    @property
    def message(self):
        return self._message.format(row=self.row,
                                    columns=', '.join(self.columns),
                                    values=', '.join(self.values))


class DataCollisionError(object):

    def __init__(self, rows=None, columns=None, values=None):
        self.rows = rows or ['Unknown', 'Unknown']
        self.columns = columns or ['Unknown']
        self.values = values or ['Unknown']

    def to_json(self):
        return {
            'rows': self.rows,
            'columns': self.columns,
            'values': self.values,
            'message': self.message
        }

    @property
    def _message(self):
        return _('Source data collision error in rows: {first_row}, '
                 '{second_row}; and columns: {columns}; with values: {values}')

    @property
    def message(self):
        return self._message.format(first_row=self.rows[0],
                                    second_row=self.rows[1],
                                    columns=self.columns, values=self.values)


class DataSyntaxError(DataInputError):

    def __unicode__(self):
        return _('Data Syntax Error')

    @property
    def _message(self):
        return _('Syntax error found in row: {row}; and columns: {columns}; '
                 'with values: {values}')


class DataAmbiguityError(DataCollisionError):

    def __unicode__(self):
        return _('Data Ambiguity Error')

    @property
    def _message(self):
        return _('Source contains siblings with same code in rows: {first_row},'
                 ' {second_row}; and columns: {columns}; with values: {values}')


class MetaParsingError(object):

    def __init__(self, reason='Unknown'):
        self.reason = reason

    def to_json(self):
        return {
            'reason': self.reason,
            'message': self.message
        }

    def __unicode__(self):
        return _('Meta Parsing Error')

    @property
    def message(self):
        return _('Source meta data invalid for reason: {reason}').format(
            reason=self.reason)


class DataValidationError(DataInputError):

    def __init__(self, reasons=None, row='Unknown'):
        super(DataValidationError, self).__init__(row=row)
        self.reasons = reasons

    def to_json(self):
        error_dic = super(DataValidationError, self).to_json()
        error_dic['reasons'] = self.reasons
        return error_dic

    def __unicode__(self):
        return _('Data Validation Error')

    @property
    def message(self):
        reasons = 'Unknown'

        if self.reasons:
            reasons = []
            for key, messages in self.reasons.iteritems():
                if key == NON_FIELD_ERRORS:
                    key = 'others'

                reasons.append('{key}: {messages}'.format(
                    key=key,
                    messages='and '.join(messages)))

            reasons = ' AND '.join(reasons)

        return _('Source data invalid in row: {row}; '
                 'for reasons: {reasons}').format(row=self.row, reasons=reasons)


class NodeDirectionError(DataCollisionError):

    def __unicode__(self):
        return _('Node Direction Error')

    @property
    def _message(self):
        return _("Inverse node's direction is not opposite of item in row: "
                 "{row}; and inverse in row: {row}")


class ParentScopeError(DataInputError):

    def __unicode__(self):
        return _('Parent Scope Error')

    @property
    def _message(self):
        return _("Parent scope is missing or not resolvable in row: {row}")

    @property
    def message(self):
        return self._message.format(row=self.row)


class NodeNotFoundError(DataInputError):

    @property
    def _message(self):
        return _('Budget template node not found for item in'
                 ' row: {row}; and columns: {columns}; with values: {values}')


class ParentNodeNotFoundError(DataInputError):

    @property
    def _message(self):
        return _('Parent node not found for item in '
                 'row: {row}; and columns: {columns}; with values: {values}')


class PathInterpolationError(DataInputError):

    def __unicode__(self):
        return _('Nodes Path Interpolation Error')

    @property
    def _message(self):
        return _('Interpolation failed, no ancestor found for row: {row}')


class InverseScopesError(DataInputError):

    def __unicode__(self):
        return _('Inverse Scopes Error')

    @property
    def _message(self):
        return _('Inverse scopes not matching inverses in'
                 ' row: {row}; and columns: {columns}; with values: {values}')


class InverseNodeNotFoundError(DataInputError):

    @property
    def _message(self):
        return _('Inverse node not found for item in'
                 ' row: {row}; and columns: {columns}; with values: {values}')

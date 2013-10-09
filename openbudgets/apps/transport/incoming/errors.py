import json
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _


UNKNOWN = u'Unknown'


class ErrorMessage(object):

    def get_arguments(self):
        # a dictionary for formatting the _message.
        raise NotImplementedError

    def to_json(self):
        value = json.dumps(self.get_arguments(), ensure_ascii=False)
        return value


class DataInputError(ErrorMessage):

    def __init__(self, row=None, columns=None, values=None):
        if row is None:
            row = UNKNOWN
        self.row = row
        self.columns = columns or [UNKNOWN]
        self.values = values or [UNKNOWN]

    def get_arguments(self):
        return {
            u'row': self.row,
            u'columns': self.columns,
            u'values': self.values,
            u'message': self.message
        }

    @property
    def _message(self):
        return _(u'Error found in row: {row}; and columns: {columns}; '
                 u'with values: {values}')

    @property
    def message(self):
        return self._message.format(row=self.row,
                                    columns=u', '.join(self.columns),
                                    values=u', '.join(self.values))


class DataCollisionError(ErrorMessage):

    def __init__(self, rows=None, columns=None, values=None):
        self.rows = rows or [UNKNOWN, UNKNOWN]
        self.columns = columns or [UNKNOWN]
        self.values = values or [UNKNOWN]

    def get_arguments(self):
        return {
            u'rows': self.rows,
            u'columns': self.columns,
            u'values': self.values,
            u'message': self.message
        }

    @property
    def _message(self):
        return _(u'Source data collision error in rows: {first_row}, '
                 u'{second_row}; and columns: {columns}; with values: {values}')

    @property
    def message(self):
        return self._message.format(first_row=self.rows[0],
                                    second_row=self.rows[1],
                                    columns=self.columns, values=self.values)


class DataSyntaxError(DataInputError):

    def __unicode__(self):
        return _(u'Data Syntax Error')

    @property
    def _message(self):
        return _(u'Syntax error found in row: {row}; and columns: {columns}; '
                 u'with values: {values}')


class DataAmbiguityError(DataCollisionError):

    def __unicode__(self):
        return _(u'Data Ambiguity Error')

    @property
    def _message(self):
        return _(u'Source contains siblings with same code in rows: {first_row},'
                 u' {second_row}; and columns: {columns}; with values: {values}')


class MetaParsingError(ErrorMessage):

    def __init__(self, reason=UNKNOWN):
        self.reason = reason

    def get_arguments(self):
        return {
            u'reason': self.reason,
            u'message': self.message
        }

    def __unicode__(self):
        return _(u'Meta Parsing Error')

    @property
    def message(self):
        return _(u'Source meta data invalid for reason: {reason}').format(
            reason=self.reason)


class DataValidationError(DataInputError):

    def __init__(self, reasons=None, row=UNKNOWN):
        super(DataValidationError, self).__init__(row=row)
        self.reasons = reasons

    def get_arguments(self):
        error_dic = super(DataValidationError, self).get_arguments()
        error_dic[u'reasons'] = self.reasons
        return error_dic

    def __unicode__(self):
        return _(u'Data Validation Error')

    @property
    def message(self):
        reasons = UNKNOWN

        if self.reasons:
            reasons = []
            for key, messages in self.reasons.iteritems():
                if key == NON_FIELD_ERRORS:
                    key = u'others'

                reasons.append(u'{key}: {messages}'.format(
                    key=key,
                    messages=u'and '.join(messages)))

            reasons = u' AND '.join(reasons)

        return _(u'Source data invalid in row: {row}; '
                 u'for reasons: {reasons}').format(row=self.row, reasons=reasons)


class NodeDirectionError(DataCollisionError):

    def __unicode__(self):
        return _(u'Node Direction Error')

    @property
    def _message(self):
        return _(u"Inverse node's direction is not opposite of item in row: "
                 u"{row}; and inverse in row: {row}")


class ParentScopeError(DataInputError):

    def __unicode__(self):
        return _(u'Parent Scope Error')

    @property
    def _message(self):
        return _(u'Parent scope is missing or not resolvable in row: {row}')

    @property
    def message(self):
        return self._message.format(row=self.row)


class NodeNotFoundError(DataInputError):

    @property
    def _message(self):
        return _(u'Budget template node not found for item in '
                 u'row: {row}; and columns: {columns}; with values: {values}')


class ParentNodeNotFoundError(DataInputError):

    @property
    def _message(self):
        return _(u'Parent node not found for item in '
                 u'row: {row}; and columns: {columns}; with values: {values}')


class PathInterpolationError(DataInputError):

    def __unicode__(self):
        return _(u'Nodes Path Interpolation Error')

    @property
    def _message(self):
        return _(u'Interpolation failed, no ancestor found for row: {row}')


class InverseScopesError(DataInputError):

    def __unicode__(self):
        return _(u'Inverse Scopes Error')

    @property
    def _message(self):
        return _(u'Inverse scopes not matching inverses in '
                 u'row: {row}; and columns: {columns}; with values: {values}')


class InverseNodeNotFoundError(DataInputError):

    @property
    def _message(self):
        return _(u'Inverse node not found for item in '
                 u'row: {row}; and columns: {columns}; with values: {values}')

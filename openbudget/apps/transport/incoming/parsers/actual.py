from openbudget.apps.budgets.models import Actual, ActualItem
from openbudget.apps.transport.incoming.parsers import register
from openbudget.apps.transport.incoming.parsers.budget import BudgetParser


class ActualParser(BudgetParser):

    container_model = Actual
    item_model = ActualItem
    ITEM_ATTRIBUTES = ('amount', 'node', 'description', 'actual')

    def _add_to_container(self, obj, key):
        if not self.dry:
            obj['actual'] = self.container_object


register('actual', ActualParser)

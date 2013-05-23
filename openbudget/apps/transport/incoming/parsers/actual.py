from openbudget.apps.budgets.models import Actual, ActualItem, Budget
from openbudget.apps.transport.incoming.parsers import register
from openbudget.apps.transport.incoming.parsers.budget import BudgetParser


class ActualParser(BudgetParser):

    container_model = Actual
    item_model = ActualItem
    ITEM_ATTRIBUTES = ('amount', 'node', 'description', 'actual')
    ITEM_CLEANING_EXCLUDE = ['node', 'actual']

    def _add_to_container(self, obj, key):
        if not self.dry:
            obj['actual'] = self.container_object

    def _get_parent_template(self, container_dict):

        entity = self._set_entity()
        # set the entity also on the template container object
        # it will be used for generating a name and cleaned later
        container_dict['entity'] = entity

        if entity:
            qs = Budget.objects.filter(
                entity=entity,
                period_start__lte=container_dict['period_start'],
                period_end__gte=container_dict['period_end']
            )[:1]

            if qs.count():
                return qs[0].template
            else:
                #TODO: implement forward looking for budgets with a template to inherit
                qs = self.container_model.objects.filter(
                    entity=entity,
                    period_end__lte=container_dict['period_start']
                ).order_by('-period_end')[:1]

                if qs.count():
                    return qs[0].template
                else:
                    return super(ActualParser, self)._get_parent_template(container_dict)

register('actual', ActualParser)

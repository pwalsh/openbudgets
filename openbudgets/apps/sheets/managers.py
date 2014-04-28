from django.db import models


class TemplateManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map_min(self):
        return self.select_related('blueprint')

    def related_map(self):
        return self.select_related('blueprint').prefetch_related(
            'divisions', 'sheets', 'nodes')

    #TODO: Consider better ways to do this.
    def latest_of(self, entity):
        return self.filter(sheets__entity=entity).latest('period_start')


class TemplateNodeManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map_min(self):
        return self.select_related('parent')

    def related_map(self):
        return self.select_related('parent').prefetch_related(
            'templates', 'children', 'backwards', 'inverse', 'items')


class TemplateNodeRelationManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map(self):
        return self.select_related()

    # TODO: check where is used, and implement differently.
    def has_same_node(self, node, template):
        return self.filter(node__code=node.code, node__name=node.name,
                           node__parent=node.parent, template=template).count()


class SheetManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map_min(self):
        return self.select_related('entity')

    def related_map(self):
        return self.select_related('entity', 'template').prefetch_related('items')

    # TODO: Check if we can replace this expensive query
    def latest_of(self, entity):
        return self.filter(entity=entity).latest('period_start')


class SheetItemManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def get_queryset(self):
        qs = super(SheetItemManager, self).get_queryset()
        return qs.select_related('node')

    def related_map_min(self):
        return self.all()

    def related_map(self):
        return self.select_related('sheet', 'parent').prefetch_related('children')

    # TODO: Check this for a more efficient implementation
    def timeline(self, node_pks, entity_pk):
        from .models import TemplateNode
        nodes = TemplateNode.objects.filter(id__in=node_pks)
        timelines = []
        if nodes.count():
            for node in nodes:
                timelines += node.timeline()
        else:
            raise TemplateNode.DoesNotExist()

        return self.filter(node__in=timelines, sheet__entity=entity_pk).select_related('sheet')


class SheetItemCommentManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def get_queryset(self):
        qs = super(SheetItemCommentManager, self).get_queryset()
        return qs.select_related()

    def related_map_min(self):  #
        return self.select_related('user')

    def related_map(self):
        return self.select_related('item', 'user')

    def by_item(self, item_pk):
        return self.filter(item=item_pk).related_map_min()

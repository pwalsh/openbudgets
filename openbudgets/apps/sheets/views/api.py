import datetime
from rest_framework import generics
from rest_framework.response import Response
from openbudgets.apps.sheets import serializers
from openbudgets.apps.sheets import models
from openbudgets.apps.sheets.serializers import SheetTimeline


class TemplateList(generics.ListAPIView):

    """Returns a list of templates."""

    model = models.Template
    queryset = model.objects.related_map_min()
    serializer_class = serializers.TemplateMin
    ordering = ['id', 'name', 'period_start', 'created_on', 'last_modified']
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = super(TemplateList, self).get_queryset()

        ### FILTERS
        domains = self.request.QUERY_PARAMS.get('domains', None)
        divisions = self.request.QUERY_PARAMS.get('divisions', None)
        entities = self.request.QUERY_PARAMS.get('entities', None)

        # DOMAINS: return templates used in the given domain(s).
        if domains:
            domains = domains.split(',')
            queryset = queryset.filter(divisions__domain__in=domains).distinct()

        # DIVISIONS: return templates used in the given division(s).
        if divisions:
            divisions = divisions.split(',')
            queryset = queryset.filter(divisions__in=divisions)

        # ENTITIES: return templates used by the given entity(-ies).
        if entities:
            entities = entities.split(',')
            queryset = queryset.filter(sheets__entity__in=entities)

        # DEFAULT: We just want to return "official" templates, unless a
        # specific filter requires otherwise
        if not self.request.QUERY_PARAMS:
            queryset = queryset.exclude(divisions=None)

        return queryset


class TemplateDetail(generics.RetrieveAPIView):

    """Returns a single template."""

    model = models.Template
    queryset = model.objects.related_map()
    serializer_class = serializers.Template


class TemplateNodeList(generics.ListAPIView):

    """Returns a list of template nodes."""

    model = models.TemplateNode
    queryset = model.objects.related_map()
    serializer_class = serializers.TemplateNode
    ordering = ['id', 'name', 'description', 'created_on', 'last_modified']
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        # TODO: Document this. with_ancestors results in hideous db queries.
        # The only sane way to deal with that is with a tree implementation,
        # such as django-treebeard
        if self.request.QUERY_PARAMS.get('with_ancestors', None):
            return serializers.TemplateNodeAncestors
        return self.serializer_class

    def get_queryset(self):
        queryset = super(TemplateNodeList, self).get_queryset()

        ### FILTERS
        templates = self.request.QUERY_PARAMS.get('templates', None)
        entities = self.request.QUERY_PARAMS.get('entities', None)
        depth = self.request.QUERY_PARAMS.get('depth', None)
        depth_gt = self.request.QUERY_PARAMS.get('depth_gt', None)
        depth_gte = self.request.QUERY_PARAMS.get('depth_gte', None)
        depth_lt = self.request.QUERY_PARAMS.get('depth_lt', None)
        depth_lte = self.request.QUERY_PARAMS.get('depth_lte', None)
        parents = self.request.QUERY_PARAMS.get('parents', None)
        comparable = self.request.QUERY_PARAMS.get('comparable', None)

        # for latest query only:
        entity = self.request.QUERY_PARAMS.get('entity', None)
        latest = self.request.QUERY_PARAMS.get('latest', None)

        # COMPARABLE: return template nodes that match the comparable argument.
        if comparable:
            if comparable == 'true':
                queryset = queryset.filter(comparable=True)
            if comparable == 'false':
                queryset = queryset.filter(comparable=False)

        # TEMPLATES: return template nodes used in the given template(s).
        if templates:
            templates = templates.split(',')
            queryset = queryset.filter(templates__in=templates)

        # ENTITIES: return template nodes of templates used by the given entity(-ies).
        if entities:
            entities = entities.split(',')
            queryset = queryset.filter(sheets__entity__in=entities)

        # DEPTH: return sheet items with a depth amount equal to the
        # given amount.
        if depth:
            queryset = queryset.filter(depth=depth)

        # DEPTH_GT: return sheet items with a depth amount greater than the
        # given amount.
        if depth_gt:
            queryset = queryset.filter(depth__gt=depth_gt)

        # DEPTH_LT: return sheet items with a depth amount less than the
        # given amount.
        if depth_lt:
            queryset = queryset.filter(depth__lt=depth_lt)

        # DEPTH_GTE: return sheet items with a depth amount greater than or
        # equal to the given amount.
        if depth_gte:
            queryset = queryset.filter(depth__gte=depth_gte)

        # DEPTH_LTE: return sheet items with a depth amount less than or
        # equal to the given amount.
        if depth_lte:
            queryset = queryset.filter(depth__lte=depth_lte)

        # PARENTS: return nodes that are children of given parent(s).
        if parents and parents == 'none':
            queryset = queryset.filter(parent__isnull=True)

        elif parents:
            parents = parents.split(',')
            queryset = queryset.filter(parent__in=parents)

        # Check about this
        # was implemented for timeline. Have a feeling we can do it more
        # efficiently elsewhere.
        if entity is not None:
            if latest:
                queryset = models.Template.objects.latest_of(entity=entity).nodes
            else:
                pass

        return queryset


class TemplateNodeDetail(generics.RetrieveAPIView):

    """Returns a single template node."""

    model = models.TemplateNode
    queryset = model.objects.related_map()
    serializer_class = serializers.TemplateNode


class SheetList(generics.ListAPIView):

    """Returns a list of sheets."""

    model = models.Sheet
    queryset = model.objects.related_map_min()
    serializer_class = serializers.SheetMin
    ordering = ['id', 'entity__name', 'period_start', 'created_on', 'last_modified']
    search_fields = ['entity__name', 'description', 'period_start',
                     'period_end']

    def get_queryset(self):
        queryset = super(SheetList, self).get_queryset()

        ### FILTERS
        entities = self.request.QUERY_PARAMS.get('entities', None)
        divisions = self.request.QUERY_PARAMS.get('divisions', None)
        templates = self.request.QUERY_PARAMS.get('templates', None)
        budget_gt = self.request.QUERY_PARAMS.get('budget_gt', None)
        budget_gte = self.request.QUERY_PARAMS.get('budget_gte', None)
        budget_lt = self.request.QUERY_PARAMS.get('budget_gt', None)
        budget_lte = self.request.QUERY_PARAMS.get('budget_gte', None)
        actual_gt = self.request.QUERY_PARAMS.get('actual_gt', None)
        actual_gte = self.request.QUERY_PARAMS.get('actual_gte', None)
        actual_lt = self.request.QUERY_PARAMS.get('actual_gt', None)
        actual_lte = self.request.QUERY_PARAMS.get('actual_gte', None)
        latest = self.request.QUERY_PARAMS.get('latest', None)
        periods = self.request.QUERY_PARAMS.get('periods', None)

        # ENTITIES: return sheets that belong to the given entity(-ies).
        if entities:
            entities = entities.split(',')
            queryset = queryset.filter(entity__in=entities)

        # DIVISIONS: return sheets that are under the given division(s).
        if divisions:
            divisions = divisions.split(',')
            queryset = queryset.filter(entity__division_id__in=divisions)

        # TEMPLATES: return sheets that use the given template(s).
        if templates:
            templates = templates.split(',')
            queryset = queryset.filter(template__in=templates)

        # BUDGET_GT: return sheet items with a budget amount greater than the
        # given amount.
        if budget_gt:
            queryset = queryset.filter(budget__gt=budget_gt)

        # BUDGET_LT: return sheet items with a budget amount less than the
        # given amount.
        if budget_lt:
            queryset = queryset.filter(budget__lt=budget_lt)

        # BUDGET_GTE: return sheets with a budget amount greater than or
        # equal to the given amount.
        if budget_gte:
            queryset = queryset.filter(budget__gte=budget_gte)

        # BUDGET_LTE: return sheets with a budget amount less than or
        # equal to the given amount.
        if budget_lte:
            queryset = queryset.filter(budget__lte=budget_lte)

        # ACTUAL_GT: return sheets with an actual amount greater than the
        # given amount.
        if actual_gt:
            queryset = queryset.filter(actual__gt=actual_gt)

        # ACTUAL_LT: return sheets with an actual amount less than the
        # given amount.
        if actual_lt:
            queryset = queryset.filter(budget__lt=actual_lt)

        # ACTUAL_GTE: return sheets with an actual amount greater than or
        # equal to the given amount.
        if actual_gte:
            queryset = queryset.filter(budget__gte=actual_gte)

        # ACTUAL_LTE: return sheets with an actual amount less than or
        # equal to the given amount.
        if actual_lte:
            queryset = queryset.filter(budget__lte=actual_lte)

        # LATEST: returns the latest sheet only, matching the rest of the query.
        if latest == 'true':
            queryset = queryset.latest('period_start')

        # PERIODS: return contexts matching the given period(s).
        if periods:
            periods = [datetime.date(int(p), 1, 1) for p in periods.split(',')]
            queryset = queryset.filter(period_start__in=periods)

        return queryset


class SheetDetail(generics.RetrieveAPIView):

    """Returns a single sheet."""

    model = models.Sheet
    queryset = model.objects.related_map()
    serializer_class = serializers.Sheet


class SheetItemList(generics.ListAPIView):

    """Returns a list of sheet items."""

    model = models.SheetItem
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetItem
    ordering = ['id', 'sheet__entity__name', 'node__code', 'created_on',
                'last_modified']
    search_fields = ['sheet__entity__name', 'node__code', 'node__name',
                     'description']

    def get_serializer_class(self):
        # TODO: Document this. with_ancestors results in hideous db queries.
        # The only sane way to deal with that is with a tree implementation,
        # such as django-treebeard
        if self.request.QUERY_PARAMS.get('with_ancestors', None):
            return serializers.SheetItemAncestors
        return self.serializer_class

    def get_queryset(self):
        queryset = super(SheetItemList, self).get_queryset()

        ### FILTERS
        sheets = self.request.QUERY_PARAMS.get('sheets', None)
        entities = self.request.QUERY_PARAMS.get('entities', None)
        divisions = self.request.QUERY_PARAMS.get('divisions', None)
        parents = self.request.QUERY_PARAMS.get('parents', None)
        nodes = self.request.QUERY_PARAMS.get('nodes', None)
        node_parents = self.request.QUERY_PARAMS.get('node_parents', None)
        direction = self.request.QUERY_PARAMS.get('direction', None)
        codes = self.request.QUERY_PARAMS.get('codes', None)
        budget_gt = self.request.QUERY_PARAMS.get('budget_gt', None)
        budget_gte = self.request.QUERY_PARAMS.get('budget_gte', None)
        budget_lt = self.request.QUERY_PARAMS.get('budget_lt', None)
        budget_lte = self.request.QUERY_PARAMS.get('budget_lte', None)
        actual_gt = self.request.QUERY_PARAMS.get('actual_gt', None)
        actual_gte = self.request.QUERY_PARAMS.get('actual_gte', None)
        actual_lt = self.request.QUERY_PARAMS.get('actual_lt', None)
        actual_lte = self.request.QUERY_PARAMS.get('actual_lte', None)
        depth = self.request.QUERY_PARAMS.get('depth', None)
        depth_gt = self.request.QUERY_PARAMS.get('depth_gt', None)
        depth_gte = self.request.QUERY_PARAMS.get('depth_gte', None)
        depth_lt = self.request.QUERY_PARAMS.get('depth_lt', None)
        depth_lte = self.request.QUERY_PARAMS.get('depth_lte', None)
        periods = self.request.QUERY_PARAMS.get('periods', None)
        has_comments = self.request.QUERY_PARAMS.get('has_comments', None)
        comparable = self.request.QUERY_PARAMS.get('comparable', None)

        # HAS_COMMENTS: return sheet items that have user discussion.
        if has_comments == 'true':
            queryset = queryset.filter(has_comments=True)

        elif has_comments == 'false':
            queryset = queryset.filter(has_comments=False)

        # COMPARABLE: return sheet items that match the comparable argument.
        if comparable:
            if comparable == 'true':
                queryset = queryset.filter(comparable=True)
            if comparable == 'false':
                queryset = queryset.filter(comparable=False)

        # SHEETS: return sheet items that belong to the given entity(-ies).
        if sheets:
            sheets = sheets.split(',')
            queryset = queryset.filter(sheet__in=sheets)

        # ENTITIES: return sheet items that belong to the given entity(-ies).
        if entities:
            entities = entities.split(',')
            queryset = queryset.filter(sheet__entity__in=entities)

        # DIVISIONS: return sheet items that are under the given division(s).
        if divisions:
            divisions = divisions.split(',')
            queryset = queryset.filter(sheet__entity__division_id__in=divisions)

        # DIRECTION: return sheet items in the given direction.
        if direction:
            direction = direction.upper()
            queryset = queryset.filter(direction=direction)

        # CODES: return sheet items that match the given code(s).
        if codes:
            codes = codes.split(',')
            queryset = queryset.filter(code__in=codes)

        # PARENTS: return items that are children of given parent(s).
        if parents and parents == 'none':
            queryset = queryset.filter(parent__isnull=True)

        elif parents:
            parents = parents.split(',')
            queryset = queryset.filter(parent__pk__in=parents)

        # NODES: return sheet items that belong to the given node(s).
        if nodes:
            nodes = nodes.split(',')
            queryset = queryset.filter(node_id__in=nodes)

        # NODE PARENTS: return items that are children of given node parent(s).
        if node_parents and node_parents == 'none':
            queryset = queryset.filter(node__parent_id__isnull=True)

        elif node_parents:
            node_parents = node_parents.split(',')
            queryset = queryset.filter(node__parent_id__in=node_parents)

        # BUDGET_GT: return sheet items with a budget amount greater than the
        # given amount.
        if budget_gt:
            queryset = queryset.filter(budget__gt=budget_gt)

        # BUDGET_LT: return sheet items with a budget amount less than the
        # given amount.
        if budget_lt:
            queryset = queryset.filter(budget__lt=budget_lt)

        # BUDGET_GTE: return sheet items with a budget amount greater than or
        # equal to the given amount.
        if budget_gte:
            queryset = queryset.filter(budget__gte=budget_gte)

        # BUDGET_LTE: return sheet items with a budget amount less than or
        # equal to the given amount.
        if budget_lte:
            queryset = queryset.filter(budget__lte=budget_lte)

        # ACTUAL_GT: return sheet items with an actual amount greater than the
        # given amount.
        if actual_gt:
            queryset = queryset.filter(actual__gt=actual_gt)

        # ACTUAL_LT: return sheet items with an actual amount less than the
        # given amount.
        if actual_lt:
            queryset = queryset.filter(actual__lt=actual_lt)

        # ACTUAL_GTE: return sheet items with an actual amount greater than or
        # equal to the given amount.
        if actual_gte:
            queryset = queryset.filter(actual__gte=actual_gte)

        # ACTUAL_LTE: return sheet items with an actual amount less than or
        # equal to the given amount.
        if actual_lte:
            queryset = queryset.filter(actual__lte=actual_lte)

        # DEPTH: return sheet items with a depth amount equal to the
        # given amount.
        if depth:
            queryset = queryset.filter(depth=depth)

        # DEPTH_GT: return sheet items with a depth amount greater than the
        # given amount.
        if depth_gt:
            queryset = queryset.filter(depth__gt=depth_gt)

        # DEPTH_LT: return sheet items with a depth amount less than the
        # given amount.
        if depth_lt:
            queryset = queryset.filter(depth__lt=depth_lt)

        # DEPTH_GTE: return sheet items with a depth amount greater than or
        # equal to the given amount.
        if depth_gte:
            queryset = queryset.filter(depth__gte=depth_gte)

        # DEPTH_LTE: return sheet items with a depth amount less than or
        # equal to the given amount.
        if depth_lte:
            queryset = queryset.filter(depth__lte=depth_lte)

        # PERIODS: return sheet items matching the given period(s).
        if periods:
            periods = [datetime.date(int(p), 1, 1) for p in periods.split(',')]
            queryset = queryset.filter(sheet__period_start__in=periods)

        return queryset


class SheetItemDetail(generics.RetrieveAPIView):

    """Returns a single sheet item."""

    model = models.SheetItem
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetItem


class SheetItemTimeline(generics.ListAPIView):

    """Returns a timeline of sheet items.

    The timeline is created according to the given entity, node(s).

    """

    def get(self, request, entity_pk, *args, **kwargs):
        """GET handler for retrieving all budget items and actual items
        of the node's timeline, filtered by entity.

        """

        nodes = self.request.QUERY_PARAMS.get('nodes', None)
        if nodes:
            nodes = nodes.split(',')
        else:
            # Provide a sensible default.
            # If there is no node query param, let's return the top level nodes,
            # as used in the latest Sheet.
            #nodes = [for models.Sheet.objects.latest_of(entity_pk).shee]
            #TODO: handle case of no nodes specified
            pass
        items = models.SheetItem.objects.timeline(nodes, entity_pk)

        serialized_timeline = SheetTimeline(items, many=True).data

        return Response(serialized_timeline)


class SheetItemCommentList(generics.ListCreateAPIView):

    """Returns a list of sheet item comments.

    Also allows saving of new comments.

    """

    model = models.SheetItemComment
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetItemCommentMin
    search_fields = ['user__first_name', 'user__last_name', 'comment']


class SheetItemCommentDetail(generics.RetrieveAPIView):

    """Returns a single sheet item comment item."""

    model = models.SheetItemComment
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetItemComment

from copy import deepcopy
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.sheets.models import Template, Sheet, SheetItem
from openbudgets.apps.entities.models import Entity
from openbudgets.apps.transport.incoming.parsers import register, ParsingError
from openbudgets.apps.transport.incoming.parsers.template import TemplateParser
from openbudgets.apps.transport.incoming.errors import MetaParsingError, NodeNotFoundError


def _rows_filter(obj, row_num=None):
    if obj['has_children']:
        return True
    else:
        if 'budget' in obj:
            if obj['budget'] is not None:
                return True
            else:
                return 'actual' in obj and obj['actual'] is not None

        elif 'actual' in obj:
            return obj['actual'] is not None

        else:
            raise ParsingError(_('Neither actual nor budget columns found.'))


class SheetParser(TemplateParser):

    container_model = Sheet
    item_model = SheetItem
    ITEM_ATTRIBUTES = ('budget', 'actual', 'node', 'description', 'sheet')
    CONTAINER_ATTRIBUTES = ('entity', 'period_start', 'period_end')
    ITEM_CLEANING_EXCLUDE = ('node', 'sheet', 'code', 'name', 'path')

    def __init__(self, container_object_dict):
        super(SheetParser, self).__init__(container_object_dict)
        self.template_parser = self._init_template_parser()

    @classmethod
    def resolve(cls, deferred):
        container_dict = deferred['container']

        if not container_dict:
            raise Exception('Deferred object missing container dict: %s' % container_dict)

        instance = cls(container_dict)
        instance.objects_lookup = deferred['items']

        instance.template_parser.objects_lookup = deferred['template_parser']['items']

        return instance

    def clean(self, data):
        for row_num, obj in enumerate(data):
            self._clean_amount(obj, 'actual')
            self._clean_amount(obj, 'budget')

        return super(SheetParser, self).clean(data=data)

    def _clean_amount(self, obj, attr):
        missing = '__missing__'

        amount = obj.get(attr, missing)

        if amount == missing or amount == '':
            obj[attr] = None
        else:
            try:
                obj[attr] = float(obj[attr])
            except (ValueError, TypeError):
                obj[attr] = None

    def validate(self, data, keep_cache=False):
        # do the sheet clean first
        data = self.clean(data)

        if self.template_parser:
            template_valid, template_errors = self.template_parser.validate(data=deepcopy(data), keep_cache=True)
            self.skipped_rows = self.template_parser.skipped_rows
        else:
            #TODO: add support for parsing sheets without a parent template to inherit from
            template_valid = False
            template_errors = []

        # here we continue with the rest the `super` logic for `validate()`
        # generate a lookup table with each item uniquely identified
        self._generate_lookup(data)

        self.keep_cache = keep_cache
        # run a dry save of the data
        self.save(dry=True)

        if self.template_parser:
            self.template_parser._clear_cache()

        return template_valid and self.valid, self.errors + template_errors

    def save(self, dry=False):
        template_saved = True

        if not dry:
            template_saved = self.template_parser.save()

        if template_saved:
            self.dry = dry

            # create an instance of the container
            self._create_container()

            if dry:
                # loop the lookup table and save every item
                for key, obj in self.objects_lookup.iteritems():
                    self._save_item(obj, key)

                if not self.keep_cache:
                    self._clear_cache()

            else:
                template_cache = self.template_parser.saved_cache
                # loop the template's saved nodes cache and save item for every node that's not in the sourcefile
                for key, obj in template_cache.iteritems():
                    if key not in self.objects_lookup:
                        self._save_item(obj, key, is_node=True)

                # loop the lookup table and save item for every row
                for key, obj in self.objects_lookup.iteritems():
                    self._save_item(obj, key)

                # post save
                self._save_amounts()
                self._save_sheet_amounts()

            self.dry = False

            self.template_parser.cleanup()
            self.cleanup()

            return True

        return False

    def deferred(self):
        deferred = super(SheetParser, self).deferred()
        deferred['template_parser'] = self.template_parser.deferred()
        return deferred

    def _save_item(self, obj, key, is_node=False):
        node = None
        # check if we already saved this object and have it in cache
        if key in self.saved_cache:
            return self.saved_cache[key]

        if is_node:
            node = obj
            obj = {}

        self._add_to_container(obj, key)

        item = self._create_item(obj, key, node)

        # cache the saved object
        self.saved_cache[key] = item

    def _create_container(self, container_dict=None, exclude=None):

        data = container_dict or self.container_object_dict
        data['template'] = self.template_parser.container_object

        fields_to_exclude = ['template']
        if exclude:
            fields_to_exclude += exclude

        super(TemplateParser, self)._create_container(container_dict=data, exclude=fields_to_exclude)

    def _generate_lookup(self, data):
        self.rows_objects_lookup = self.template_parser.rows_objects_lookup
        self.objects_lookup = deepcopy(self.template_parser.objects_lookup)

    def _create_item(self, obj, key, node=None):

        if node:
            obj['node'] = node

        elif key in self.template_parser.saved_cache:
            obj['node'] = self.template_parser.saved_cache[key]

        elif self.dry:
            # prepare data for the error
            columns = ['code', 'parent', 'parentscope']
            values = []
            for col in columns:
                if col not in obj:
                    columns.remove(col)
                else:
                    values.append(obj[col])
            self.throw(
                NodeNotFoundError(
                    row=self.rows_objects_lookup[key],
                    columns=columns,
                    values=values
                )
            )
        else:
            raise ParsingError(_('Did not find a node for the item in row: %s') % self.rows_objects_lookup[key])

        return super(TemplateParser, self)._create_item(obj, key)

    def _clean_object(self, obj, key):
        super(SheetParser, self)._clean_object(obj, key)

        if 'budget' not in obj or obj['budget'] == '':
            obj['budget'] = None

        if 'actual' not in obj or obj['actual'] == '':
            obj['actual'] = None

    def _add_to_container(self, obj, key):
        if not self.dry:
            obj['sheet'] = self.container_object

    def _init_template_parser(self):
        container_dict_copy = deepcopy(self.container_object_dict)

        #TODO: refactor this into a proper clean method
        if 'template' in container_dict_copy:
            del container_dict_copy['template']

        parent_template, blueprint = self._get_parent_template(container_dict_copy)

        if 'period_end' in container_dict_copy:
            del container_dict_copy['period_end']

        if parent_template:
            return TemplateParser(container_dict_copy, extends=parent_template, blueprint=blueprint, rows_filters=(_rows_filter,))

        return False

    def _get_parent_template(self, container_dict):

        parent = None
        blueprint = None

        entity = self._set_entity()
        # set the entity also on the template container object
        # it will be used for generating a name and cleaned later
        container_dict['entity'] = entity

        if entity:
            date = datetime.strptime(container_dict['period_start'], '%Y-%m-%d')
            try:
                blueprint = entity.division.templates.filter(period_start__lte=date).order_by('-period_start')[0]
                container_dict['blueprint'] = blueprint
            except IndexError:
                raise ParsingError(_(u'Could not find a '
                                     u'blueprint template for entity {entity}'
                                     u' and start date '
                                     u'{period_start}').format(entity=entity.name,
                                                               period_start=container_dict['period_start']))

        if entity:
            # try getting the container model for same period or containing it
            qs = self.container_model.objects.filter(
                entity=entity,
                period_start__lte=container_dict['period_start'],
                period_end__gte=container_dict['period_end']
            ).order_by('-period_end')[:1]

            if qs.count():
                parent = qs[0].template
            else:
                # try getting the latest container model prior to this one
                qs = self.container_model.objects.filter(
                    entity=entity,
                    period_end__lte=container_dict['period_start']
                ).order_by('-period_end')[:1]

                if qs.count():
                    parent = qs[0].template
                else:
                    # try getting the earliest container model later then this one
                    qs = self.container_model.objects.filter(
                        entity=entity,
                        period_start__gte=container_dict['period_end']
                    ).order_by('period_start')[:1]

                    if qs.count():
                        parent = qs[0].template
                    else:
                        # try getting the standard template for this entity's division
                        qs = Template.objects.filter(
                            divisions=entity.division,
                            period_start__lte=container_dict['period_start']
                        ).order_by('-period_start')[:1]

                        if qs.count():
                            parent = qs[0]
                        else:
                            #TODO: handle this case of no previous template found
                            raise ParsingError(_('Could not find a parent template for input: %s') % container_dict)
        return parent, blueprint

    def _set_entity(self):

        container_dict = self.container_object_dict

        try:
            if not isinstance(container_dict['entity'], Entity):
                entity = Entity.objects.get(pk=container_dict['entity'])

                return entity

            else:
                return container_dict['entity']

        except Entity.DoesNotExist as e:
            if self.dry:
                self.throw(
                    MetaParsingError(
                        reason='Could not find Entity with key: %s' % container_dict['entity']
                    )
                )
            else:
                raise e

    def _save_sheet_amounts(self):

        summable_items = self.item_model.objects.filter(sheet=self.container_object,
                                                        node__parent__isnull=True,
                                                        node__direction='EXPENDITURE')
        sheet_budget = sum([item.budget or 0 for item in summable_items])
        sheet_actual = sum([item.actual or 0 for item in summable_items])
        self.container_object.budget = sheet_budget
        self.container_object.actual = sheet_actual
        self.container_object.save()

    def _save_amounts(self):
        children_lookup = {}
        keys_by_level = {1: []}

        def _make_adder(attr):
            def _add(a, b):
                b_value = getattr(b, attr)
                if a is None:
                    if b_value is None:
                        return None

                    else:
                        return float(b_value)

                elif b_value is None:
                    return a

                else:
                    return a + float(b_value)

            return _add

        for key, item in self.saved_cache.iteritems():
            node = item.node
            parent = node.parent

            if parent:
                parent_key = parent.path
                level = len(parent_key.split(self.PATH_DELIMITER))

                if parent_key not in children_lookup:
                    children_lookup[parent_key] = []
                children_lookup[parent_key].append(item)

                if not level in keys_by_level:
                    keys_by_level[level] = []
                keys_by_level[level].append(parent_key)

            else:
                parent_key = node.path
                if parent_key not in children_lookup:
                    children_lookup[parent_key] = []
                keys_by_level[1].append(parent_key)

        levels = keys_by_level.keys()
        levels.sort(reverse=True)
        for level in levels:
            keys = keys_by_level[level]
            for key in keys:
                children = children_lookup[key]
                item = self.saved_cache[key]

                for child in children:
                    # set the item's parent for all children
                    child.parent = item
                    child.save()

                item.budget = reduce(_make_adder('budget'), children, None)
                item.actual = reduce(_make_adder('actual'), children, None)
                item.save()


register('sheet', SheetParser)

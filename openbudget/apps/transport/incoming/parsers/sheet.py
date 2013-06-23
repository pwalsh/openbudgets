from copy import deepcopy
from django.utils.translation import gettext as __
from openbudget.apps.sheets.models import Template, Sheet, SheetItem
from openbudget.apps.entities.models import Entity
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.transport.incoming.parsers import register, ParsingError
from openbudget.apps.transport.incoming.parsers.template import TemplateParser
from openbudget.apps.transport.incoming.errors import MetaParsingError, NodeNotFoundError


def _rows_filter(obj, row_num=None):
    if obj['has_children']:
        return True
    else:
        try:
            float(obj['budget'])
            return True
        except (KeyError, ValueError, TypeError):
            try:
                float(obj['actual'])
                return True
            except (KeyError, ValueError, TypeError):
                pass

        return False


class SheetParser(TemplateParser):

    container_model = Sheet
    item_model = SheetItem
    ITEM_ATTRIBUTES = ['budget', 'actual', 'node', 'description', 'sheet']\
                      + translated_fields(SheetItem)
    ITEM_CLEANING_EXCLUDE = ['node', 'sheet']

    def __init__(self, container_object_dict):
        super(SheetParser, self).__init__(container_object_dict)
        self.skipped_rows = {}
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

    def validate(self, data, keep_cache=False):
        if self.template_parser:
            template_valid, template_errors = self.template_parser.validate(data=deepcopy(data), keep_cache=True)
        else:
            #TODO: add support for parsing sheets without a parent template to inherit from
            template_valid = False
            template_errors = []

        valid, sheet_errors = super(SheetParser, self).validate(data)

        if self.template_parser:
            self.template_parser._clear_cache()

        return template_valid and valid, sheet_errors + template_errors

    def save(self, dry=False):
        template_saved = True

        if not dry:
            template_saved = self.template_parser.save()

        if template_saved:
            self.dry = dry

            # create an instance of the container
            self._create_container()

            if dry:
                # save an untempered copy
                lookup_table_copy = deepcopy(self.objects_lookup)

                # loop the lookup table and save every item
                for key, obj in self.objects_lookup.iteritems():
                    self._save_item(obj, key)

                if not self.keep_cache:
                    self._clear_cache()
                # clear all changes by replacing the lookup with the old copy
                self.objects_lookup = lookup_table_copy

            else:
                # loop the lookup table and save item for every row
                for key, obj in self.objects_lookup.iteritems():
                    self._save_item(obj, key)
                # loop the template's saved nodes cache and save item for node
                for key, obj in self.template_parser.saved_cache.iteritems():
                    self._save_item(obj, key, is_node=True)

            self.dry = False

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
            raise ParsingError(__('Did not find a node for the item in row: %s') % self.rows_objects_lookup[key])

        self._clean_object(obj, key)
        if not self.dry:
            item = self.item_model.objects.create(**obj)
        else:
            item = self.item_model(**obj)
            self._dry_clean(item, self.rows_objects_lookup[key], exclude=self.ITEM_CLEANING_EXCLUDE)

        return item

    def _add_to_container(self, obj, key):
        if not self.dry:
            obj['sheet'] = self.container_object

    def _init_template_parser(self):
        container_dict_copy = deepcopy(self.container_object_dict)

        #TODO: refactor this into a proper cleanup method
        if 'template' in container_dict_copy:
            del container_dict_copy['template']

        parent_template = self._get_parent_template(container_dict_copy)

        if 'period_end' in container_dict_copy:
            del container_dict_copy['period_end']

        if parent_template:
            return TemplateParser(container_dict_copy, extends=parent_template, rows_filters=(_rows_filter,))

        return False

    def _get_parent_template(self, container_dict):

        entity = self._set_entity()
        # set the entity also on the template container object
        # it will be used for generating a name and cleaned later
        container_dict['entity'] = entity

        if entity:
            # try getting the container model for same period or containing it
            qs = self.container_model.objects.filter(
                entity=entity,
                period_start__lte=container_dict['period_start'],
                period_end__gte=container_dict['period_end']
            ).order_by('-period_end')[:1]

            if qs.count():
                return qs[0].template
            else:
                # try getting the latest container model prior to this one
                qs = self.container_model.objects.filter(
                    entity=entity,
                    period_end__lte=container_dict['period_start']
                ).order_by('-period_end')[:1]

                if qs.count():
                    return qs[0].template
                else:
                    # try getting the earliest container model later then this one
                    qs = self.container_model.objects.filter(
                        entity=entity,
                        period_start__gte=container_dict['period_end']
                    ).order_by('period_start')[:1]

                    if qs.count():
                        return qs[0].template
                    else:
                        # try getting the standard template for this entity's division
                        qs = Template.objects.filter(
                            divisions=entity.division,
                            period_start__lte=container_dict['period_start']
                        ).order_by('-period_start')[:1]

                        if qs.count():
                            return qs[0]
                        else:
                            #TODO: handle this case of no previous template found
                            raise ParsingError(__('Could not find a parent template for input: %s') % container_dict)

    def _set_entity(self):

        container_dict = self.container_object_dict

        try:
            if not isinstance(container_dict['entity'], Entity):
                entity = Entity.objects.get(
                    pk=container_dict['entity']
                )
                container_dict['entity'] = entity

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


register('sheet', SheetParser)

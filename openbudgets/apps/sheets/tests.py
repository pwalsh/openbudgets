from django.test import TestCase
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from openbudgets.apps.sheets import factories
from openbudgets.apps.entities.factories import Division, Entity
from openbudgets.commons import tests


class TemplateLogicTestCase(TestCase):
    """Tests the implemented logic of the template implementation:

    * code unique in parent scope
    * 'dangling nodes' - nodes that are not in a blueprint template, but added
    on a case-by-case basis
    * 'morphing nodes' - support for different nodes to have the same meaning
    over time.

    """

    def setUp(self):
        """
        Creating 2 additional templates:
            1. template_1 which inherits base template
            2. templtae_2 which inherits template_1

        Creating 3 additional, dangling nodes on template_1 and 2 on template_2.
        """

        # create required divisions and entities
        self.division = Division.create()
        self.entities = Entity.create_batch(5, division=self.division)

        # create the blueprint template, and two templates for use by sheets
        self.tmpl_blueprint = factories.Template.create(divisions=[self.division])
        self.tmpl_one = factories.Template.create(blueprint=self.tmpl_blueprint)
        self.tmpl_two = factories.Template.create(blueprint=self.tmpl_blueprint)

        # create the blueprint nodes, and assign them to the blueprint and the
        # "inheriting" templates
        self.rev_nodes = factories.TemplateNode.create_batch(5)

        for node in self.rev_nodes:
            factories.TemplateNodeRelation(node=node, template=self.tmpl_blueprint)
            factories.TemplateNodeRelation(node=node, template=self.tmpl_one)
            factories.TemplateNodeRelation(node=node, template=self.tmpl_two)

        self.rev_nodes[1].parent = self.rev_nodes[0]
        self.rev_nodes[2].parent = self.rev_nodes[0]
        self.rev_nodes[3].parent = self.rev_nodes[1]
        self.rev_nodes[4].parent = self.rev_nodes[2]

        for node in self.rev_nodes:
            node.save()

        self.exp_nodes = factories.TemplateNode.create_batch(5, direction="EXPENDITURE")

        for node in self.exp_nodes:
            factories.TemplateNodeRelation(node=node, template=self.tmpl_blueprint)
            factories.TemplateNodeRelation(node=node, template=self.tmpl_one)
            factories.TemplateNodeRelation(node=node, template=self.tmpl_two)

        self.exp_nodes[1].parent = self.exp_nodes[0]
        self.exp_nodes[2].parent = self.exp_nodes[0]
        self.exp_nodes[3].parent = self.exp_nodes[1]
        self.exp_nodes[4].parent = self.exp_nodes[2]

        for node in self.exp_nodes:
            node.save()

        # some additional nodes for template 1
        self.tmpl_one_extra_nodes = factories.TemplateNode.create_batch(2)

        for node in self.tmpl_one_extra_nodes:
            factories.TemplateNodeRelation(node=node, template=self.tmpl_one)

        self.tmpl_one_extra_nodes[0].direction = "EXPENDITURE"
        self.tmpl_one_extra_nodes[0].parent = self.exp_nodes[4]
        self.tmpl_one_extra_nodes[0].parent = self.rev_nodes[3]

        for node in self.tmpl_one_extra_nodes:
            node.save()

        # some additional nodes for template 2
        self.tmpl_two_extra_nodes = factories.TemplateNode.create_batch(2)

        for node in self.tmpl_two_extra_nodes:
            factories.TemplateNodeRelation(node=node, template=self.tmpl_two)

        self.tmpl_two_extra_nodes[0].direction = "EXPENDITURE"
        self.tmpl_two_extra_nodes[0].parent = self.exp_nodes[1]
        self.tmpl_two_extra_nodes[0].parent = self.rev_nodes[0]

        for node in self.tmpl_two_extra_nodes:
            node.save()

        # some nodes from template 1 also shared by template 2
        factories.TemplateNodeRelation(node=self.tmpl_one_extra_nodes[0], template=self.tmpl_two)

    def test_path_creation(self):

        expected_path = ','.join([self.rev_nodes[4].code,
                                  self.rev_nodes[2].code,
                                  self.rev_nodes[0].code])

        self.assertEqual(expected_path, self.rev_nodes[4].path)

    def test_code_unique_in_parent_scope(self):

        for n in self.tmpl_blueprint.nodes.all():
            nodes = {}

            children = list(n.children.all())

            if children and len(children) > 1:
                nodes[n.code] = [child for child in children]
                children[0].code = children[1].code
                self.assertRaises(IntegrityError, children[0].save())

            for k, v in nodes:
                self.assertEqual(len(set(v)), len(v))

    def test_template_diffs(self):
        blueprint = [node.path for node in self.tmpl_blueprint.nodes.all()]
        tmpl_one = [node.path for node in self.tmpl_one.nodes.all()]
        tmpl_two = [node.path for node in self.tmpl_two.nodes.all()]
        diff_one = set(blueprint).symmetric_difference(set(tmpl_one))
        diff_two = set(blueprint).symmetric_difference(set(tmpl_two))
        diff_three = set(tmpl_one).symmetric_difference(set(tmpl_two))

        self.assertEqual(2, len(diff_one))
        self.assertEqual(3, len(diff_two))
        self.assertEqual(3, len(diff_three))

    def test_blueprint_status(self):
        self.assertTrue(self.tmpl_blueprint.is_blueprint)
        self.assertFalse(self.tmpl_one.is_blueprint)
        self.assertFalse(self.tmpl_two.is_blueprint)

    def test_tmpl_one_has_blueprint_nodes(self):
        for node in self.tmpl_blueprint.nodes.all():
            self.assertIn(node, self.tmpl_one.nodes.all())

    def test_tmpl_two_has_blueprint_nodes(self):
        for node in self.tmpl_blueprint.nodes.all():
            self.assertIn(node, self.tmpl_two.nodes.all())

    def test_morphing_node_same_code(self):
        """Test case where a code remains consistent, other values
        (eg: name, parent), have changed, and a *relation* of sameness has been
        made between the nodes via the 'backwards' attribute.

        The test goes two levels back. The first level back has a different
        name, and the second level back has a different name and parent.

        Test morphing nodes using template inheritance and manual backwards setting.

        """

        dummy_back_two_tmpl = factories.Template.create(
            blueprint=self.tmpl_blueprint)

        dummy_back_one_tmpl = factories.Template.create(
            blueprint=self.tmpl_blueprint)

        dummy_back_two_node = factories.TemplateNode.create(
            code=self.tmpl_one.nodes.all()[0].code,
            parent=self.tmpl_one.nodes.all()[4].parent,
            direction=self.tmpl_one.nodes.all()[0].direction)

        factories.TemplateNodeRelation(node=dummy_back_two_node,
                                              template=dummy_back_two_tmpl)

        dummy_back_one_node = factories.TemplateNode.create(
            code=self.tmpl_one.nodes.all()[0].code,
            parent=self.tmpl_one.nodes.all()[0].parent,
            direction=self.tmpl_one.nodes.all()[0].direction,
            backwards=[dummy_back_two_node])

        factories.TemplateNodeRelation(node=dummy_back_one_node,
                                              template=dummy_back_one_tmpl)

        self.tmpl_one.nodes.all()[0].backwards.add(dummy_back_one_node)

        # Now, we create Sheets that use these Templates.

        sheet_two = factories.Sheet.create(entity=self.entities[0],
                                                  template=dummy_back_two_tmpl)

        sheet_one = factories.Sheet.create(entity=self.entities[0],
                                                  template=dummy_back_one_tmpl)

        sheet_current = factories.Sheet.create(entity=self.entities[0],
                                                  template=self.tmpl_one)

        sheet_item_two = factories.SheetItem.create(sheet=sheet_two,
                                                           node=dummy_back_two_node,
                                                           budget=350.00,
                                                           actual=479.00)

        sheet_item_one = factories.SheetItem.create(sheet=sheet_one,
                                                           node=dummy_back_one_node,
                                                           budget=995.00,
                                                           actual=911.00)

        sheet_item_current = factories.SheetItem.create(sheet=sheet_current,
                                                               node=self.tmpl_one.nodes.all()[0],
                                                               budget=1000.00,
                                                               actual=1137.00)
        from openbudgets.apps.sheets.models import SheetItem
        item_timeline = SheetItem.objects.filter(
            node__in=self.tmpl_one.nodes.all()[0].with_past)

        item_timeline_codes = [item.node.code for item in item_timeline]

        self.assertIn(sheet_item_current, item_timeline)
        self.assertIn(sheet_item_two, item_timeline)
        self.assertIn(sheet_item_one, item_timeline)
        self.assertTrue(len(set(item_timeline_codes)) == 1)


class TemplateViewTestCase(TestCase):

    def setUp(self):
        self.divisions = Division.create_batch(3)
        self.template = factories.Template.create(
            divisions=self.divisions)

    def test_template_listview(self):

        listview = reverse('template_list')
        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_template_detailview(self):

        detailview = reverse('template_detail',
            args=(self.template.pk,))

        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)


class SheetViewTestCase(TestCase):

    def setUp(self):
        self.sheet = factories.Sheet.create()

    def test_sheet_listview(self):

        listview = reverse('sheet_list')
        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_sheet_detailview(self):

        detailview = reverse('sheet_detail',
            args=(self.sheet.entity.slug, self.sheet.period)
        )
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)


class SheetUITestCase(tests.OpenBudgetsUITestCase):

    listview_name = 'sheet_list'
    detailview_name = 'sheet_detail'

    def setUp(self):
        self.object = factories.Sheet.create()

    def test_listview(self):
        return SheetUITestCase.listview(self)

    # TODO: Write a test for this url pattern
    #def test_detailview(self):
    #    return SheetUITestCase.detailview(self)


class SheetItemUITestCase(tests.OpenBudgetsUITestCase):

    listview_name = 'sheet_item_list'
    detailview_name = 'sheet_item_detail'

    def setUp(self):
        self.object = factories.SheetItem.create()

    def test_detailview(self):
        return SheetItemUITestCase.detailview(self)


class SheetDownloadTestCase(TestCase):

    def setUp(self):
        self.object = factories.Sheet.create()

    def test_download_csv(self):
        pass

    def test_download_xls(self):
        pass

    def test_download_xlsx(self):
        pass


class TemplateUITestCase(tests.OpenBudgetsUITestCase):

    listview_name = 'template_list'
    detailview_name = 'template_detail'

    def setUp(self):
        self.object = factories.Template.create()

    def test_listview(self):
        return TemplateUITestCase.listview(self)

    def test_detailview(self):
        return TemplateUITestCase.detailview(self)


class TemplateNodeUITestCase(tests.OpenBudgetsUITestCase):

    listview_name = 'template_node_list'
    detailview_name = 'template_node_detail'

    def setUp(self):
        self.object = factories.TemplateNode.create()

    def test_detailview(self):
        return TemplateNodeUITestCase.detailview(self)


class SheetAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'sheet-list'
    detailview_name = 'sheet-detail'

    def setUp(self):
        self.object = factories.Sheet.create()

    def test_listview(self):
        return SheetAPITestCase.listview(self)

    def test_detailview(self):
        return SheetAPITestCase.detailview(self)


class SheetItemAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'sheetitem-list'
    detailview_name = 'sheetitem-detail'

    def setUp(self):
        self.object = factories.SheetItem.create()

    def test_listview(self):
        return SheetItemAPITestCase.listview(self)

    def test_detailview(self):
        return SheetItemAPITestCase.detailview(self)


class SheetItemCommentAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'sheetitemcomment-list'
    detailview_name = 'sheetitemcomment-detail'

    def setUp(self):
        self.object = factories.SheetItemComment.create()

    def test_listview(self):
        return SheetItemCommentAPITestCase.listview(self)

    def test_detailview(self):
        return SheetItemCommentAPITestCase.detailview(self)


class TemplateAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'template-list'
    detailview_name = 'template-detail'

    def setUp(self):
        self.object = factories.Template.create()

    def test_listview(self):
        return TemplateAPITestCase.listview(self)

    def test_detailview(self):
        return TemplateAPITestCase.detailview(self)


class TemplateNodeAPITestCase(tests.OpenBudgetsAPITestCase):

    listview_name = 'templatenode-list'
    detailview_name = 'templatenode-detail'

    def setUp(self):
        self.object = factories.TemplateNode.create()

    def test_listview(self):
        return TemplateNodeAPITestCase.listview(self)

    def test_detailview(self):
        return TemplateNodeAPITestCase.detailview(self)

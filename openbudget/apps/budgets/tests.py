import random
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudget.apps.budgets.factories import BudgetTemplateFactory,BudgetFactory, ActualFactory
from openbudget.apps.entities.factories import DomainDivisionFactory, EntityFactory
from openbudget.apps.budgets.models import Template, TemplateNode, TemplateNodeRelation, Budget, BudgetItem


class TemplateInheritanceTestCase(TestCase):
    """Testing templates inheritance, dangling template nodes and nodes morphing over time"""

    fixtures = ['tmp_budgets_tests.json']

    def setUp(self):
        """
        Creating 2 additional templates:
            1. template_1 which inherits base template
            2. templtae_2 which inherits template_1

        Creating 3 additional, dangling nodes on template_1 and 2 on template_2.
        """
        base = Template.objects.get(pk=1)
        self.base = base

        base_nodes = base.nodes.all()
        self.codes = [node.code for node in base_nodes]

        # create a new template: template_1 inherits base
        self.template_1 = Template.objects.create(
            name=base.name + "'s child"
        )
        for node in base_nodes:
            TemplateNodeRelation.objects.create(
                template=self.template_1,
                node=node
            )

        # creating dangling nodes
        parent = base_nodes[5]
        parent_code = parent.code
        self.node_1_1 = TemplateNode.objects.create(
            name=parent.name + "'s child",
            code=parent_code + '-1',
            parent=parent,
            direction=parent.direction
        )
        TemplateNodeRelation.objects.create(
            template=self.template_1,
            node=self.node_1_1
        )

        parent = base_nodes[4]
        parent_code = parent.code
        self.node_1_2 = TemplateNode.objects.create(
            name=parent.name + "'s child",
            code=parent_code + '-1',
            parent=parent,
            direction=parent.direction
        )
        TemplateNodeRelation.objects.create(
            template=self.template_1,
            node=self.node_1_2
        )

        parent = self.node_1_2
        parent_code = parent.code
        self.node_1_2_1 = TemplateNode.objects.create(
            name=parent.name + "'s child",
            code=parent_code + '-1',
            parent=parent,
            direction=parent.direction
        )
        TemplateNodeRelation.objects.create(
            template=self.template_1,
            node=self.node_1_2_1
        )

        # create a new template: template_2 inherits template_1
        self.template_2 = Template.objects.create(
            name=self.template_1.name + "'s child"
        )
        for node in self.template_1.nodes.all():
            TemplateNodeRelation.objects.create(
                template=self.template_2,
                node=node
            )

        parent = self.node_1_1
        parent_code = parent.code
        self.node_2_1 = TemplateNode.objects.create(
            name=parent.name + "'s child",
            code=parent_code + '-1',
            parent=parent,
            direction=parent.direction
        )
        TemplateNodeRelation.objects.create(
            template=self.template_2,
            node=self.node_2_1
        )

        parent = self.node_1_2_1
        parent_code = parent.code
        self.node_2_2 = TemplateNode.objects.create(
            name=parent.name + "'s child",
            code=parent_code + '-1',
            parent=parent,
            direction=parent.direction
        )
        TemplateNodeRelation.objects.create(
            template=self.template_2,
            node=self.node_2_2
        )

    def test_dangling_nodes_level_1(self):
        """
        Test dangling nodes using template inheritance.

        Level 1:
        Test that template_1 contains exactly the nodes of base + node_1_1, node_1_2 and node_1_2_1

        Level 2:
        Test that template_2 contains exactly the nodes of base + nodes of template_1 + node_2_1 and node_2_2
        """

        # set up level 1
        nodes = self.template_1.nodes.all()
        base_nodes = self.base.nodes.all()

        # test level 1
        self.assertIn(self.node_1_1, nodes)
        self.assertIn(self.node_1_2, nodes)
        self.assertIn(self.node_1_2_1, nodes)

        for node in base_nodes:
            self.assertIn(node, nodes)

        self.assertEqual(len(nodes), len(base_nodes) + 3)

        # set up level 2
        nodes = self.template_2.nodes.all()
        base_nodes = self.template_1.nodes.all()

        # test level 2
        self.assertIn(self.node_2_1, nodes)
        self.assertIn(self.node_2_2, nodes)

        for node in base_nodes:
            self.assertIn(node, nodes)

        self.assertEqual(len(nodes), len(base_nodes) + 2)

    def test_morphing_node_with_same_code(self):
        """
        Test morphing nodes using template inheritance and manual backwards setting.


        Test #1:
            * 1 level backward.
            * Same code.

        Test #2:
            * 2 levels backward.
            * Same code.
        """

        backward = self.node_1_2_1
        backward_code = backward.code
        node_2_3 = TemplateNode.objects.create(
            name=backward.name + "'s future",
            code=backward_code,
            parent=backward.parent,
            direction=backward.direction
        )
        TemplateNodeRelation.objects.get(
            template=self.template_2,
            node=backward
        ).delete()
        TemplateNodeRelation.objects.create(
            template=self.template_2,
            node=node_2_3
        )
        node_2_3.backwards.add(backward)

        backward = self.base.nodes.all()[0]
        backward_code = backward.code
        node_2_4 = TemplateNode.objects.create(
            name=backward.name + "'s future",
            code=backward_code,
            parent=backward.parent,
            direction=backward.direction
        )
        TemplateNodeRelation.objects.get(
            template=self.template_2,
            node=backward
        ).delete()
        TemplateNodeRelation.objects.create(
            template=self.template_2,
            node=node_2_4
        )
        node_2_4.backwards.add(backward)

        # create new budget based on tempalte_2
        entity = EntityFactory.create()

        budget = Budget.objects.create(
            entity=entity,
            template=self.template_2,
            period_start=date(2013, 1, 1),
            period_end=date(2013, 12, 31)
        )

        # create 2 nodes on template_2 with backward nodes
        item_1 = BudgetItem.objects.create(
            budget=budget,
            node=node_2_3,
            amount=500
        )
        item_1_past = BudgetItem.objects.create(
            budget=budget,
            node=self.node_1_2_1,
            amount=1500
        )
        item_2 = BudgetItem.objects.create(
            budget=budget,
            node=node_2_4,
            amount=1000
        )
        item_2_past = BudgetItem.objects.create(
            budget=budget,
            node=backward,
            amount=2000
        )

        items = BudgetItem.objects.filter(node__in=node_2_3.with_past)

        self.assertIn(item_1, items)
        self.assertIn(item_1_past, items)

        items = BudgetItem.objects.filter(node__in=node_2_4.with_past)

        self.assertIn(item_2, items)
        self.assertIn(item_2_past, items)


class TemplateViewTestCase(TestCase):

    def setUp(self):
        self.divisions = DomainDivisionFactory.create_batch(3)
        self.template = BudgetTemplateFactory.create(
            divisions=self.divisions
        )

    def test_template_listview(self):

        listview = reverse('template_list')
        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_template_detailview(self):

        detailview = reverse('template_detail',
            args=(self.template.uuid,)
        )
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)

class SheetViewTestCase(TestCase):

    def setUp(self):
        self.budget = BudgetFactory.create()
        self.actual = ActualFactory.create()

    def test_budget_listview(self):

        listview = reverse('budget_list')
        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_actual_listview(self):

        listview = reverse('actual_list')
        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_budget_detailview(self):

        detailview = reverse('budget_detail',
            args=(self.budget.uuid,)
        )
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)

    def test_actual_detailview(self):

        detailview = reverse('actual_detail',
            args=(self.actual.uuid,)
        )
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)

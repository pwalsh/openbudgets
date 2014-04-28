

def mock_db(amount):

    """Builds out a complete database with mock objects.

    Useful for quick testing. Commonly invoked via the `fab mock` command.

    """

    from django.conf import settings
    from django.core.management import call_command
    from openbudgets.apps.accounts.factories import *
    from openbudgets.apps.contexts.factories import *
    from openbudgets.apps.entities.factories import *
    from openbudgets.apps.interactions.factories import *
    from openbudgets.apps.pages.factories import *
    from openbudgets.apps.sheets.factories import *
    from openbudgets.apps.sources.factories import *
    #from openbudgets.apps.taxonomies.factories import *
    from openbudgets.apps.tools.factories import *

    amount = int(amount)

    call_command('loaddata', 'tools')
    domain = Domain.create(name='Example Domain')
    division1 = Division.create(name='Example Division', domain=domain, budgeting=True, index=1)
    division2 = Division.create(name='Example Division2', domain=domain, budgeting=False, index=2)
    division3 = Division.create(name='Example Division3', domain=domain, budgeting=True, index=3)
    entity1 = Entity.create(division=division1)
    entity2 = Entity.create(division=division2)
    entities = Entity.create_batch(3, division=division3, parent=entity2)
    blueprint_template = Template.create(name='Example Blueprint Template', divisions=[division3])
    blueprint_template_nodes = TemplateNode.create_batch(amount)

    for node in blueprint_template_nodes:
        TemplateNodeRelation.create(template=blueprint_template, node=node)
        child_nodes = TemplateNode.create_batch(2, parent=node)

        for child_node in child_nodes:
            TemplateNodeRelation.create(node=child_node, template=blueprint_template)
            child_child_nodes = TemplateNode.create_batch(2, parent=child_node)

        for child_child_node in child_child_nodes:
            TemplateNodeRelation.create(node=child_child_node, template=blueprint_template)

    for entity in entities:
        Context.create(entity=entity)
        sheet1 = Sheet.create(entity=entity, template=blueprint_template,
                              period_start=datetime.date(2007, 1, 1), period_end=datetime.date(2007, 12, 31))
        for node in blueprint_template.nodes.all():
            parent = None
            if node.parent and node.parent.items.all():
                parent = node.parent.items.filter(sheet__template=sheet1.template)[0]
            SheetItem.create(sheet=sheet1, node=node, parent=parent)

        sheet2 = Sheet.create(entity=entity, template=blueprint_template,
                              period_start=datetime.date(2008, 1, 1), period_end=datetime.date(2008, 12, 31))
        for node in blueprint_template.nodes.all():
            parent = None
            if node.parent and node.parent.items.all():
                parent = node.parent.items.filter(sheet__template=sheet1.template)[0]
            SheetItem.create(sheet=sheet2, node=node, parent=parent)

        sheet3 = Sheet.create(entity=entity, template=blueprint_template,
                              period_start=datetime.date(2009, 1, 1), period_end=datetime.date(2009, 12, 31))
        for node in blueprint_template.nodes.all():
            parent = None
            if node.parent and node.parent.items.all():
                parent = node.parent.items.filter(sheet__template=sheet1.template)[0]
            SheetItem.create(sheet=sheet3, node=node, parent=parent)

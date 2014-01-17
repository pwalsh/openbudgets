from quilt import *
from dock.fabfile import *
from fabric.api import task, env, execute, roles
from fabric import operations
from fabric.contrib import django
django.project('openbudgets')
from django.core.management import call_command
from openbudgets.apps.entities.factories import *
from openbudgets.apps.sheets.factories import *


@roles('app')
@task
def mock(amount=300):
    utilities.notify(u'Creating some mock objects for the database.')
    mock_db(amount)


@roles('db')
@task
def db_put():
    utilities.notify(u'Loading a local db dump to the remote dump location.')

    execute(remote.db.rebuild)

    operations.put('/Users/paulwalsh/Sites/projects/openbudgets/tmp/db_dump.sql',
                   '/srv/projects/openbudgets/tmp/db_dump.sql')


def mock_db(amount):

    """Builds out a complete database with mock objects.

    Useful for quick testing. Commonly invoked via the `fab mock` command.

    """

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

    utilities.notify(u'Adding blueprint nodes.')
    for node in blueprint_template_nodes:
        TemplateNodeRelation.create(template=blueprint_template, node=node)
        child_nodes = TemplateNode.create_batch(2, parent=node)

        for child_node in child_nodes:
            TemplateNodeRelation.create(node=child_node, template=blueprint_template)
            child_child_nodes = TemplateNode.create_batch(2, parent=child_node)

        for child_child_node in child_child_nodes:
            TemplateNodeRelation.create(node=child_child_node, template=blueprint_template)

    utilities.notify(u'Adding sheets.')
    for entity in entities:
        sheet1 = Sheet.create(entity=entity, template=blueprint_template,
                              period_start=datetime.date(2007, 1, 1), period_end=datetime.date(2007, 12, 31))
        for node in blueprint_template.nodes.all():
            SheetItem.create(sheet=sheet1, node=node)

        sheet2 = Sheet.create(entity=entity, template=blueprint_template,
                              period_start=datetime.date(2008, 1, 1), period_end=datetime.date(2008, 12, 31))
        for node in blueprint_template.nodes.all():
            SheetItem.create(sheet=sheet2, node=node)

        sheet3 = Sheet.create(entity=entity, template=blueprint_template,
                              period_start=datetime.date(2009, 1, 1), period_end=datetime.date(2009, 12, 31))
        for node in blueprint_template.nodes.all():
            SheetItem.create(sheet=sheet3, node=node)

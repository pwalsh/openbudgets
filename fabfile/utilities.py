import os
import sys
from fabric.api import puts
from fabric.colors import red, green, yellow
from fabric.contrib import django
from django.core.management import call_command
from fabfile.config import CONFIG

django.project('openbudgets')
from openbudgets.apps.entities.factories import *
from openbudgets.apps.sheets.factories import *


SUCCESS_PREFIX = u'Good! '
ERROR_PREFIX = u'Oh Noes! '


def notify(msg):
    return puts(green(msg))


def warn(msg):
    return puts(yellow(msg))


def alert(msg):
    return puts(red(msg))


# This which function is copied from twisted.
# http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.1.0/twisted/python/procutils.py
def which(name, flags=os.X_OK):
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    if result:
        notify(SUCCESS_PREFIX + name + u' is installed.')
    else:
        notify(ERROR_PREFIX + name + u' is not installed.')


def check_postgres_user(username=CONFIG['db_user']):
    #TODO: check exists, and check has createdb perms
    pass

def sanity_check():

    # Ensure we are in an active virtualenv
    if hasattr(sys, 'real_prefix'):
        notify(SUCCESS_PREFIX + u'You have an activated virtual environment.')
    else:
        alert(ERROR_PREFIX + u'There is no active virtual environment. '
                             u'Please ensure that you have created a virtual '
                             u'environment for the project, and that you have '
                             u'activated the virtual environment.')

    # Ensure we have the minimum system requirements
    which('python')
    which('fab')
    which('pip')
    which('virtualenv')
    which('psql')
    which('git')
    which('hg')
    which('redis-server')
    #which('node')
    #which('npm')
    #which('volo')

    # Check the Postgresql user exists and is configured as required
    #check_postgres_user()


def mock_db(amount):
    """Builds out a complete database with mock objects.

    Useful for quick testing. Commonly invoked via the `fab mock` command.

    """

    domain = Domain.create(name='Example Domain')
    division = Division.create(name='Example Division', domain=domain, index=3)
    entities = Entity.create_batch(2, division=division)
    template = Template.create(name='Example Template', divisions=[division])
    template_nodes = TemplateNode.create_batch(amount)
    call_command('loaddata', 'tools')

    for node in template_nodes:
        TemplateNodeRelation.create(node=node, template=template)
        child_nodes = TemplateNode.create_batch(2, parent=node)
        for node in child_nodes:
            TemplateNodeRelation.create(node=node, template=template)

    for entity in entities:
        sheet = Sheet.create(entity=entity, template=template)
        for node in template.nodes.all():
            SheetItem.create(sheet=sheet, node=node)

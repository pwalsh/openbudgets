from django.core import management
from celery.task import task


@task(name='tasks.update_index')
def update_index():
    management.call_command(
        'update_index',
        verbosity=0,
        interactive=False
    )


@task(name='tasks.rebuild_index')
def rebuild_index():
    management.call_command(
        'rebuild_index',
        verbosity=0,
        interactive=False
    )

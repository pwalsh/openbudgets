import cuisine
from fabric.api import task, roles, sudo
from fabfile import templates
from fabfile.utilities import notify
from fabfile.config import CONFIG


@task
@roles('web')
def start():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl start ' + CONFIG['project_name'] + '-gunicorn')
    sudo('supervisorctl start ' + CONFIG['project_name'] + '-celery')


@task
@roles('web')
def stop():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl stop ' + CONFIG['project_name'] + '-gunicorn')
    sudo('supervisorctl stop ' + CONFIG['project_name'] + '-celery')


@task
@roles('web')
def restart():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl restart ' + CONFIG['project_name'] + '-gunicorn')
    sudo('supervisorctl restart ' + CONFIG['project_name'] + '-celery')


@task
@roles('web')
def nginx():
    notify('Configuring nginx.')
    context = CONFIG
    context.update({'domain_names': ' '.join(CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/open-budgets', content)
    sudo('service nginx restart')


@task
@roles('web')
def gunicorn():
    notify('Configuring gunicorn.')
    context = CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn_upstart, context)
    cuisine.file_write('/etc/init/gunicorn.conf', content)
    restart()


#@task
#@roles('web')
#def celery():
#    notify('Configuring celery.')
#    context = {
#        'ACTION_DATE': MACHINE['ACTION_DATE'],
#        'NAME': PROJECT['NAME'],
#        'KEY': KEY,
#        'CONCURRENCY': PROJECT['CELERY_CONCURRENCY'],
#        'MAX_TASKS_PER_CHILD': PROJECT['CELERY_MAX_TASKS_PER_CHILD'],
#        'PROJECT_ROOT': PROJECT['ROOT'],
#        'PROJECT_ENV': PROJECT['ENV'],
#        'ACCESS_LOG': PROJECT['LOGS']['CELERY'],
#   }
#
#    cuisine.mode_sudo()
#    content = cuisine.text_template(templates.celery_supervisor, context)
#    cuisine.file_write('/etc/supervisor/conf.d/' + KEY + '-celery.conf', content)
#    restart()

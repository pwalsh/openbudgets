import cuisine
from fabric.api import task, roles, sudo
from fabfile import templates
from fabfile.utilities import notify
from fabfile.config import CONFIG


@task
@roles('demo')
def start():
    sudo('service ' + CONFIG['project_name'] + ' start')


@task
@roles('demo')
def stop():
    sudo('service ' + CONFIG['project_name'] + ' stop')


@task
@roles('demo')
def restart():
    sudo('service ' + CONFIG['project_name'] + ' restart')


@task
@roles('demo')
def nginx():
    notify('Configuring nginx.')
    context = CONFIG
    context.update({'domain_names': ' '.join(CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + CONFIG['project_name'], content)
    sudo('service nginx restart')


@task
@roles('demo')
def gunicorn():
    notify('Configuring gunicorn.')
    context = CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn, context)
    cuisine.file_write('/etc/init/' + CONFIG['project_name'] + '.conf', content)
    restart()

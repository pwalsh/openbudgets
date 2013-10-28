import cuisine
from fabric.api import task, roles, run, sudo, cd, local
from fabric.contrib.files import uncomment
from utilities import notify
from config import CONFIG
import templates


# FOR DEPLOYMENT TO GOOGLE COMPUTE ENGINE, SET UP FIREWALLS ON THE NETWORK
# create a static IP address (done via web console)
# gcutil addnetwork openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-ssh --allowed=:22 --network=openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-http --allowed=tcp:80 --network=openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-https --allowed=:443 --network=openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-mail --allowed=:587 --network=openmuni-budgets --project=open-municipalities
# gcutil addinstance openmuni-budgets-v1 --network=openmuni-budgets --project=open-municipalities --persistent_boot_disk --zone=europe-west1-b --external_ip_address=8.34.222.255 --machine_type=n1-standard-1-d --ssh_user=robot --image=projects/debian-cloud/global/images/debian-7-wheezy-v20130926
# gcutil deleteinstance openmuni-budgets --project=open-municipalities

# SSH IN
# gcutil --project=open-municipalities --network=openmuni-budgets --zone=europe-west1-b ssh openmuni-budgets-v1

# then:
# install salt:


#@task
#@roles('web')
#def bootstrap():
#    notify('Configuring the server.')
#    tz_conf()
#    locale_conf()
#    apt_update()
#    apt_upgrade()
#    hosts_conf()
#    dir_conf()
#    package_conf()
#    nonmanaged_package_conf()
#    python_package_conf()
#    node_module_conf()
#    profile_conf()
#    #firewall_conf()
#    link_conf()
#    reboot()

@task
@roles('web')
def apt_update():
    sudo('apt-get update')


def apt_upgrade():
    sudo('apt-get upgrade')


#def tz_conf():
#    notify('Configuring timezone defaults.')
#    sudo('echo "Etc/UTC" > /etc/timezone')
#    sudo('dpkg-reconfigure -f noninteractive tzdata')
#
#
#def locale_conf():
#    notify('Configuring locale defaults.')
#    sudo('locale-gen --purge en_US.UTF-8')
#    sudo('echo -e "LANG=\'en_US.UTF-8\'\nLANGUAGE=\'en_US:en\'\n" > /etc/default/locale')
#    sudo('dpkg-reconfigure -f noninteractive locales')
#
#
#def hosts_conf():
#    notify('Writing hostname and hosts files.')
#    cuisine.mode_sudo()
#    run('echo "{NAME}" > /etc/hostname'.format(NAME=MACHINE['KEY']))
#    run('hostname -F /etc/hostname')
#    hosts = cuisine.text_template(templates.hosts, MACHINE)
#    cuisine.file_append('/etc/hosts', hosts)
#
#
#def dir_conf():
#    notify('Creating the working directory structure.')
#    cuisine.mode_sudo()
#    cuisine.dir_ensure(MACHINE['DIR_WORKSPACE'])
#    cuisine.dir_ensure(MACHINE['DIR_ENVIRONMENTS'], recursive=True, mode=MACHINE['DIR_MODE'],
#                       owner=KEY, group=MACHINE['OWNER_GROUP'])
#    cuisine.dir_ensure(MACHINE['DIR_PROJECTS'], recursive=True, mode=MACHINE['DIR_MODE'],
#                       owner=KEY, group=MACHINE['OWNER_GROUP'])
#    cuisine.dir_ensure(MACHINE['DIR_SSL'], recursive=True, mode=MACHINE['DIR_MODE'],
#                       owner=KEY, group=MACHINE['OWNER_GROUP'])
#    cuisine.dir_ensure(MACHINE['DIR_LOGS'], recursive=True, mode=MACHINE['DIR_MODE'],
#                       owner=KEY, group=MACHINE['OWNER_GROUP'])
#
#
#def package_conf(databases=MACHINE['DATABASES']):
#    notify('Installing all required system packages.')
#    #package_ensure('ufw')
#    cuisine.package_ensure('supervisor')
#    cuisine.package_ensure('python-dev')
#    cuisine.package_ensure('python-setuptools')
#    cuisine.package_ensure('python-software-properties')
#    cuisine.package_ensure('g++')
#    cuisine.package_ensure('make')
#    cuisine.package_ensure('build-essential')
#    cuisine.package_ensure('checkinstall')
#    cuisine.package_ensure('libxml2-dev')
#    cuisine.package_ensure('libjpeg8-dev')
#    cuisine.package_ensure('libpng-dev')
#    cuisine.package_ensure('zlib1g-dev')
#    cuisine.package_ensure('libfreetype6-dev')
#    cuisine.package_ensure('liblcms1-dev')
#    cuisine.package_ensure('python')
#    cuisine.package_ensure('python-pip')
#    cuisine.package_ensure('nginx')
#    cuisine.package_ensure('git-core')
#    cuisine.package_ensure('mercurial')
#
#    if databases:
#        if 'postgres' in databases:
#            cuisine.package_ensure('postgresql')
#            cuisine.package_ensure('postgresql-contrib')
#            cuisine.package_ensure('postgresql-server-dev-all')
#            # Not working, do manually
#            #postgres_conf()
#
#        if 'redis' in databases:
#            cuisine.package_ensure('redis-server')
#
#
#def nonmanaged_package_conf():
#    notify('Installing additional non-managed packages.')
#    # NODE.JS
#    #
#    #
#    # IMPORTANT: REQUIRES YOU TO RESET THE VERSION NUMBER WITHOUT A "v"
#    # during install.
#    #
#    #
#    notify('Installing node.js')
#    cuisine.mode_sudo()
#    cuisine.dir_ensure(MACHINE['DIR_USER_HOME'])
#    with cd(MACHINE['DIR_USER_HOME']):
#        sudo('wget -N http://nodejs.org/dist/node-latest.tar.gz')
#        sudo('tar xzvf node-latest.tar.gz')
#        with cd('node-v*'):
#            sudo('./configure')
#            sudo('checkinstall')
#            sudo('sudo dpkg -i node_*')
#
#
#def python_package_conf():
#    notify('Installing required system python packages.')
#    cuisine.mode_sudo()
#    cuisine.python_package_ensure('virtualenv')
#    cuisine.python_package_ensure('virtualenvwrapper')
#
#
#def node_module_conf():
#    notify('Installing required system node modules.')
#    cuisine.mode_sudo()
#    sudo('npm install -g volo')
#
#
#def postgres_conf():
#    uncomment('/etc/postgresql/9.1/main/postgresql.conf', 'listen_addresses',
#              use_sudo=True, char='#', backup='.bak')
#    sudo('passwd postgres')
#    with sudo('su - postgres'):
#        run('psql')
#        run('CREATE EXTENSION adminpack;')
#        #
#        # get out of postgresq shell here
#        #
#        run('createuser ' + KEY)
#        run('exit')
#        run('createdb ' + KEY)
#
#
#@task
#@roles('web')
#def profile_conf():
#    notify('Configuring .profile settings.')
#    profile = cuisine.text_template(templates.profile, MACHINE)
#    cuisine.file_append(MACHINE['OWNER_PROFILE'], profile)
#    run('source ' + MACHINE['OWNER_PROFILE'])
#
#
#def firewall_conf():
#    sudo('ufw default deny')
#    sudo('ufw allow 80')
#    sudo('ufw allow 443')
#    sudo('ufw allow 587')
#    sudo('ufw enable')
#
#
#def link_conf():
#    notify('Configuring necessary symlinks for our libraries.')
#    cuisine.mode_sudo()
#    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libjpeg.so', '/usr/lib/libjpeg.so', symbolic=True)
#    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libpng.so', '/usr/lib/libpng.so', symbolic=True)
#    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libz.so', '/usr/lib/libz.so', symbolic=True)
#    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libfreetype.so', '/usr/lib/libfreetype.so', symbolic=True)
#    cuisine.file_link('/usr/lib/x86_64-linux-gnu/liblcms.so', '/usr/lib/liblcms.so', symbolic=True)
#
#
#def reboot():
#    sudo('reboot')




@task
@roles('demo')
def start():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl start ' + CONFIG['project_name'] + '-gunicorn')
    sudo('supervisorctl start ' + CONFIG['project_name'] + '-celery')


@task
@roles('demo')
def stop():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl stop ' + CONFIG['project_name'] + '-gunicorn')
    sudo('supervisorctl stop ' + CONFIG['project_name'] + '-celery')


@task
@roles('demo')
def restart():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl restart ' + CONFIG['project_name'] + '-gunicorn')
    sudo('supervisorctl restart ' + CONFIG['project_name'] + '-celery')


@task
@roles('demo')
def nginx():
    notify('Configuring nginx.')
    context = CONFIG
    context.update({'domain_names': ' '.join(CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/open-budgets', content)
    sudo('service nginx restart')


@task
@roles('demo')
def gunicorn():
    notify('Configuring gunicorn.')
    context = CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn_upstart, context)
    cuisine.file_write('/etc/init/gunicorn.conf', content)
    restart()


#@task
#@roles('demo')
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







gunicorn_supervisor = """; Generated via Fabric on ${ACTION_DATE}
; gunicorn configuration for ${NAME}
; usually would pass logs on gunicorn, but it errors:
; --access-logfile ${ACCESS_LOG} --error-logfile ${ERROR_LOG}

[program:${KEY}-gunicorn]

command=${PROJECT_ENV}/bin/gunicorn --bind ${APP_LOCATION}:${APP_PORT} --timeout ${APP_TIMEOUT} --workers ${APP_WORKERS} ${APP_WSGI}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${KEY}
redirect_stderr=true
autostart=true
autorestart=true
"""


celery_supervisor = """### Generated via Fabric on ${ACTION_DATE}
# celery configuration for ${NAME}
[program:${KEY}-celery]

command=${PROJECT_ENV}/bin/python manage.py celery worker --concurrency=${CONCURRENCY} --maxtasksperchild=${MAX_TASKS_PER_CHILD} --logfile=${ACCESS_LOG}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${KEY}
redirect_stderr=true
autostart=true
autorestart=true
"""


import cuisine
from fabric.api import env, task, roles, run, sudo, cd
from fabric.contrib.files import uncomment
from fabfile.utilities import notify
from fabfile.config import CONFIG
from fabfile import templates


# override the base CONFIG object that is used for the demo instance
env.user = 'paulwalsh'
env.key_filename = '~/.ssh/google_compute_engine'

CONFIG['project_name'] = 'openmuni-budgets'
CONFIG['machine_location'] = env.roledefs['openmuni-budgets'][0]
CONFIG['allowed_hosts'] = ['openmuni.org.il', 'en.openmuni.org.il', 'he.openmuni.org.il',
                           'ar.openmuni.org.il', 'ru.openmuni.org.il']
CONFIG['cookie_domain'] = '.openmuni.org.il'

# extras, for machine setup
CONFIG['OWNER_GROUP'] = 'www-data'
CONFIG['OWNER_USER'] = env.user
CONFIG['OWNER_PROFILE'] = '/home/' + env.user + '/.profile'
CONFIG['DIR_USER_HOME'] = '/home/' + env.user
CONFIG['DIR_MODE'] = 'g+s'
CONFIG['DIR_WORKSPACE'] = '/srv'
CONFIG['DIR_ENVIRONMENTS'] = '/srv/environments'
CONFIG['DIR_PROJECTS'] = '/srv/projects'
CONFIG['DIR_SSL'] = '/srv/ssl'
CONFIG['DIR_LOGS'] = '/srv/logs'


########################## GOOGLE COMPUTE ENGINE ############################

# create a static IP address (done via web console)

# gcutil addnetwork openmuni-budgets --project=open-municipalities

# gcutil addfirewall openmuni-budgets-ssh --allowed=:22 --network=openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-http --allowed=tcp:80 --network=openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-https --allowed=:443 --network=openmuni-budgets --project=open-municipalities
# gcutil addfirewall openmuni-budgets-mail --allowed=:587 --network=openmuni-budgets --project=open-municipalities

# gcutil addinstance openmuni-budgets-v1 --network=openmuni-budgets --project=open-municipalities --persistent_boot_disk --zone=europe-west1-b --external_ip_address=8.34.222.255 --machine_type=n1-standard-1-d --ssh_user=robot --image=projects/debian-cloud/global/images/debian-7-wheezy-v20130926
# gcutil --ssh_user=robot ssh openmuni-budgets-v1

# gcutil deleteinstance openmuni-budgets --project=open-municipalities

# SSH IN
# gcutil --project=open-municipalities --network=openmuni-budgets --zone=europe-west1-b ssh openmuni-budgets-v1

###########################################################################


@task
@roles('openmuni-budgets')
def bootstrap():
    notify('Configuring the server.')
    tz_conf()
    locale_conf()
    apt_update()
    apt_upgrade()
    hosts_conf()
    dir_conf()
    package_conf()
    python_package_conf()
    profile_conf()
    link_conf()
    reboot()


@task
@roles('openmuni-budgets')
def tz_conf():
    notify('Configuring timezone defaults.')
    sudo('echo "Etc/UTC" > /etc/timezone')
    sudo('dpkg-reconfigure -f noninteractive tzdata')


@task
@roles('openmuni-budgets')
def locale_conf():
    notify('Configuring locale defaults.')
    sudo('locale-gen --purge en_US.UTF-8')
    sudo('echo -e "LANG=\'en_US.UTF-8\'\nLANGUAGE=\'en_US:en\'\n" > /etc/default/locale')
    sudo('dpkg-reconfigure -f noninteractive locales')


@task
@roles('openmuni-budgets')
def apt_update():
    sudo('apt-get update')


@task
@roles('openmuni-budgets')
def apt_upgrade():
    sudo('apt-get upgrade')


@task
@roles('openmuni-budgets')
def hosts_conf():
    notify('Writing hostname and hosts files.')
    cuisine.mode_sudo()
    run('echo "{NAME}" > /etc/hostname'.format(NAME=CONFIG['project_name']))
    run('hostname -F /etc/hostname')
    hosts = cuisine.text_template(templates.hosts, CONFIG)
    cuisine.file_append('/etc/hosts', hosts)


@task
@roles('openmuni-budgets')
def dir_conf():
    notify('Creating the working directory structure.')
    cuisine.mode_sudo()
    cuisine.dir_ensure(CONFIG['DIR_WORKSPACE'])
    cuisine.dir_ensure(CONFIG['DIR_ENVIRONMENTS'], recursive=True, mode=CONFIG['DIR_MODE'],
                       owner=CONFIG['user'], group=CONFIG['OWNER_GROUP'])
    cuisine.dir_ensure(CONFIG['DIR_PROJECTS'], recursive=True, mode=CONFIG['DIR_MODE'],
                       owner=CONFIG['user'], group=CONFIG['OWNER_GROUP'])
    cuisine.dir_ensure(CONFIG['DIR_SSL'], recursive=True, mode=CONFIG['DIR_MODE'],
                       owner=CONFIG['user'], group=CONFIG['OWNER_GROUP'])
    cuisine.dir_ensure(CONFIG['DIR_LOGS'], recursive=True, mode=CONFIG['DIR_MODE'],
                       owner=CONFIG['user'], group=CONFIG['OWNER_GROUP'])


@task
@roles('openmuni-budgets')
def package_conf():
    notify('Installing all required system packages.')
    cuisine.package_ensure('supervisor')
    cuisine.package_ensure('python-dev')
    cuisine.package_ensure('python-setuptools')
    cuisine.package_ensure('python-software-properties')
    cuisine.package_ensure('g++')
    cuisine.package_ensure('make')
    cuisine.package_ensure('build-essential')
    cuisine.package_ensure('checkinstall')
    cuisine.package_ensure('libxml2-dev')
    cuisine.package_ensure('libjpeg8-dev')
    cuisine.package_ensure('libpng-dev')
    cuisine.package_ensure('zlib1g-dev')
    cuisine.package_ensure('libfreetype6-dev')
    cuisine.package_ensure('liblcms1-dev')
    cuisine.package_ensure('python')
    cuisine.package_ensure('python-pip')
    cuisine.package_ensure('nginx')
    cuisine.package_ensure('git-core')
    cuisine.package_ensure('mercurial')
    cuisine.package_ensure('postgresql')
    cuisine.package_ensure('postgresql-contrib')
    cuisine.package_ensure('postgresql-server-dev-all')
    cuisine.package_ensure('redis-server')
    # Not working, do manually
    #postgres_conf()


@task
@roles('openmuni-budgets')
def python_package_conf():
    notify('Installing required system python packages.')
    cuisine.mode_sudo()
    cuisine.python_package_ensure('virtualenv')
    cuisine.python_package_ensure('virtualenvwrapper')


@task
@roles('openmuni-budgets')
def postgres_conf():
    uncomment('/etc/postgresql/9.1/main/postgresql.conf', 'listen_addresses',
              use_sudo=True, char='#', backup='.bak')
    sudo('passwd postgres')
    with sudo('su - postgres'):
        run('psql')
        run('CREATE EXTENSION adminpack;')
        #
        # get out of postgresq shell here
        #
        run('createuser ' + CONFIG['user'])
        run('exit')
        run('createdb ' + CONFIG['db_name'])


@task
@roles('openmuni-budgets')
def profile_conf():
    notify('Configuring .profile settings.')
    profile = cuisine.text_template(profile, CONFIG)
    cuisine.file_append(CONFIG['OWNER_PROFILE'], profile)
    run('source ' + CONFIG['OWNER_PROFILE'])


@task
@roles('openmuni-budgets')
def link_conf():
    notify('Configuring necessary symlinks for our libraries.')
    cuisine.mode_sudo()
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libjpeg.so', '/usr/lib/libjpeg.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libpng.so', '/usr/lib/libpng.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libz.so', '/usr/lib/libz.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libfreetype.so', '/usr/lib/libfreetype.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/liblcms.so', '/usr/lib/liblcms.so', symbolic=True)


@task
@roles('openmuni-budgets')
def reboot():
    sudo('reboot')


@task
@roles('openmuni-budgets')
def start():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl start ' + CONFIG['project_name'])
    sudo('supervisorctl start ' + CONFIG['project_name'] + 'q')


@task
@roles('openmuni-budgets')
def stop():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl stop ' + CONFIG['project_name'])
    sudo('supervisorctl stop ' + CONFIG['project_name'] + 'q')


@task
@roles('openmuni-budgets')
def restart():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl restart ' + CONFIG['project_name'])
    sudo('supervisorctl restart ' + CONFIG['project_name'] + 'q')


@task
@roles('openmuni-budgets')
def nginx():
    notify('Configuring nginx.')
    context = CONFIG
    context.update({'domain_names': ' '.join(CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + CONFIG['project_name'], content)
    sudo('service nginx restart')


#@task
#@roles('openmuni-budgets')
#def gunicorn():
#    notify('Configuring gunicorn.')
#    context = CONFIG
#    cuisine.mode_sudo()
#    content = cuisine.text_template(gunicorn_supervisor, context)
#    cuisine.file_write('/etc/init/gunicorn.conf', content)
#    restart()


@task
@roles('openmuni-budgets')
def celery():
    notify('Configuring celery.')
    cuisine.mode_sudo()
    content = cuisine.text_template(celery_supervisor, CONFIG)
    cuisine.file_write('/etc/supervisor/conf.d/' + CONFIG['project_name'] + 'q.conf', content)
    restart()


hosts = """### Generated via Fabric on ${timestamp}
# hosts configuration for ${project_name}
${machine_Location} ${project_name}
"""


profile = """### Generated via Fabric on ${timestamp}
# .profile configuration for ${project_name}
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export EDITOR=nano
export PYTHONIOENCODING=utf-8
export WORKON_HOME=${DIR_ENVIRONMENTS}
export PROJECT_HOME=${DIR_PROJECTS}
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
export PIP_USE_MIRRORS=true
export PIP_INDEX_URL=https://simple.crate.io/
"""


gunicorn_supervisor = """; Generated via Fabric on ${timestamp}
; gunicorn configuration for ${project_name}
; usually would pass logs on gunicorn, but it errors:
; --access-logfile ${ACCESS_LOG} --error-logfile ${ERROR_LOG}

[program:${project_name}]

command=${PROJECT_ENV}/bin/gunicorn --bind ${app_location}:${app_port} --timeout ${app_timeout} --workers ${app_workers} ${app_wsgi}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${user}
redirect_stderr=true
autostart=true
autorestart=true
"""


celery_supervisor = """### Generated via Fabric on ${timestamp}
# celery configuration for ${project_name}
[program:${project_name}q]

command=${PROJECT_ENV}/bin/python manage.py celery worker --concurrency=${queue_workers} --maxtasksperchild=${queue_max_tasks_per_child} --logfile=${queue_log}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${user}
redirect_stderr=true
autostart=true
autorestart=true
"""

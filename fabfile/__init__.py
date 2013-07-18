import datetime
from fabric.api import *
from fabric.colors import green, red
from fabric.contrib.files import uncomment
from cuisine import *
from . import templates


env.use_ssh_config = True
env.forward_agent = True
env.user = 'omuni'
env.roledefs = {
    'web': ['192.158.30.219']
}

####### HERE IS THE CURRENT SETUP ON COMPUTE ENGINE
#####
###
##
#

# gcutil addinstance omuni --project=open-municipalities --persistent_boot_disk --zone=europe-west1-a --external_ip_address=192.158.30.219 --machine_type=n1-standard-1 --ssh_user=omuni --image=projects/debian-cloud/global/images/debian-7-wheezy-v20130617

# gcutil addfirewall http-web --allowed=tcp:80 --project=open-municipalities
# gcutil addfirewall https-web --allowed=:443 --project=open-municipalities

# gcutil deleteinstance omuni --project=open-municipalities


###### SOME MANUAL MACHINE SETUP STILL...
#####
###
##
#

# 1. run the machine_bootstrap task (have a couple of questions to answer via prompts). It is CRITICAL to
# change the version number on the node install to be the same, WITHOUT the v prepended. pay attention.

# 2. manual setup of postgres user etc.


KEY = env.user


MACHINE = {
    'LOCATION': env.roledefs['web'][0],
    'PORT': 80,
    'NAME': 'Open Muni Budgets',
    'KEY': KEY,
    'OWNER_GROUP': 'www-data',
    'OWNER_USER': env.user,
    'OWNER_PROFILE': '/home/' + env.user + '/.profile',
    'DIR_USER_HOME': '/home/' + env.user,
    'DIR_MODE': 'g+s',
    'DIR_WORKSPACE': '/srv',
    'DIR_ENVIRONMENTS': '/srv/environments',
    'DIR_PROJECTS': '/srv/projects',
    'DIR_SSL': '/srv/ssl',
    'DIR_LOGS': '/srv/logs',
    'DATABASES': ['postgres', 'redis'],
    'ACTION_DATE': datetime.datetime.now()
}


PROJECT = {
    'APP_LOCATION': '127.0.0.1',
    'APP_PORT': 9999,
    'APP_WORKERS': 4,
    'CELERY_CONCURRENCY': 1,
    'CELERY_MAX_TASKS_PER_CHILD': 10,
    'APP_WSGI': 'openbudget.wsgi:application',
    'NAME': MACHINE['NAME'],
    'KEY': KEY,
    'DOMAINS': ['dev.openmuni.org.il', 'api.dev.openmuni.org.il',
                'en.dev.openmuni.org.il', 'he.dev.openmuni.org.il',
                'ar.dev.openmuni.org.il', 'ru.dev.openmuni.org.il'],
    'REPO': 'https://github.com/hasadna/omuni-budget',
    'DEFAULT_BRANCH': 'develop',
    'ROOT': MACHINE['DIR_PROJECTS'] + '/' + KEY,
    'ENV': MACHINE['DIR_ENVIRONMENTS'] + '/' + KEY,
    'WORKON': 'workon ' + KEY,
    'DEACTIVATE': 'deactivate',
    'MAKE_ENV': 'mkvirtualenv ' + KEY,
    'SET_ENV': 'setvirtualenvproject ' + MACHINE['DIR_ENVIRONMENTS'] + '/' +
               KEY + ' ' + MACHINE['DIR_PROJECTS'] + '/' + KEY,
    'LOGS': {
        'NGINX_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_nginx_access.log',
        'NGINX_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_nginx_error.log',
        'GUNICORN_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_gunicorn_access.log',
        'GUNICORN_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_gunicorn_error.log',
        'CELERY': MACHINE['DIR_LOGS'] + '/' + KEY + '_celery.log',
        'REDIS_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_redis_access.log',
        'REDIS_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_redis_error.log',
    },
    'ACTION_DATE': datetime.datetime.now()
}


@task
@roles('web')
def machine_bootstrap():
    puts(green('Configuring the server.'))
    tz_conf()
    locale_conf()
    apt_update()
    apt_upgrade()
    hosts_conf()
    dir_conf()
    package_conf()
    nonmanaged_package_conf()
    python_package_conf()
    node_module_conf()
    profile_conf()
    #firewall_conf()
    link_conf()
    reboot()


@task
@roles('web')
def project_bootstrap():
    puts(green('Configuring the project.'))
    #venv_conf()
    #project_install()
    #project_requirements_install()
    #project_validate()
    #project_initialize()
    #project_restart_sequence()
    #project_nginx_conf()
    project_gunicorn_conf()
    project_celery_conf()


@task
@roles('web')
def db_load():
    puts(green('Loading data to postgres.'))
    local = '/Users/paulwalsh/Desktop/postgres.sql'
    remote = MACHINE['DIR_USER_HOME'] + '/' + KEY + '.sql'
    file_upload(remote, local)
    run('dropdb ' + KEY)
    run('createdb ' + KEY)
    run('psql ' + KEY + ' < ' + remote)


def venv_conf():
    run(PROJECT['MAKE_ENV'])
    dir_ensure(PROJECT['ROOT'])
    run(PROJECT['SET_ENV'])


def project_install():
    with prefix(PROJECT['WORKON']):
        run('git clone ' + PROJECT['REPO'] + ' .')
        run(PROJECT['DEACTIVATE'])


@task
@roles('web')
def project_requirements_install():
    with prefix(PROJECT['WORKON']):
        run('pip install -r requirements/base.txt')
        run('pip install -r requirements/deploy.txt')
        run('volo add -noprompt')
        run(PROJECT['DEACTIVATE'])


def project_restart_sequence():
    with prefix(PROJECT['WORKON']):
        run('python manage.py collectstatic')
        # restart server
        run(PROJECT['DEACTIVATE'])


def project_validate():
    with prefix(PROJECT['WORKON']):
        run('python manage.py validate')
        run(PROJECT['DEACTIVATE'])


def project_initialize():
    with prefix(PROJECT['WORKON']):
        run('python manage.py devstrap -m -t')
        run(PROJECT['DEACTIVATE'])


def project_nginx_conf():
    puts(green('Configuring nginx.'))
    context = {
        'ACTION_DATE': MACHINE['ACTION_DATE'],
        'NAME': PROJECT['NAME'],
        'KEY': KEY,
        'APP_LOCATION': PROJECT['APP_LOCATION'],
        'APP_PORT': PROJECT['APP_PORT'],
        'LOCATION': MACHINE['LOCATION'],
        'PORT': MACHINE['PORT'],
        'PROJECT_ROOT': PROJECT['ROOT'],
        'ACCESS_LOG': PROJECT['LOGS']['NGINX_ACCESS'],
        'ERROR_LOG': PROJECT['LOGS']['NGINX_ERROR'],
        'SERVER_NAMES': ' '.join(PROJECT['DOMAINS'])
    }
    mode_sudo()
    content = text_template(templates.nginx, context)
    file_write('/etc/nginx/sites-enabled/' + KEY, content)
    sudo('/etc/init.d/nginx restart')


def project_gunicorn_conf():
    puts(green('Configuring gunicorn.'))
    context = {
        'ACTION_DATE': MACHINE['ACTION_DATE'],
        'NAME': PROJECT['NAME'],
        'KEY': KEY,
        'APP_LOCATION': PROJECT['APP_LOCATION'],
        'APP_PORT': PROJECT['APP_PORT'],
        'APP_WSGI': PROJECT['APP_WSGI'],
        'APP_WORKERS': PROJECT['APP_WORKERS'],
        'LOCATION': MACHINE['LOCATION'],
        'PORT': MACHINE['PORT'],
        'PROJECT_ROOT': PROJECT['ROOT'],
        'PROJECT_ENV': PROJECT['ENV'],
        'ACCESS_LOG': PROJECT['LOGS']['GUNICORN_ACCESS'],
        'ERROR_LOG': PROJECT['LOGS']['GUNICORN_ERROR'],
    }

    mode_sudo()
    content = text_template(templates.gunicorn_supervisor, context)
    file_write('/etc/supervisor/conf.d/' + KEY + '-gunicorn.conf', content)
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl restart ' + KEY + '-gunicorn')


def project_celery_conf():
    puts(green('Configuring celery.'))
    context = {
        'ACTION_DATE': MACHINE['ACTION_DATE'],
        'NAME': PROJECT['NAME'],
        'KEY': KEY,
        'CONCURRENCY': PROJECT['CELERY_CONCURRENCY'],
        'MAX_TASKS_PER_CHILD': PROJECT['CELERY_MAX_TASKS_PER_CHILD'],
        'PROJECT_ROOT': PROJECT['ROOT'],
        'PROJECT_ENV': PROJECT['ENV'],
        'ACCESS_LOG': PROJECT['LOGS']['CELERY'],
    }

    mode_sudo()
    content = text_template(templates.celery_supervisor, context)
    file_write('/etc/supervisor/conf.d/' + KEY + '-celery.conf', content)
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl restart ' + KEY + '-celery')


######                  ######
##### MACHINE FUNCTIONS  #####
####                      ####

def apt_update():
    sudo('apt-get update')


def apt_upgrade():
    sudo('apt-get upgrade')


def tz_conf():
    puts(green('Configuring timezone defaults.'))
    sudo('echo "Etc/UTC" > /etc/timezone')
    sudo('dpkg-reconfigure -f noninteractive tzdata')


def locale_conf():
    puts(green('Configuring locale defaults.'))
    sudo('locale-gen --purge en_US.UTF-8')
    sudo('echo -e "LANG=\'en_US.UTF-8\'\nLANGUAGE=\'en_US:en\'\n" > /etc/default/locale')
    sudo('dpkg-reconfigure -f noninteractive locales')


def hosts_conf():
    puts(green('Writing hostname and hosts files.'))
    mode_sudo()
    run('echo "{NAME}" > /etc/hostname'.format(NAME=MACHINE['KEY']))
    run('hostname -F /etc/hostname')
    hosts = text_template(templates.hosts, MACHINE)
    file_append('/etc/hosts', hosts)

    # Want to do an ensure here, the current method is not good for repeated
    # runs.
    #print 'GOING TO GO IN LINES'
    #for l in hosts.splitlines():
    #    print 'LINE:'
    #    print l
    #    text_ensure_line(f, l)
    #file_write('/etc/hosts', f)


def dir_conf():
    puts(green('Creating the working directory structure.'))
    mode_sudo()
    dir_ensure(MACHINE['DIR_WORKSPACE'])
    dir_ensure(MACHINE['DIR_ENVIRONMENTS'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=env.user, group=MACHINE['OWNER_GROUP'])
    dir_ensure(MACHINE['DIR_PROJECTS'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=env.user, group=MACHINE['OWNER_GROUP'])
    dir_ensure(MACHINE['DIR_SSL'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=env.user, group=MACHINE['OWNER_GROUP'])
    dir_ensure(MACHINE['DIR_LOGS'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=env.user, group=MACHINE['OWNER_GROUP'])


def package_conf(databases=MACHINE['DATABASES']):
    puts(green('Installing all required system packages.'))
    #package_ensure('ufw')
    package_ensure('supervisor')
    package_ensure('python-dev')
    package_ensure('python-setuptools')
    package_ensure('python-software-properties')
    package_ensure('g++')
    package_ensure('make')
    package_ensure('build-essential')
    package_ensure('checkinstall')
    package_ensure('libxml2-dev')
    package_ensure('libjpeg8-dev')
    package_ensure('libpng-dev')
    package_ensure('zlib1g-dev')
    package_ensure('libfreetype6-dev')
    package_ensure('liblcms1-dev')
    package_ensure('python')
    package_ensure('python-pip')
    package_ensure('nginx')
    package_ensure('git-core')
    package_ensure('mercurial')

    if databases:
        if 'postgres' in databases:
            package_ensure('postgresql')
            package_ensure('postgresql-contrib')
            package_ensure('postgresql-server-dev-all')
            # Not working, do manually
            #postgres_conf()

        if 'redis' in databases:
            package_ensure('redis-server')


def nonmanaged_package_conf():
    puts(green('Installing additional non-managed packages.'))
    # NODE.JS
    #
    #
    # IMPORTANT: REQUIRES YOU TO RESET THE VERSION NUMBER WITHOUT A "v"
    # during install.
    #
    #
    puts(green('Installing node.js'))
    mode_sudo()
    dir_ensure(MACHINE['DIR_USER_HOME'])
    with cd(MACHINE['DIR_USER_HOME']):
        sudo('wget -N http://nodejs.org/dist/node-latest.tar.gz')
        sudo('tar xzvf node-latest.tar.gz')
        with cd('node-v*'):
            sudo('./configure')
            sudo('checkinstall')
            sudo('sudo dpkg -i node_*')


def python_package_conf():
    puts(green('Installing required system python packages.'))
    mode_sudo()
    python_package_ensure('virtualenv')
    python_package_ensure('virtualenvwrapper')


def node_module_conf():
    puts(green('Installing required system node modules.'))
    mode_sudo()
    sudo('npm install -g volo')


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
        run('createuser ' + env.user)
        run('exit')
        run('createdb ' + env.user)



def profile_conf():
    puts(green('Configuring .profile settings.'))
    profile = text_template(templates.profile, MACHINE)
    file_append(MACHINE['OWNER_PROFILE'], profile)
    run('source ' + MACHINE['OWNER_PROFILE'])


def firewall_conf():
    sudo('ufw default deny')
    sudo('ufw allow 80')
    sudo('ufw allow 443')
    sudo('ufw allow 587')
    sudo('ufw enable')


def link_conf():
    puts(green('Configuring necessary symlinks for our libraries.'))
    mode_sudo()
    file_link('/usr/lib/x86_64-linux-gnu/libjpeg.so', '/usr/lib/libjpeg.so', symbolic=True)
    file_link('/usr/lib/x86_64-linux-gnu/libpng.so', '/usr/lib/libpng.so', symbolic=True)
    file_link('/usr/lib/x86_64-linux-gnu/libz.so', '/usr/lib/libz.so', symbolic=True)
    file_link('/usr/lib/x86_64-linux-gnu/libfreetype.so', '/usr/lib/libfreetype.so', symbolic=True)
    file_link('/usr/lib/x86_64-linux-gnu/liblcms.so', '/usr/lib/liblcms.so', symbolic=True)


def reboot():
    sudo('reboot')


######                  ######
##### PROJECT FUNCTIONS  #####
####                      ####





"""
def security_conf()
    pass
### Lock down access

Now we want to lock down access to the machine. We want to completely disable all password access, and, disable root logins.

To disable password access, first we need to generate some ssh keys.

If you are on Mac or Linux, simply type:

    ssh-keygen

and follow the steps. Create a name for the key (the same name as the hostname you gave to the machine earlier would be logical, but you can call it anything).

Again, on Mac or Linux, just make sure that this key is in the .ssh folder of your user.

I gave the key a name because I presume that most developers need multiple keys, so they need a way to manage them.

To do that, you need a config file in your .ssh folder. This file just tells ssh which key to use for any given connection. For each key, you'll have a record like this:

    Host your.ip.address
    IdentityFile ~/.ssh/your_key


It is pretty straightforward.

Again, these ssh steps are all on your local machine.

You'll notice that two files were generated when you created the ssh key - one with no extension, and one with a .pub extension. Now we need to get the one with the .pub extension into the user's ssh directory on the machine. The handshake between the keys is what will log you in.


For this we'll use scp, a utility to copy files over ssh. From your local machine, execute the following command.

    scp ~/.ssh/your_key.pub your_user@your.ip.address:

The trailing : is important. It says to put the public key in the user's home directory.

Now, log back into the machine, create an .ssh directory in the user's directory (if there isn't one already), and copy the pub key into that .ssh directory. The, rename the pub key as "authorized_keys". Future keys will need to be appended to this file.

To make sure that this user and only this user can fiddle with this key, enter the following commands:

    chown -R example_user:example_user ~example_user/.ssh
    chmod 700 ~example_user/.ssh
    chmod 600 ~example_user/.ssh/authorized_keys


Now we are going to shutdown password access, and root user login.

Remember, we are now logged in as the created user, so, to perform system commands like this, we use sudo.

    sudo nano /etc/ssh/sshd_config

First we'll disable root login. Find the appropriate lne and change it to no.

    PermitRootLogin no

Before we disbale password access, we want to check that our key is actually working.

So, logout of the machine.

If you can log back in again without reentering your password, you're good. (if you password protected your ssh key when setting it up, your local machne will ask for THAT password, but the server won't ask for a password).

If not, work out why and do not do the net steps.


So, now we are back in, we'll disable password access:

    sudo nano /etc/ssh/sshd_config

And the line:

    PasswordAuthentication no

Ok, we've go the system pretty locked down at a basic level. Now let's enable a firewall.
"""

from openbudget.settings import *

# required by TravisCI postgres instance
DATABASES['default']['USER'] = 'postgres'

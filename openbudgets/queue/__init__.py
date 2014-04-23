import os
from celery import Celery
from django.conf import settings
from openbudgets.queue import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openbudgets.settings')


app = Celery('openbudgets')
app.config_from_object(config)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

from celery.task import task
from django.core.mail import send_mail
from openbudget.settings import local as settings


@task(name='tasks.save_import')
def save_import(deferred, email):

    from openbudget.apps.transport.incoming.importers.tablibimporter import TablibImporter

    importer = TablibImporter()
    saved = importer.resolve(deferred).save()

    sender = settings.EMAIL_HOST_USER
    recipient = email

    if saved:
        subject = 'IMPORT SAVED'
        message = 'HOORAH!'

    else:
        subject = 'IMPORT FAILED'
        message = 'BUMMER!'

    return send_mail(
        subject,
        message,
        sender,
        [recipient],
        fail_silently=True
    )

from celery.task import task
from django.core.mail import send_mail
from openbudget.settings import local as settings


@task(name='tasks.save_import')
def save_import(deferred, email):

    from openbudget.apps.transport.incoming.importers import TablibImporter

    importer = TablibImporter()
    save = importer.resolve(deferred)

    sender = settings.EMAIL_HOST_USER
    recipient = email

    if save:
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

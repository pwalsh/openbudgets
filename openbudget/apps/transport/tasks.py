from celery.task import task
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
# TODO: this can't use local
from openbudget.settings import local as settings


@task(name='tasks.save_import')
def save_import(deferred, email):

    from openbudget.apps.transport.incoming.importers.tablibimporter import TablibImporter

    importer = TablibImporter()
    saved = importer.resolve(deferred).save()

    sender = settings.EMAIL_HOST_USER
    recipient = email

    if saved:
        subject = _('[OPEN BUDGET]: Data import success')
        message = _('The data import succeeded for ' + deferred['container'])

    else:
        subject = _('[OPEN BUDGET]: Data import failure')
        message = _('The data import failed for ' + deferred['container'])

    return send_mail(
        subject,
        message,
        sender,
        [recipient],
        fail_silently=True
    )

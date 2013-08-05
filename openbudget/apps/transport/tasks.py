from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from celery.task import task
from openbudget.apps.transport.incoming.parsers import get_parser


@task(name='tasks.denormalize_sheet')
def denormalize_sheet(sheet_id):
    from openbudget.apps.sheets.models import Sheet, DenormalizedSheetItem
    sheet = Sheet.objects.get(id=sheet_id)
    items = sheet.sheetitems.all().select_related('node')
    denormalized_items = {}

    for item in items:
        node = item.node
        denormalized_items[node.path] = DenormalizedSheetItem.objects.create(
            normal_item=item,
            sheet=sheet,
            description=item.description,
            budget=item.budget,
            actual=item.actual,
            name=node.name,
            code=node.code,
            direction=node.direction,
            node_description=node.description,
            path=node.path
        )

    for item in denormalized_items.itervalues():
        parent = item.normal_item.node.parent
        if parent:
            item.parent = denormalized_items[parent.path]
            item.save()

        for inverse in node.inverse.all():
            if inverse.path in denormalized_items:
                item.inverse.add(denormalized_items[inverse.path])
        for backward in node.backwards.all():
            if backward.path in denormalized_items:
                item.backwards.add(denormalized_items[backward.path])


@task(name='tasks.save_import')
def save_import(deferred, email):

    from openbudget.apps.transport.incoming.importers.tablibimporter import TablibImporter

    importer = TablibImporter()
    saved = importer.resolve(deferred).save()

    if importer.parser.container_model.get_class_name() == 'sheet':
        denormalize_sheet.apply_async((importer.parser.container_object.id,))

    sender = settings.EMAIL_HOST_USER
    recipient = email

    container = deferred['container']
    name = container.get('name', '')
    if not name:
        name = get_parser(deferred['class']).container_model._meta.verbose_name + ' of '
        entity = container.get('entity', None)
        period = container.get('period_start')
        if entity:
            try:
                entity_name = getattr(entity, 'name')
            except AttributeError:
                entity_name = entity.get('name')
            name += entity_name
        else:
            name += 'unknown'
        name += ' for ' + period

    if saved:
        subject = _('[OPEN BUDGET]: Data import success')
        message = _('The data import succeeded for ' + name)

    else:
        subject = _('[OPEN BUDGET]: Data import failure')
        message = _('The data import failed for ' + name)

    return send_mail(
        subject,
        message,
        sender,
        [recipient],
        fail_silently=True
    )

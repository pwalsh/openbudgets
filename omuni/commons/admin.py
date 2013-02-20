from django.contrib import admin
from django.contrib.contenttypes import generic
#from djcelery.models import TaskState, WorkerState, PeriodicTask, IntervalSchedule, CrontabSchedule
from omuni.commons.models import DataSource


class TranslatedMedia(object):

    js = (

        # for modeltranslation
        'modeltranslation/js/force_jquery.js',
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
        # 'modeltranslation/js/tabbed_translation_fields.js',
        '/static/js/tabbed_translation_fields.js',
        # for grappelli
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/tinymce.js',
    )

    css = {
        # 'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        'screen': ('/static/css/tabbed_translation_fields.css',),
        }


class DataSourceInline(generic.GenericStackedInline):
    """Gives an inlineable DataSource form"""

    model = DataSource
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0


# Celery admin config
#admin.site.unregister(TaskState)
#admin.site.unregister(WorkerState)
#admin.site.unregister(IntervalSchedule)
#admin.site.unregister(CrontabSchedule)
#admin.site.unregister(PeriodicTask)

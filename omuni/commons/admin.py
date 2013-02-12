from django.contrib import admin
from django.contrib.contenttypes import generic
#from djcelery.models import TaskState, WorkerState, PeriodicTask, IntervalSchedule, CrontabSchedule
from omuni.commons.models import DataSource


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

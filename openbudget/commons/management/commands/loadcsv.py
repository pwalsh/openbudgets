import os
from django.core.management.base import BaseCommand
from django.utils import translation
from openbudget.settings import base as settings
from openbudget.apps.transport.incoming.importers.initial import InitImporter


class Command(BaseCommand):
    help = 'Loads initial data for the instance from formatted CSV files.'

    # Also need for the language settings issue described below.
    can_import_settings = False

    def __init__(self):

        # Make django respect our language settings in management commands.
        # We need to enforce this for modeltranslation to work as expected, and
        # work around a hardcoded value for this in Django itself.
        # https://groups.google.com/forum/?fromgroups#!topic/django-modeltranslation/JBgEBfWZZ9A

        translation.activate(settings.MODELTRANSLATION_DEFAULT_LANGUAGE)
        print 'COMMAND INIT'
        print translation.get_language()
        super(Command, self).__init__()

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data from CSV sources.')

        fixtures =  os.listdir(settings.FIXTURE_DIRS[0])
        csvs = [filename for filename in fixtures if filename.endswith('.csv')]

        for csv in csvs:
            self.stdout.write('Writing data from ' + csv + ' ...')
            f = settings.FIXTURE_DIRS[0] + '/' + csv
            importer = InitImporter(f)
            importer.save()

        self.stdout.write("Data from CSV sources loaded. We are ready to rock.")

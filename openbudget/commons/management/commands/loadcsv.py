import os
from django.core.management.base import BaseCommand
from openbudget.settings import base as settings
from openbudget.apps.transport.incoming.importers.initial import InitImporter


class Command(BaseCommand):
    help = 'Loads initial data for the instance from formatted CSV files.'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data from CSV sources.')

        fixtures =  os.listdir(settings.FIXTURE_DIRS[0])
        csvs = [filename for filename in fixtures if filename.endswith('.csv')]

        for csv in csvs:
            self.stdout.write('Writing data from ' + csv + ' ...')
            f = settings.FIXTURE_DIRS[0] + '/' + csv
            importer = InitImporter(f)
            importer.save()
            from time import sleep
            sleep(5)

        self.stdout.write("Data from CSV sources loaded. We are ready to rock.")

import os
from optparse import make_option
from subprocess import call
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from openbudget.settings import local as settings
from modeltranslation.models import autodiscover as register_models_translations


class Command(BaseCommand):
    help = 'Bootstrap development environment'
    option_list = BaseCommand.option_list + (
            make_option(
                '-t',
                action='store_true',
                dest='test',
                default=False,
                help="Run tests"
            ),
        )

    def handle(self, *args, **options):
        self.stdout.write("### DON'T PANIC\n")
        self.stdout.write("### Bootstrapping development environment\n")

        # remove current database file
        db_file_path = settings.DATABASES['default']['NAME']

        if os.path.isfile(db_file_path):
            try:
                self.stdout.write("### Removing DB\n")
                os.remove(db_file_path)
            except IOError as e:
                raise CommandError(e)

        # sync the db and do South migrations
        try:
            self.stdout.write("### Syncing DB\n")
            call_command('syncdb', interactive=False, migrate=True)
        except:
            raise CommandError('syncdb failed')

        # register models translations (duh)
        self.stdout.write("### Registering models translations\n")
        register_models_translations()

        self.stdout.write("### Loading fixtures\n")
        for fixture in settings.DEVSTRAP['FIXTURES']:
            call_command('loaddata', fixture)

        if options['test']:
            call_command('test', 'accounts', 'api', 'budgets', 'commons', 'govts', 'interactions', 'pages', 'international')

        self.stdout.write("### Development bootstrapping completed successfully\n")
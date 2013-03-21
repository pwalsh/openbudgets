from django.core.management import call_command
from django.core.management.base import BaseCommand
from openbudget.settings import local as settings


class Command(BaseCommand):
    help = 'Test only the apps configured in settings.DEVSTRAP.TESTS'

    def handle(self, *args, **options):
        self.stdout.write("### DON'T PANIC\n")
        self.stdout.write("### Testing just what you asked for\n")

        call_command('test', *settings.DEVSTRAP['TESTS'])

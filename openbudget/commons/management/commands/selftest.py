from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Test only the apps configured in settings.OPENBUDGETS_BOOTSTRAP.TESTS'

    def handle(self, *args, **options):
        self.stdout.write("### DON'T PANIC\n")
        self.stdout.write("### Testing just what you asked for\n")

        call_command('test', *settings.OPENBUDGETS_BOOTSTRAP['TESTS'])

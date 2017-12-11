import re

from django.core.management.base import BaseCommand

from bluebottle.clients.utils import LocalTenant
from bluebottle.analytics.utils import create_report_views


class Command(BaseCommand):
    help = 'Create report views (database)'

    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', action='store', dest='file',
                            help="File path to sql for creating report views")
        parser.add_argument('--tenant', '-t', action='store', dest='tenant',
                            help="Tenant name")

    def handle(self, *args, **options):
        if not options['file']:
            raise Exception('`Please specify either an sql file path')

        create_report_views(options['file'], options['tenant'])

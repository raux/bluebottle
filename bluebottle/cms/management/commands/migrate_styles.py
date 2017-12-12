from StringIO import StringIO
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.files import File

from bluebottle.clients import properties
from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant

from bluebottle.cms.models import (
    StylePlatformSettings, StyleRule
)


class Command(BaseCommand):
    help = 'Create styles settings'

    def add_arguments(self, parser):
        parser.add_argument('--tenant', '-t', action='store', dest='tenant',
                            help="The tenant to create styles for")
        parser.add_argument('--all', '-a', action='store_true', dest='all',
                            default=False, help="Import all tenants")

    def handle(self, *args, **options):
        if options['all']:
            tenants = Client.objects.all()

        if options['tenant']:
            tenants = [Client.objects.get(schema_name=options['tenant'])]

        for client in tenants:
            print "\n\nCreating settings for {}".format(client.name)
            connection.set_tenant(client)

            with LocalTenant(client, clear_tenant=True):
                try:
                    style = properties.STYLES
                    (settings, _created) = StylePlatformSettings.objects.update_or_create(
                        pk=1,
                        defaults={
                            'logo': File(
                                StringIO(style['logo']),
                                name='logo.svg'
                            )
                        }
                    )

                    for key, value in style['rules'].items():
                        StyleRule(settings=settings, key=key, value=value).save()
                except AttributeError:
                    pass

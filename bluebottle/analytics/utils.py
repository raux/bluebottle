import re
import os
import logging

from django.conf import settings
from django.db import connection
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.management import call_command
from django.db import connection

from tenant_extras.utils import TenantLanguage

from bluebottle.clients import properties
from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant
from .tasks import queue_analytics_record


logger = logging.getLogger(__name__)


def drop_report_views(client_name=None):
    if client_name:
        clients = [Client.objects.get(client_name=client_name)]
    else:
        clients = Client.objects.all()

    for client in clients:
        connection.set_tenant(client)
        with LocalTenant(client, clear_tenant=True):
            cursor = connection.cursor()

            # NOTE: Drop with cascade on v_projects view should drop all
            #       views related to reporting.
            cursor.execute('DROP VIEW IF EXISTS v_projects CASCADE;')


def create_report_views(sql_file_path=None, client_name=None):
    if not sql_file_path:
        sql_file_path = os.path.join(settings.PROJECT_ROOT, 'bluebottle', 'analytics',
                                     'views', 'report.sql')
        logger.info('Using default views file for reporting: {}'.format(sql_file_path))
    import pudb;pudb.set_trace() 
    with open(sql_file_path, 'r') as file:
        report_sql = file.read()

    # Remove comments and blank lines
    sql_lines = filter(lambda x: not re.match(r'^(---.*|\s*)$', x), report_sql.splitlines())

    # Basic sanity check
    if not (re.match(r'^\s*DROP VIEW.*', sql_lines[0]) and
            re.match(r'^\s*CREATE OR REPLACE VIEW.*', sql_lines[1])):
        raise Exception('Is this a valid query to create a database view?')

    if client_name:
        clients = [Client.objects.get(client_name=client_name)]
    else:
        clients = Client.objects.all()

    sql = "\n".join(sql_lines)

    for client in clients:
        connection.set_tenant(client)
        with LocalTenant(client, clear_tenant=True):
            cursor = connection.cursor()
            cursor.execute(sql)


def _multi_getattr(obj, attr, **kw):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
            if callable(obj):
                obj = obj()
        except AttributeError:
            if 'default' in kw:
                return kw['default']
            else:
                raise
    return obj


def process(instance, created):
    instance_name = instance.__class__.__name__

    # _merge_attrs combines the base and instance tag or field values with
    # the class values. It also handles translateable attrs.
    def _merge_attrs(data, attrs):
        try:
            items = attrs.iteritems()
        except AttributeError:
            logger.exception('analytics_merge_attrs')
            return

        for label, attr in items:
            options = {}
            # If a dict is passed then the key is the dotted
            # property string and the value is options.
            try:
                new_attr = attr.keys()[0]
                options = attr[new_attr]
                attr = new_attr
            except AttributeError:
                # TODO: Logging
                pass

            value = _multi_getattr(instance, attr, default='')

            if options.get('translate', False):
                with LocalTenant():
                    # Translate using the default tenant language
                    with TenantLanguage(getattr(properties, 'LANGUAGE_CODE', 'en')):
                        # If attr is a string then try to translate
                        # Note: tag values should always be strings.
                        value = _(value)

            data[label] = value

    def snakecase(name):
        return re.sub("([A-Z])", "_\\1", name).lower().lstrip("_")

    if not getattr(settings, 'ANALYTICS_ENABLED', False):
        logger.debug('analytics_disabled')
        return

    # Return early if instance is a migration.
    if instance_name == 'Migration':
        return

    # Check if the instance has an _original_status and whether the status
    # has changed. If not then skip recording this save event. This can be
    # skipped if the record has been created as we will always record metrics
    # for a newly created record.
    try:
        if not created and instance._original_status == instance.status:
            return
    except AttributeError:
        pass

    # Return early if the instance doesn't have an Analytics class
    # or there is no tenant schema set.
    try:
        analytics_cls = instance.Analytics
        tenant_name = connection.schema_name
    except AttributeError:
        return

    analytics = analytics_cls()

    # Check if the analytics class for the instance has a skip
    # method and return if skip return true, otherwise continue
    try:
        if analytics.skip(instance, created):
            return
    except AttributeError:
        pass

    try:
        timestamp = analytics.timestamp(instance, created)
    except AttributeError:
        timestamp = timezone.now()

    # Check for instance specific tags
    try:
        tags = analytics.extra_tags(instance, created)
    except AttributeError:
        tags = {}

    tags['type'] = getattr(analytics, 'type', snakecase(instance_name))
    tags['tenant'] = tenant_name

    # Process tags
    _merge_attrs(tags, analytics.tags)

    # Check for instance specific fields
    try:
        fields = analytics.extra_fields(instance, created)
    except AttributeError:
        fields = {}

    # Process fields
    _merge_attrs(fields, analytics.fields)

    # If enabled, use celery to queue task
    if getattr(properties, 'CELERY_RESULT_BACKEND', None):
        queue_analytics_record.delay(timestamp=timestamp, tags=tags, fields=fields)
    else:
        queue_analytics_record(timestamp=timestamp, tags=tags, fields=fields)


class NoReportingViews(object):
    def __init__(self, client_name=None):
        if not client_name:
            client = Client.objects.get(schema_name=connection.schema_name)
            self.client_name = client.client_name
        else:
            self.client_name = client_name

    def __enter__(self):
        drop_report_views(client_name=self.client_name)

    def __exit__(self, type, value, traceback):
        create_report_views(client_name=self.client_name)

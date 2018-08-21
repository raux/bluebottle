# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-01 10:18
from __future__ import unicode_literals

from django.db import migrations, connection
from django.utils.translation import activate, _trans, ugettext as _

from tenant_extras.middleware import tenant_translation
from bluebottle.clients.utils import LocalTenant


def translate_themes(apps, schema_editor):
    Client = apps.get_model('clients', 'Client')
    ProjectTheme = apps.get_model('bb_projects', 'ProjectTheme')

    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)

    with LocalTenant(tenant):
        for theme in ProjectTheme.objects.all():
            for translation in theme.translations.all():
                activate(translation.language_code)
                _trans._active.value = tenant_translation(
                    translation.language_code, connection.tenant.client_name
                )
                translation.name = _(translation.name)
                translation.description = _(translation.description)
                translation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0078_auto_20180528_1414'),
    ]

    operations = [
        migrations.RunPython(translate_themes)
    ]
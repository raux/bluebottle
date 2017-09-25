# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-15 11:58
from __future__ import unicode_literals

from django.db import migrations


from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Anonymous': {
            'perms': ('api_read_projectimage',)
        },
        'Authenticated': {
            'perms': (
                'api_read_projectimage', 'api_add_own_projectimage',
                'api_change_own_projectimage', 'api_delete_own_projectimage',
            )
        }
    }

    update_group_permissions('projects', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_auto_20170915_1358'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
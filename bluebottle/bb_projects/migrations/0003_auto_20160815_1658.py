# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-15 14:58
from __future__ import unicode_literals

from django.db import migrations


def update_status_names(apps, schema_editor):
    ProjectPhase = apps.get_model('bb_projects', 'ProjectPhase')

    updates =  {
        'plan-new': 'Plan - Draft',
        'voting': 'Voting - Running',
        'campaign': 'Project - Running',
        'done-complete': 'Project - Realised',
        'done-incomplete': 'Project - Done',
        'closed': 'Rejected / Cancelled'
    }

    for slug, new_name in updates.items():
        try:
            phase = ProjectPhase.objects.get(slug=slug)
            phase.name = new_name

            phase.save()
        except ProjectPhase.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('bb_projects', '0002_remove_projecttheme_name_nl'),
    ]

    operations = [
        migrations.RunPython(update_status_names)
    ]

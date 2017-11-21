# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-20 11:07
from __future__ import unicode_literals

from django.db import migrations


def set_campaign_ended(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.filter(status__slug='done-complete').all():
        logs = project.projectphaselog_set.filter(status__slug='done-complete').order_by('-start')
        if logs.count():
            project.campaign_ended = logs.all()[0].start
            project.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0044_auto_20171110_1549'),
    ]

    operations = [
        migrations.RunPython(set_campaign_ended)
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-06 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def migrate_stats(apps, schema_editor):
    Stat = apps.get_model('cms', 'Stat')
    for stat in Stat.objects.all():
        pk = stat.pk
        # There might be multiple pages using the same list
        # so we iterate and make copies and then delete the original
        translations = stat.translations.all()
        for block in stat.stats.stats_content.all():
            new_stat = stat
            new_stat.block = block
            new_stat.pk = None
            new_stat.save()
            new_stat.translations = translations
            new_stat.save()
        Stat.objects.filter(pk=pk).all().delete()

def dummy(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0025_migrate_stats_1'),
    ]

    operations = [
        migrations.RunPython(migrate_stats, dummy),
    ]

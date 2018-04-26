# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-30 11:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb_projects', '0008_migrate_theme_translations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projecttheme',
            options={'ordering': ['translations__name'], 'permissions': (('api_read_projecttheme', 'Can view project theme through API'),), 'verbose_name': 'project theme', 'verbose_name_plural': 'project themes'},
        ),
        migrations.RenameField(
            model_name='projectthemetranslation',
            old_name='_description',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='projecttheme',
            name='description',
        ),
        migrations.RemoveField(
            model_name='projecttheme',
            name='name',
        ),
    ]

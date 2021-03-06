# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 10:59
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20161208_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareresultscontent',
            name='share_text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stat',
            name='stats',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Stats'),
        ),
    ]

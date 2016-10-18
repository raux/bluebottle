# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-06 09:49
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='currencies',
            field=select_multiple_field.models.SelectMultipleField(choices=[(b'EUR', b'Euro')], max_length=100, null=True),
        ),
    ]
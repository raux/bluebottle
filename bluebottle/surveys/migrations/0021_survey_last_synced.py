# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-27 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0020_answer_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='last_synced',
            field=models.DateTimeField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-19 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0008_question_properties'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='value',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
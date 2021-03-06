# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-23 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0005_merge_20170124_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='type',
            field=models.CharField(choices=[(b'manual', 'Manual'), (b'donated_total', 'Donated total'), (b'pledged_total', 'Pledged total'), (b'projects_online', 'Projects online'), (b'projects_realized', 'Projects realized'), (b'projects_complete', 'Projects complete'), (b'tasks_realized', 'Tasks realized'), (b'task_members', 'Taskmembers'), (b'people_involved', 'People involved'), (b'participants', 'Participants'), (b'amount_matched', 'Amount Matched'), (b'votes_cast', 'Number of votes cast')], db_index=True, default=b'manual', max_length=20, verbose_name='Type'),
        ),
    ]

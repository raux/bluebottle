# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-19 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0021_auto_20171017_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='component',
            field=models.CharField(blank=True, choices=[(b'page', 'Page'), (b'project', 'Project'), (b'task', 'Task'), (b'fundraiser', 'Fundraiser'), (b'results', 'Results'), (b'news', 'News')], max_length=50, null=True, verbose_name='Component'),
        ),
        migrations.AlterField(
            model_name='link',
            name='component_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Component ID'),
        ),
        migrations.AlterField(
            model_name='link',
            name='external_link',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='External Link'),
        ),
        migrations.AlterField(
            model_name='linkgroup',
            name='name',
            field=models.CharField(choices=[(b'main', 'Main'), (b'about', 'About'), (b'info', 'Info'), (b'discover', 'Discover'), (b'social', 'Social')], default=b'main', max_length=25),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager

from fluent_contents.models.managers import ContentItemManager


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('cms', '0003_merge_20161207_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsMapContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'contentitem_cms_projectsmapcontent',
                'verbose_name': 'Projects Map',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]

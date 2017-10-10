# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-10 10:55
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_add_group_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('group', models.CharField(choices=[(b'main', 'Main'), (b'about', 'About'), (b'info', 'Info'), (b'discover', 'Discover'), (b'social', 'Social')], default=b'main', max_length=25)),
                ('highlight', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['sequence'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LinkPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(help_text='A dot separated app name and permission codename.', max_length=255)),
                ('present', models.BooleanField(default=True, help_text='Should the permission be present or not to access the link?')),
            ],
        ),
        migrations.CreateModel(
            name='LinkTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('component', models.CharField(blank=True, choices=[(b'page', 'Page'), (b'project', 'Project'), (b'task', 'Task'), (b'fundraiser', 'Fundraiser'), (b'results', 'Results'), (b'news', 'News')], max_length=50, verbose_name='Component')),
                ('component_id', models.CharField(blank=True, max_length=100, verbose_name='Component ID')),
                ('external_link', models.CharField(blank=True, max_length=2000, verbose_name='External Link')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cms.Link')),
            ],
            options={
                'managed': True,
                'db_table': 'cms_link_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'link Translation',
            },
        ),
        migrations.CreateModel(
            name='SiteLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_copyright', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Site links',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='link_permissions',
            field=models.ManyToManyField(blank=True, to='cms.LinkPermission'),
        ),
        migrations.AddField(
            model_name='link',
            name='site_links',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='cms.SiteLinks'),
        ),
        migrations.AlterUniqueTogether(
            name='linktranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]

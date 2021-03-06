# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-18 12:13
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import parler.models

from fluent_contents.models.managers import ContentItemManager


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('cms', '0039_auto_20171017_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', bluebottle.utils.fields.ImageField(blank=True, max_length=255, null=True, upload_to=b'logo_images/', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='LogosContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=70, null=True)),
                ('action_text', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'contentitem_cms_logoscontent',
                'verbose_name': 'Logos',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='logo',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logos', to='cms.LogosContent'),
        ),
    ]

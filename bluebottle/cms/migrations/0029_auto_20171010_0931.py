# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-10 07:31
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('geo', '0004_auto_20160929_0817'),
        ('cms', '0028_merge_20171006_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriesContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=70, null=True)),
                ('categories', models.ManyToManyField(db_table=b'cms_taskscontent_categories', to='geo.Location')),
            ],
            options={
                'db_table': 'contentitem_cms_categoriescontent',
                'verbose_name': 'Categories',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='LocationsContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=70, null=True)),
                ('locations', models.ManyToManyField(db_table=b'cms_taskscontent_locations', to='geo.Location')),
            ],
            options={
                'db_table': 'contentitem_cms_locationscontent',
                'verbose_name': 'Locations',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SlidesContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
            ],
            options={
                'db_table': 'contentitem_cms_slidescontent',
                'verbose_name': 'Slides',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SlideTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('tab_text', models.CharField(help_text='This is shown on tabs beneath the banner.', max_length=100, verbose_name='Tab text')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Title')),
                ('body', models.TextField(blank=True, verbose_name='Body text')),
                ('image', bluebottle.utils.fields.ImageField(blank=True, max_length=255, null=True, upload_to=b'banner_slides/', verbose_name='Image')),
                ('background_image', bluebottle.utils.fields.ImageField(blank=True, max_length=255, null=True, upload_to=b'banner_slides/', verbose_name='Background image')),
                ('video_url', models.URLField(blank=True, default=b'', max_length=100, verbose_name='Video url')),
                ('link_text', models.CharField(blank=True, help_text='This is the text on the button inside the banner.', max_length=400, verbose_name='Link text')),
                ('link_url', models.CharField(blank=True, help_text='This is the link for the button inside the banner.', max_length=400, verbose_name='Link url')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cms.Slide')),
            ],
            options={
                'managed': True,
                'db_table': 'cms_slide_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'slide Translation',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', bluebottle.utils.fields.ImageField(blank=True, max_length=255, null=True, upload_to=b'step_images/', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StepsContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=70, null=True)),
                ('action_text', models.CharField(blank=True, default='Start your own project', max_length=40, null=True)),
                ('action_link', models.CharField(blank=True, default=b'/start-project', max_length=100, null=True)),
            ],
            options={
                'db_table': 'contentitem_cms_stepscontent',
                'verbose_name': 'Steps',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='StepTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('header', models.CharField(max_length=100, verbose_name='Header')),
                ('text', models.CharField(max_length=400, verbose_name='Text')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cms.Step')),
            ],
            options={
                'managed': True,
                'db_table': 'cms_step_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'step Translation',
            },
        ),
        migrations.RemoveField(
            model_name='metric',
            name='block',
        ),
        migrations.RemoveField(
            model_name='metricscontent',
            name='contentitem_ptr',
        ),
        migrations.AlterUniqueTogether(
            name='metrictranslation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='metrictranslation',
            name='master',
        ),
        migrations.DeleteModel(
            name='Metric',
        ),
        migrations.DeleteModel(
            name='MetricsContent',
        ),
        migrations.DeleteModel(
            name='MetricTranslation',
        ),
        migrations.AddField(
            model_name='step',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='cms.StepsContent'),
        ),
        migrations.AddField(
            model_name='slide',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='cms.SlidesContent'),
        ),
        migrations.AlterUniqueTogether(
            name='steptranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='slidetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]

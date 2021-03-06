# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 13:25
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bb_projects', '0001_initial'),
        ('geo', '0001_initial'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=254, unique=True, verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='deleted')),
                ('user_type', models.CharField(choices=[(b'person', 'Person'), (b'company', 'Company'), (b'foundation', 'Foundation'), (b'school', 'School'), (b'group', 'Club / association')], default=b'person', max_length=25, verbose_name='Member Type')),
                ('first_name', models.CharField(blank=True, max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=100, verbose_name='last name')),
                ('place', models.CharField(blank=True, max_length=100, verbose_name='Location your at now')),
                ('picture', bluebottle.utils.fields.ImageField(blank=True, upload_to=b'profiles', verbose_name='picture')),
                ('is_co_financer', models.BooleanField(default=False, help_text='Donations by co-financers are shown in a separate list on the project page.These donation will always be visible.', verbose_name='Co-financer')),
                ('can_pledge', models.BooleanField(default=False, help_text='User can create a pledge donation.', verbose_name='Can pledge')),
                ('about_me', models.TextField(blank=True, max_length=265, verbose_name='about me')),
                ('primary_language', models.CharField(choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-co', b'Colombian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gd', b'Scottish Gaelic'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese')], default='en', help_text='Language used for website and emails.', max_length=5, verbose_name='primary language')),
                ('share_time_knowledge', models.BooleanField(default=False, verbose_name='share time and knowledge')),
                ('share_money', models.BooleanField(default=False, verbose_name='share money')),
                ('newsletter', models.BooleanField(default=True, help_text='Subscribe to newsletter.', verbose_name='newsletter')),
                ('phone_number', models.CharField(blank=True, max_length=50, verbose_name='phone number')),
                ('gender', models.CharField(blank=True, choices=[(b'male', 'Male'), (b'female', 'Female')], max_length=6, verbose_name='gender')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='birthdate')),
                ('disable_token', models.CharField(blank=True, max_length=32, null=True)),
                ('campaign_notifications', models.BooleanField(default=True, verbose_name='Project Notifications')),
                ('website', models.URLField(blank=True, verbose_name='website')),
                ('facebook', models.CharField(blank=True, max_length=50, verbose_name='facebook profile')),
                ('twitter', models.CharField(blank=True, max_length=15, verbose_name='twitter profile')),
                ('skypename', models.CharField(blank=True, max_length=32, verbose_name='skype profile')),
                ('remote_id', models.CharField(blank=True, max_length=75, null=True, verbose_name='remote_id')),
                ('favourite_themes', models.ManyToManyField(blank=True, to='bb_projects.ProjectTheme')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('location', models.ForeignKey(blank=True, help_text='Location', null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.Location')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'member',
                'verbose_name_plural': 'members',
            },
        ),
    ]

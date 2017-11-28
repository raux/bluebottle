# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-18 12:37
from __future__ import unicode_literals

from django.db import migrations
import parler


def set_default_translation(apps, schema_editor):
    Quote = apps.get_model('cms', 'Quote')
    QuoteTranslation = apps.get_model('cms', 'QuoteTranslation')

    for quote in Quote.objects.all():
        try:
            translation = QuoteTranslation.objects.get(
                language_code=quote.block.language_code,
                master=quote
            )
            quote.temp_name = translation.name
            quote.temp_quote = translation.quote
            quote.save()
        except QuoteTranslation.DoesNotExist:
            pass



class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0041_auto_20171018_1437'),
    ]

    operations = [
        migrations.RunPython(set_default_translation)
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-09 12:37
from __future__ import unicode_literals

from django.db import migrations


from bluebottle.utils.utils import StatusDefinition


def set_refund_status(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order._meta.get_field('status').protected = False

    for order in Order.objects.filter(order_payments__status=StatusDefinition.REFUNDED):

        if any(donation.project.status.slug == 'refunded' for donation in order.donations.all()):
            order.status = StatusDefinition.CANCELLED
        else:
            order.status = StatusDefinition.REFUNDED

        order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20180509_1436'),
    ]

    operations = [
        migrations.RunPython(set_refund_status)
    ]

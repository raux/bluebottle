from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'bluebottle.settings.local')

app = Celery('bluebottle',
             broker=getattr(settings, 'BROKER_URL', 'amqp://guest@localhost//'))

app.config_from_object('celeryconfig')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print ('Request: {0!r}').format(self.request)

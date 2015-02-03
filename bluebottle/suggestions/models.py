from datetime import date, timedelta
from django.db import models
from djchoices import DjangoChoices, ChoiceItem
from django.utils.translation import ugettext as _
from django_extensions.db.fields import (
    ModificationDateTimeField, CreationDateTimeField)
from bluebottle.utils.model_dispatcher import get_project_model

PROJECT_MODEL = get_project_model()

class Suggestion(models.Model):
    class Statuses(DjangoChoices):
        unconfirmed = ChoiceItem('unconfirmed', label=_('Unconfirmed email'))
        draft = ChoiceItem('draft', label=_('Draft'))
        accepted = ChoiceItem('accepted', label=_('Accepted'))
        rejected = ChoiceItem('rejected', label=_('Rejected'))
        expired = ChoiceItem('expired', label=_('Expired'))
        in_progress = ChoiceItem('in_progress', label=_('In progress'))
        submitted = ChoiceItem('submitted', label=_('Submitted'))

    created = CreationDateTimeField(_('created'), help_text=_('When this project was created.'))
    updated = ModificationDateTimeField(_('updated'), help_text=_('When this project was updated.'))
    
    title = models.TextField() ## description
    pitch = models.TextField() ## requirements
    deadline = models.DateField() ## date
    theme = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    org_name = models.CharField(max_length=100)
    org_contactname = models.CharField(max_length=100)
    org_email = models.EmailField()
    org_phone = models.CharField(max_length=64)
    org_website = models.URLField()

    status = models.CharField(_("status"), choices=Statuses.choices, max_length=64, default="unconfirmed")
    token = models.CharField(max_length=100)

    project = models.ForeignKey(PROJECT_MODEL, related_name="suggestions", 
                                null=True, blank=True)

    def confirm(self):
        if self.status == "unconfirmed":
            self.status = 'draft'
            self.save()
            return True

        return False

    @property
    def expired(self):
        # Expired will return False if the deadline is today
        return self.deadline - date.today() < timedelta(0)

    def __unicode__(self):
        return u'Suggestion "{0}" from {1}'.format(self.title, self.org_contactname)

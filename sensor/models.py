from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class Reading(models.Model):
    date_time = models.DateTimeField('time reading taken')
    value = models.IntegerField('reading value', blank=True)

    def __unicode__(self):
        return unicode(self.id)

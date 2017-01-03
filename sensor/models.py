from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Reading(models.Model):
    datetime = models.DateTimeField('time reading taken')
    value = models.IntegerField('reading value', blank=True)

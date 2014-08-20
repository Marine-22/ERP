from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from erp.apps.partner.models import Partner

class Currency(models.Model):
    Currency = models.CharField(max_length=100)
    Symbol = models.CharField(max_length=100)
    def __unicode__(self):
        return u'%s' % (self.Symbol)


from django.contrib.auth.models import User
from django.db import models

class Internal(models.Model):
    Name = models.CharField(max_length=200)
    Description = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return u'%s' % (self.Name)
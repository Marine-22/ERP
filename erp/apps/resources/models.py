from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from erp.apps.partner.models import Partner

class UserType(models.Model):
    Type = models.CharField(max_length=100)
    def __unicode__(self):
        return u'%s' % self.Type

class InternalRole(models.Model):
    Role = models.CharField(max_length=100)
    def __unicode__(self):
        return u'%s' % self.Role

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    ManHourCost = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    ManHourSale = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    Phone = models.CharField(max_length=30,null=True,blank=True)
    Partner = models.ForeignKey(Partner, null=True, blank=True)
    InternalRole = models.ForeignKey(InternalRole, null=True, blank=True)
    UserType = models.ForeignKey(UserType, null=True, blank=True)
    def __unicode__(self):
        return u'%s' % self.user

def __str__(self):
    return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
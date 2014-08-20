from django.contrib.auth.models import User
from django.db import models
from erp.apps.project.models import Project

class Allocation(models.Model):
    Project = models.ForeignKey(Project, null=True, blank=True, related_name='Projectname')
    Resource = models.ForeignKey(User, related_name='Username')
    FixedPrice = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    Start = models.DateTimeField(null=True, blank=True)
    End = models.DateTimeField(null=True, blank=True)
    Mandays = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    HourSale = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
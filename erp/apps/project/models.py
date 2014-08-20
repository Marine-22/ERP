from django.contrib.auth.models import User
from django.db import models

from erp.apps.partner.models import Partner
from erp.libs.workflows.models import State


class ProjectType(models.Model):
    Type = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.Type


class ProjectSegment(models.Model):
    Segment = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.Segment


class Project(models.Model):
    Name = models.CharField(max_length=200)
    ProjectClient = models.ForeignKey(Partner)
    Start = models.DateField(blank=True, null=True)
    End = models.DateField(blank=True, null=True)
    ProjectManager = models.ForeignKey(User, related_name='PM')
    QualityAssurance = models.ForeignKey(User, related_name='QA')
    Status = models.ForeignKey(State, null=True, blank=True)
    Price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    Segment = models.ForeignKey(ProjectSegment, null=True, blank=True)
    Type = models.ForeignKey(ProjectType, null=True, blank=True)
    Milestone = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return u'%s' % self.Name


class ProjectNote(models.Model):
    Project = models.ForeignKey(Project)
    Note = models.TextField()


class ProjectPhase(models.Model):
    Partner = models.ForeignKey(Partner, null=True, blank=True)
    Name = models.CharField(max_length=200)
    Project = models.ForeignKey(Project, blank=True, null=True)
    Milestone = models.BooleanField(default=False, blank=True)
    Status = models.ForeignKey(State, blank=True, null=True)
    Price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    Start = models.DateField(null=True, blank=True)
    End = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.Name


class Allocation(models.Model):
    Project = models.ForeignKey(Project, null=True, blank=True)
    Resource = models.ForeignKey(User)
    FixedPrice = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    Start = models.DateTimeField(null=True, blank=True)
    End = models.DateTimeField(null=True, blank=True)
    Mandays = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    HourSale = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
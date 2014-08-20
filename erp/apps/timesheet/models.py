from django.contrib.auth.models import User
from django.db import models
from erp.apps.internal.models import Internal
from erp.apps.partner.models import Partner
from erp.apps.project.models import ProjectPhase, Project
from erp.libs.workflows.models import State
from smart_selects.db_fields import ChainedForeignKey

class TimeSheet(models.Model):
    DueDate = models.DateField(auto_now_add=False, blank=True,null=True)
    User = models.ForeignKey(User, null=True, blank=True)
    Partner = models.ForeignKey(Partner, null=True, blank=True)
    Project = models.ForeignKey(Project)#, chained_field="Partner", chained_model_field="ProjectClient")
    Phase = models.ForeignKey(ProjectPhase, blank=True, null=True)#, chained_field="Project",chained_model_field="Project",blank=True,null=True)
    Activity = models.TextField(blank=True,null=True)
    Hours = models.DecimalField(max_digits=5, decimal_places=1)
    Status = models.ForeignKey(State, blank=True,null=True)
    HoursBooked = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)

class InternalTimeSheet(models.Model):
    InternalDueDate = models.DateField(auto_now_add=False, blank=True, null=True)
    User = models.ForeignKey(User)
    Internal = models.ForeignKey(Internal)
    Activity = models.TextField(blank=True, null=True)
    Hours = models.DecimalField(max_digits=5, decimal_places=1)
    Status = models.ForeignKey(State, blank=True, null=True)

class Workshop(models.Model):
    DueDate = models.DateField()
    Ws_Partner = models.ForeignKey(Partner, null=True, blank=True)
    Ws_Project = ChainedForeignKey(Project, chained_field="Ws_Partner", chained_model_field="ProjectClient")
    Ws_Phase = ChainedForeignKey(ProjectPhase, chained_field="Ws_Project",chained_model_field="Project",blank=True,null=True)
    Activity = models.TextField(blank=True, null=True)
    Start = models.TimeField()
    End = models.TimeField()
    Status = models.ForeignKey(State, blank=True, null=True)
    Resources = models.ManyToManyField(User)

class Holiday(models.Model):
    Date = models.DateField()
    Name = models.CharField(max_length=300)
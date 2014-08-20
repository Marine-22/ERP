from django.db import models
from django.contrib.auth.models import User

"""
from core.master.project.models import Project
from core.master.timesheet.models import Workshop

class WeeklyProjectReport(models.Model):
    Project = models.ForeignKey(Project)
    Week = models.DateField()

class WeeklyProjectReportResource(models.Model):
    Report = models.ForeignKey(WeeklyProjectReport)
    Resource = models.ForeignKey(User)
    AllocationPercent = models.DecimalField(max_digits=4, decimal_places=1)
    AllocationManday = models.DecimalField(max_digits=6, decimal_places=1)
    PlannedAllocation = models.DecimalField(max_digits=4, decimal_places=1,null=True,blank=True)

class WeeklyProjectReportWorkshop(models.Model):
    Report = models.ForeignKey(WeeklyProjectReport)
    Workshop = models.ForeignKey(Workshop)

class WeeklyProjectReportActivity(models.Model):
    Activity = models.TextField()
    Report = models.ForeignKey(WeeklyProjectReport)

class WeeklyProjectReportFutureActivity(models.Model):
    Activity = models.TextField()
    Report = models.ForeignKey(WeeklyProjectReport)

class WeeklyProjectReportIssue(models.Model):
    Issue = models.TextField()
    Report = models.ForeignKey(WeeklyProjectReport)"""

class InternalReport(models.Model):
    Resource = models.ForeignKey(User)
    ResourceFullName = models.CharField(max_length=500, null=True, blank=True)
    Month = models.DateField()
    WorkDays = models.IntegerField()
    WorkHours = models.IntegerField()
    HolidayDays = models.IntegerField()
    IllnessDays = models.IntegerField()
    DoctorDays = models.IntegerField()
    TravelSlovakia = models.IntegerField(null=True, blank=True)
    TravelOutside = models.IntegerField(null=True, blank=True)
    TravelMoney = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    AdvancePayment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Dietary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    DietaryTickets = models.IntegerField()
import time
import datetime
from datetime import timedelta, date

from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from dateutil.relativedelta import relativedelta

from erp.apps.fabric import calendar
from erp.apps.allocation.models import Allocation
from erp.apps.internal.models import Internal
from erp.apps.reporting.models import InternalReport
from erp.apps.timesheet.models import TimeSheet, InternalTimeSheet
from erp.apps.resources.models import UserProfile, UserType, InternalRole
from erp.apps.fabric.workdays import networkdays
from erp.apps.partner.models import Partner
from erp.apps.timesheet.models import Holiday
from erp.libs.workflows.models import State, Workflow


def main(request):
    projects = {}
    days = timedelta(days=120)
    begin = date.today() - days

    allocations = Allocation.objects.filter(Resource=request.user)

    for item in allocations:
        timesheets = TimeSheet.objects.filter(Project=item.Project, DueDate__range=(begin, date.today()))
        single = []
        for ts in timesheets:
            epoch = time.strptime(ts.DueDate.strftime('%Y-%m-%d'), '%Y-%m-%d')
            if epoch:
                epoch = calendar.timegm(epoch)
                single += [float(epoch)*1000,int(ts.Hours)],

        projects[''+item.Project.Name+''] = single

    return render_to_response('main/main.html', {'projects':projects}, context_instance=RequestContext(request))

#Function creates internal report for a month that is passed into it
def createInternalReport(date):
    """
    Create internal report for a month that was passed into function
    """
    holiday = Internal.objects.get(Name='Holiday')
    illness = Internal.objects.get(Name='Illness')
    doctor = Internal.objects.get(Name='Doctor')
    deleted = State.objects.get(name='Deleted', workflow=Workflow.objects.get(name='Timesheet'))
    month, year = date.month, date.year
    first_day = datetime.datetime(date.year, date.month, 1)
    if calendar.isleap(year):
        last_day = datetime.datetime(date.year, date.month, calendar.mdays[date.month])
    else:
        last_day = datetime.datetime(date.year, date.month, calendar.mdays[date.month])
    dayofWeek = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday']

    #Calculate number of workdays for current month
    number_workdays = int(networkdays(first_day,last_day))
    holidays = Holiday.objects.filter(Date__month=month, Date__year=year)
    for item in holidays:
        oldDate = item.Date

        if dayofWeek[datetime.date.weekday(oldDate)] == 'Saturday' or dayofWeek[datetime.date.weekday(oldDate)] == 'Sunday':
            pass
        else:
            number_workdays -= 1
    print number_workdays

    #Calculate ammount of dietary tickets
    delta = relativedelta(months=1)
    next_month = date + delta

    next_month_first = datetime.datetime(next_month.year, next_month.month, 1)
    if calendar.isleap(next_month.year):
        next_month_last = datetime.datetime(next_month.year, next_month.month, calendar.lmdays[next_month.month])
    else:
        next_month_last = datetime.datetime(next_month.year, next_month.month, calendar.mdays[next_month.month])

    next_holidays = Holiday.objects.filter(Date__month=next_month.month, Date__year=next_month.year)

    dietary_tickets = int(networkdays(next_month_first, next_month_last))

    for item in next_holidays:
        oldDate = item.Date

        if dayofWeek[datetime.date.weekday(oldDate)] == 'Saturday' or dayofWeek[datetime.date.weekday(oldDate)] == 'Sunday':
            pass
        else:
            dietary_tickets -= 1


    internal_list = InternalRole.objects.all().exclude(Role='Ex-employee').values_list('Role', flat=True)

    internal = UserType.objects.get(Type='Internal')

    iquap = Partner.objects.get(pk=int(30))
    resource_list = UserProfile.objects.filter(Partner=iquap, UserType=internal, InternalRole__Role__in=internal_list)

    for item in resource_list:

        resource = User.objects.get(pk=item.pk)

        holiday_count = InternalTimeSheet.objects.filter(InternalDueDate__year=year, InternalDueDate__month=month, User=resource, Internal=holiday).exclude(Status=deleted).count()
        illness_count = InternalTimeSheet.objects.filter(InternalDueDate__year=year, InternalDueDate__month=month, User=resource, Internal=illness).exclude(Status=deleted).count()
        doctor_count = InternalTimeSheet.objects.filter(InternalDueDate__year=year, InternalDueDate__month=month, User=resource, Internal=doctor).exclude(Status=deleted).count()
        resource_workdays = number_workdays - holiday_count - doctor_count - illness_count

        try:
            partial_report = InternalReport.objects.get(Month__year=year, Month__month=month, Resource=resource)
            partial_report.ResourceFullName = resource.last_name +' '+ resource.first_name
            partial_report.WorkDays = resource_workdays
            partial_report.WorkHours = resource_workdays*8
            partial_report.HolidayDays = holiday_count
            partial_report.IllnessDays = illness_count
            partial_report.DoctorDays = doctor_count
            partial_report.DietaryTickets = dietary_tickets - holiday_count - illness_count - doctor_count

            partial_report.save()

        except InternalReport.DoesNotExist:
            full_name = resource.last_name +' '+ resource.first_name
            partial_report = InternalReport.objects.create(Resource=resource, ResourceFullName=full_name, Month=date, WorkDays=resource_workdays, WorkHours=resource_workdays*8, HolidayDays=holiday_count, IllnessDays=illness_count, DoctorDays=doctor_count, DietaryTickets=resource_workdays)
            partial_report.save()

def number_of_workdays(month):
    pass
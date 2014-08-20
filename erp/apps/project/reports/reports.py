import calendar
from unicodedata import decimal
import time
from erp.apps.allocation.models import Allocation
from erp.apps.timesheet.models import TimeSheet

def used_budget(project):
    budget = project.Price
    used_budget = 0

    allocations = Allocation.objects.filter(Project=project)

    for item in allocations:
        if item.FixedPrice:
            used_budget = used_budget + item.FixedPrice
        else:
            hours = TimeSheet.objects.filter(User=item.Resource).values('Hours').count()
            used_budget = used_budget + hours*item.HourSale

    return used_budget

def resource_budget_constumption(project):
    resource_budget = {}
    allocations = Allocation.objects.filter(Project=project).order_by('Resource__id')

    for item in allocations:
        hours = None
        if item.FixedPrice:
            resource_budget[''+item.Resource.last_name+' '+item.Resource.first_name+''] = item.FixedPrice
        else:
            hours = TimeSheet.objects.filter(User=item.Resource, Project=project).values('Hours').count()
            
            resource_budget[''+item.Resource.last_name+' '+item.Resource.first_name+''] = int(hours*item.HourSale)

    return resource_budget

def time_consumption(project):
    time_consumption = {}
    allocations = Allocation.objects.filter(Project=project).order_by('Resource__id')

    for item in allocations:
        ts = TimeSheet.objects.filter(Project=project, User=item.Resource)

        single = []
        for timesheet in ts:
            epoch = time.strptime(timesheet.DueDate.strftime('%Y-%m-%d'), '%Y-%m-%d')
            epoch = calendar.timegm(epoch)
            single += [float(epoch)*100,int(timesheet.Hours)],

        time_consumption[''+item.Resource.last_name+''] = single

    return time_consumption

        
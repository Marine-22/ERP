from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from erp.apps.internal.models import Internal
from erp.apps.reporting.reports.holiday_report.helper import construct_holiday_series
from erp.apps.timesheet.models import InternalTimeSheet
import datetime
from erp.libs.workflows.models import Workflow, State

def holiday_report_generator(request):
    return render_to_response('reporting/holiday_report.html', context_instance=RequestContext(request))


def holiday_report_ajax_generator(request):

    now = datetime.datetime.now()

    # Fucking spaghetti code. Die in a fire bitch.
    type = Internal.objects.get(Name='Holiday')
    workflow = Workflow.objects.get(name='Timesheet')
    status = State.objects.filter(workflow=workflow).exclude(name="Deleted").exclude(name="Rejected")#|Q(name="New")|Q(name="Approved"))

    resources = InternalTimeSheet.objects.filter(Internal=type, Status__in=status, InternalDueDate__year=now.year).values_list('User__id',flat=True).distinct()

    holiday_list = []

    for resource in resources:
        def dict(**kwargs): return kwargs
        single_resource = User.objects.get(pk=int(resource))

        single_holidays = construct_holiday_series(single_resource, now.year)

        if all(not d for d in single_holidays):
            pass
        else:
            series = []
            blocks = []
            for holiday in single_holidays:
                date = holiday.get('InternalDueDate')
                day = '%02d' % date.day
                month = '%02d' % date.month
                date_construct = str(date.year)+', '+ str(day)+', '+ str(month)
                holiday_block = dict(id=holiday.get('id'), start=date_construct, end=date_construct)
                blocks.append(holiday_block)

            blocks_inner_dict = dict(name='', blocks=blocks)

            series.append(blocks_inner_dict)

            resource_line = dict(id=resource, name=single_resource.username, series=series)


            holiday_list.append(resource_line)


    json = holiday_list
    return HttpResponse(simplejson.dumps(json, cls=DjangoJSONEncoder))
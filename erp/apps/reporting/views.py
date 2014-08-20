import copy
import datetime
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from erp.apps.allocation.models import Allocation
from erp.apps.reporting.models import InternalReport
import time
from erp.apps.reporting.reports.holiday_report.holiday_report import holiday_report_generator, holiday_report_ajax_generator
from erp.apps.reporting.reports.internal_summary_report.internal_summary_report import internal_summary_report_generator

def company_dashboard(request):
    return render_to_response('reporting/company_dashboard.html', context_instance=RequestContext(request))

def internal_summary_report(request):
    return internal_summary_report_generator(request)

def holiday_report(request):
    if not request.is_ajax():
        return holiday_report_generator(request)
    else:
        return holiday_report_ajax_generator(request)

def holiday_ajax_report(request):
    return holiday_report_ajax_generator(request)
import datetime
import time
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from erp.apps.reporting.models import InternalReport
from erp.apps.reporting.reports.internal_summary_report.helper import xls_all_types

def internal_summary_report_generator(request):

    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    template_month = int(current_month - 1)
    template_year = current_year

    mnames = "January February March April May June July August September October November December"
    mnames = mnames.split()

    year = time.localtime()[0]

    #construct month list
    mlst = []
    for month in enumerate(mnames):
        mlst.append(dict(name=month))

    #construct year list
    ylst = []
    for y in [year-1, year, year+1]:
        ylst.append((y))

    if request.method != 'POST':
        internal_report_list = InternalReport.objects.filter(Month__month=current_month, Month__year=current_year).exclude()
    else:
        month = int(request.POST.get('month'))+1
        year = request.POST.get('year')

        template_month = month - 1
        template_year = int(year)

        internal_report_list = InternalReport.objects.filter(Month__month=month, Month__year=year)

        if request.POST.get('export'):
            object = internal_report_list
            return xls_all_types(request, internal_report_list)

    #@TODO Move render function to generic view and make this function only to return dict of values
    return render_to_response('reporting/internal_summary_report.html', {'ylst':ylst,
                                                               'mlst':mlst,
                                                               'template_year':template_year,
                                                               'template_month':template_month,
                                                               'internal_report_list':internal_report_list
    }, context_instance=RequestContext(request))
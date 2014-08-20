from django.http import HttpResponse
from django_excel_templates import *

def xls_all_types(request, internal_report_list):

    headerstyle = ExcelStyle()
    headerstyle.set_font(font_color='FFFFFF',bold=True)
    headerstyle.set_border(border_color='000000',border_style=5)
    headerstyle.set_pattern(pattern_color='000000',pattern=1)
    bodystyle = ExcelStyle(font_color='C0C0C0')
    altcolorstyle = ExcelStyle(font_color='00000',pattern_color='E7E7E7',pattern=1,border_color='000000',border_style=1,)

    formatter = ExcelFormatter()
    formatter.addHeaderStyle(headerstyle)
    formatter.addBodyStyle(bodystyle)
    formatter.addAlternateColorStyle(altcolorstyle)

    #formatter.addFormula('IntegerField','SUM') #BUG:  can't parse formula SUM(A0:A0)
    #formatter.addFormula('DateField','COUNT')
    #formatter.addFormula('SmallIntegerField,PositiveIntegerField','MAX')
    #formatter.addFormula('DecimalField','MIN')

    type_report = ExcelReport()
    type_report.addSheet("All Types")
    filter = ExcelFilter(exclude='id,Resource,Month,TravelSlovakia,TravelOutside,TravelMoney,AdvancePayment,Dietary',
        order='ResourceFullName,WorkDays,WorkHours,HolidayDays,IllnessDays,DoctorDays,DietaryTickets')

    type_report.addQuerySet(internal_report_list,REPORT_HORZ,formatter,filter)

    response = HttpResponse(type_report.writeReport(),mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=IQUAP_dochadzka_stravne_listky_TPA.xls'
    return response
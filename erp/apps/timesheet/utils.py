import codecs

from django.utils.encoding import smart_str

from erp.apps.timesheet.models import TimeSheet, Holiday, InternalTimeSheet


def get_timesheet_list(month, year, user):

    count = user.count()

    timesheet_list = TimeSheet.objects.filter(
        User__in = user,
        DueDate__month = month,
        DueDate__year = year
    ).exclude(
        Status__name = "Deleted"
    ).values(
        'id',
        'Project__Name',
        'DueDate',
        'Hours',
        'User__first_name',
        'User__last_name'
    )

    holiday_list = Holiday.objects.filter(
        Date__month = month,
        Date__year = year
    ).values(
        'Date',
        'Name'
    )

    internal_list = InternalTimeSheet.objects.filter(
        User__in = user,
        InternalDueDate__month = month,
        InternalDueDate__year = year,
    ).exclude(
        Status__name = "Deleted"
    ).values(
        'id',
        'Internal__Name',
        'InternalDueDate',
        'Status__name',
        'User__first_name',
        'User__last_name'
    )

    list = create_timesheet_json(timesheet_list, holiday_list, internal_list, count)

    return list

def create_timesheet_json(timesheet_list, holiday_list, internal_list, count):
    for timesheet in timesheet_list:
        timesheet['title'] = timesheet.pop('Project__Name')
        timesheet['start'] = timesheet.pop('DueDate')
        timesheet['color'] = '#3366cc'
        timesheet['className'] = 'timesheet'
        timesheet['title'] += ' - '+str(timesheet['Hours'])
        if count > 1:
            username = unicode(timesheet['User__first_name']) + ' ' + unicode(timesheet['User__last_name'])
            timesheet['title'] = username + ' - ' + timesheet.pop('title')
        timesheet.pop('Hours')

    for holiday in holiday_list:
        holiday['title'] = holiday.pop('Name')
        holiday['start'] = holiday.pop('Date')
        holiday['className'] = 'internal'
        holiday['color'] = '#d42020'

    for internal in internal_list:
        internal['title'] = internal.pop('Internal__Name')
        internal['start'] = internal.pop('InternalDueDate')
        internal['className'] = 'internal'
        if internal['title'] == 'Holiday' : internal['color'] = '#765300'
        if internal['title'] == 'Holiday' and internal['Status__name'] == 'Approved' : internal['color'] = '#327542'
        if internal['title'] == 'Holiday' and internal['Status__name'] == 'Rejected' : internal['color'] = '#5a3031'
        if count > 1:
            username = unicode(internal['User__first_name']) + ' ' + unicode(internal['User__last_name'])
            internal['title'] = username + ' - ' + internal.pop('title')

    merged_list = list(timesheet_list) + list(holiday_list) + list(internal_list)

    return merged_list
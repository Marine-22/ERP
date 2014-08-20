from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from dateutil import easter
import datetime
from conf import holidays
from erp.apps.timesheet.models import Holiday

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
        )
    help = 'Help text goes here'

    def handle(self, **options):

        non_working_days = holidays.holidays
        now = datetime.datetime.now()
        current_month = now.month
        current_year = now.year

        easter_day = easter.easter(current_year, method=3)
        good_firday = easter_day - datetime.timedelta(8 - easter_day.weekday())
        easter_monday = easter_day + datetime.timedelta(7 - easter_day.weekday())

        for item in non_working_days:
            print item[0]

            if item[0] == 'Good Friday':
                print good_firday
            elif item[0] == 'Easter day':
                print easter_day
            elif item[0] == 'Easter Monday':
                print easter_monday
            else:
                print datetime.date(current_year, item[1], item[2])

            print '***'

            try:
                if item[0] == 'Good Friday':
                    holiday_object = Holiday.objects.get(Name=item[0], Date=good_firday)
                elif item[0] == 'Easter day':
                    holiday_object = Holiday.objects.get(Name=item[0], Date=easter_day)
                elif item[0] == 'Easter Monday':
                    holiday_object = Holiday.objects.get(Name=item[0], Date=easter_monday)
                else:
                    holiday_object = Holiday.objects.get(Name=item[0], Date=datetime.date(current_year, item[1], item[2]))

                print item[0]
                print 'exists'
                print '++++++++++++++++++++++++++++++++++++++++++++++++'

            except Holiday.DoesNotExist:
                if item[0] == 'Good Friday':
                    holiday_object = Holiday.objects.create(Name=item[0], Date=good_firday)
                elif item[0] == 'Easter day':
                    holiday_object = Holiday.objects.create(Name=item[0], Date=easter_day)
                elif item[0] == 'Easter Monday':
                    holiday_object = Holiday.objects.create(Name=item[0], Date=easter_monday)
                else:
                    holiday_object = Holiday.objects.create(Name=item[0], Date=datetime.date(current_year, item[1], item[2]))

                holiday_object.save()
                print item[0]
                print 'created'
                print '************************************************'

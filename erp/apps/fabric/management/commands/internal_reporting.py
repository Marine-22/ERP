import datetime
from optparse import make_option
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand

from erp.apps.fabric.views import createInternalReport


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
        date = datetime.datetime.now()

        delta = relativedelta(months=1)
        last_month = date - delta

        createInternalReport(date)
        createInternalReport(last_month)
        print 'Done'

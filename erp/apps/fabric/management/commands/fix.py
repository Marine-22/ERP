import datetime
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from erp.apps.timesheet.models import TimeSheet, InternalTimeSheet
from erp.libs.workflows.models import State, Workflow, Transition
from erp.libs import workflows


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
        )
    help = 'Help text goes here'

    def handle(self, **options):

        transition = Transition.objects.get(name="ApproveTimesheet")

        timesheet = InternalTimeSheet.objects.filter(InternalDueDate__lte=datetime.datetime.now())

        for item in timesheet:
            workflows.utils.do_transition(item, transition, User.objects.get(pk=1))

            item.Status = transition.destination
            item.save()
            print item.InternalDueDate
            print 'Done'
            print '*********************************'
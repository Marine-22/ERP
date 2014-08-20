from optparse import make_option
import datetime
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models.aggregates import Sum
from core.master.allocation.models import Allocation
from core.master.project.models import Project
from core.master.reporting.generic import report_resource_allocation
from core.master.reporting.models import WeeklyProjectReport
from core.master.timesheet.models import TimeSheet
from modules.workflows.models import State, Workflow

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
        )
    help = 'Help text goes here'

    def handle(self, **options):
        active_project_status = State.objects.get(name='In progress', workflow=Workflow.objects.get(name='Project'))
        projects = Project.objects.filter(Status=active_project_status)

        now = datetime.datetime.now()

        dayofWeek = [0, 1, 2, 3, 4, 5, 6]

        current_day = dayofWeek[date.weekday(now)]

        negative_delta = timedelta(days=current_day)
        positive_delta = timedelta(days=6-current_day)

        first_day = now - negative_delta
        last_day = now + positive_delta

        first_day = datetime.date(first_day.year, first_day.month, first_day.day)
        last_day = datetime.date(last_day.year, last_day.month, last_day.day)

        for project in projects:
            allocations = Allocation.objects.filter(Project=project).values('Resource')
            resources = User.objects.filter(pk__in=allocations)

            print resources

            allocations_absolute = TimeSheet.objects.filter(Project=project,DueDate__range=(first_day,last_day)).aggregate(total=Sum('Hours'))

            if allocations_absolute.get('total') is not None:
                try:
                    report = WeeklyProjectReport.objects.get(Project=project, Week__range=(first_day,last_day))

                    for resource in resources:
                        singularity = report_resource_allocation(project, resource, report, first_day, last_day, allocations_absolute)
                        print singularity
                        print '--------------'

                except WeeklyProjectReport.DoesNotExist:
                    report = WeeklyProjectReport.objects.create(Project=project,Week=now)
                    report.save()

                    for resource in resources:
                        singularity = report_resource_allocation(project, resource, report, first_day, last_day, allocations_absolute)
                        print singularity
                        print '--------------'
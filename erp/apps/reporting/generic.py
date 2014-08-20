from django.db.models.aggregates import Sum
from erp.apps.reporting.models import WeeklyProjectReportResource
from erp.apps.timesheet.models import TimeSheet

def report_resource_allocation(project, resource, report, first_day, last_day, allocations_absolute):
    allocation_percent = TimeSheet.objects.filter(DueDate__range=(first_day, last_day),Project=project,User=resource).aggregate(total=Sum('Hours'))

    if allocation_percent.get('total') is not None:
        try:
            singularity = WeeklyProjectReportResource.objects.get(Resource=resource,Report=report)
            singularity.AllocationManday = allocation_percent.get('total')
            singularity.AllocationPercent = allocation_percent.get('total')/allocations_absolute.get('total')*100
            singularity.save()
        except WeeklyProjectReportResource.DoesNotExist:
            singularity = WeeklyProjectReportResource.objects.create(Report=report,
                Resource=resource,
                AllocationPercent=allocation_percent.get('total')/allocations_absolute.get('total')*100,
                AllocationManday=allocation_percent.get('total'))
            singularity.save()
        singularity = allocation_percent.get('total')
    else:
        singularity = None

    return singularity
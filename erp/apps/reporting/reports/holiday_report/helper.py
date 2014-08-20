from django.db.models.query_utils import Q
from erp.apps.internal.models import Internal
from erp.apps.timesheet.models import InternalTimeSheet
from erp.libs.workflows.models import Workflow, State

#@TODO: Some day move the generic selects to a higher level so they dont run each time a cycle is made. Right now im to lazy and dont give a shit to do it.
def construct_holiday_series(user, year):
    type = Internal.objects.get(Name='Holiday')
    workflow = Workflow.objects.get(name='Timesheet')
    status = State.objects.filter(workflow=workflow).exclude(name="Deleted").exclude(name="Rejected")#|Q(name="New")|Q(name="Approved"))
    holidays = InternalTimeSheet.objects.filter(Status__in=status, User=user, InternalDueDate__year=year, Internal=type).values('id','InternalDueDate')
    return holidays
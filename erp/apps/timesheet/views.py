from datetime import timedelta
import datetime
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.utils import simplejson
import time

from erp.apps.timesheet.forms.internal import InternalForm
from erp.apps.timesheet.forms.timesheet import TimeSheetForm

from erp.apps.timesheet.utils import get_timesheet_list

from erp.apps.timesheet.models import TimeSheet, InternalTimeSheet, Workshop
from erp.libs.workflows import utils
from erp.libs import workflows
from erp.libs.workflows.models import Workflow, Transition, State


def timesheet(request):
    """
    Default view that renders calendar
    """
    return render(
        request,
        'timesheet/timesheet.html'
    )


def timesheet_all(request):
    """
    Default view that renders calendar for all employees; Houston
    we need a better solution here
    """
    return render(
        request,
        'timesheet/timesheet_all.html'
    )


def timesheet_form(request):
    """
    View that serves forms for creating a new instance of TimeSheet or Internal object
    """
    timsheetForm = TimeSheetForm()
    internalForm = InternalForm()

    return render(
        request,
        'timesheet/forms/add.html',
        {
            'timsheetForm':timsheetForm,
            'internalForm':internalForm
        }
    )


def timesheet_edit_form(request, type, id):
    """
    View that serves forms for creating a new instance of TimeSheet or Internal object
    """
    if type == 'timesheet':
        timesheet = TimeSheet.objects.get(pk=int(id))
        editForm = TimeSheetForm(
                initial = {
                    'dueDate':timesheet.DueDate,
                    'hours':timesheet.Hours,
                    'partner':timesheet.Partner,
                    'project':timesheet.Project,
                    'phase':timesheet.Phase,
                    'activity':timesheet.Activity
                })
    else:
        timesheet = InternalTimeSheet.objects.get(pk=int(id))
        editForm = InternalForm(
                initial = {
                    'dueDate':timesheet.InternalDueDate,
                    'hours':timesheet.Hours,
                    'internal':timesheet.Internal,
                    'activity':timesheet.Activity
                })
    return render(
            request,
            'timesheet/forms/edit.html',
            {
                'editForm':editForm,
                'type':type,
                'timesheet':timesheet
            })


def form_save(request, type=None, id=None):
    """
    View to save the timesheet form
    """
    if type == 'timesheet':
        currentForm = TimeSheetForm(request.POST)
    else:
        currentForm = InternalForm(request.POST)
    if currentForm.is_valid():
        currentForm.save(request.user, id)
    # Generally, the ajax call after submitting the form will
    # refetch events so no big deal if we return something
    # meaningless here
    return HttpResponse('1')


# View that serves list of all timesheets for the current user
def get_timesheet(request, argument=None):
    if argument is None:
        user = User.objects.filter(pk=request.user.id)
    else:
        user = User.objects.all().exclude(groups__name='Ex-employee')
    epoch_month = time.gmtime(float(request.REQUEST.get('start')))
    if epoch_month.tm_mon == 12:
        month = 1
        year = epoch_month.tm_year+1
    else:
        month = epoch_month.tm_mon+1
        year = epoch_month.tm_year
    response = get_timesheet_list(month,year,user)
    return HttpResponse(simplejson.dumps(list(response), cls=DjangoJSONEncoder))


# View that is responsible for cloning the timesheet
def clone_timesheet(request):
    user = request.user

    event_id = request.POST.get('id')
    delta = int(request.POST.get('delta'))
    type = request.POST.get('type[]')

    if type == 'timesheet':
        event = TimeSheet.objects.get(pk=int(event_id))
    if type == 'internal':
        event = InternalTimeSheet.objects.get(pk=int(event_id))

    workflow = Workflow.objects.get(name='Timesheet')

    new_delta = 1
    while delta != 0:
        if type == 'timesheet':
            item = TimeSheet(Activity=event.Activity, Hours=event.Hours, Phase=event.Phase, Project=event.Project, User=event.User, DueDate=event.DueDate+timedelta(days=new_delta), Partner=event.Partner)
            item.save()
        if type == 'internal':
            item = InternalTimeSheet(Activity=event.Activity, Hours=event.Hours, Internal=event.Internal, User=event.User, InternalDueDate=event.InternalDueDate+timedelta(days=new_delta))
            item.save()

        #assign WF and set status
        utils.set_workflow(item, workflow)
        state = utils.get_state(item)
        item.Status = state
        item.save()

        delta = delta - 1
        new_delta += 1

    json = 'Success'

    return HttpResponse(simplejson.dumps(list(json), cls=DjangoJSONEncoder))

# View for approving the timesheet
def timesheet_approval(request):
    if request.method != 'POST':

        timesheet_list = InternalTimeSheet.objects.filter(Status__name='New', Internal__Name='Holiday').values('User__id').distinct()
        user_list = User.objects.filter(id__in=timesheet_list).exclude(groups__name='Ex-employee').order_by('first_name')

        for user in user_list:
            count = InternalTimeSheet.objects.filter(Status__name='New', Internal__Name='Holiday', User=user).count()
            user.__dict__['count'] = count

        return render(
            request,
            'timesheet/approval.html',
            {
                'user_list':user_list
            }
        )

    else:
        internal_list = request.POST.getlist('internal')
        transition = Transition.objects.get(name=request.POST.get('action_type'))

        for item in internal_list:
            internal = InternalTimeSheet.objects.get(pk=int(item))
            workflows.utils.do_transition(internal, transition, request.user)

            internal.Status = transition.destination
            internal.save()

        return HttpResponseRedirect(reverse('approveTimesheet'))

# View that will server all unapproved timesheets
def timesheet_approval_fetch(request, id=None):
    timesheet_list = InternalTimeSheet.objects.filter(Status__name='New', Internal__Name='Holiday', User__id=int(id)).order_by('InternalDueDate')

    return render(
        request,
        'timesheet/approval_single.html',
        {
            'timesheet_list':timesheet_list
        }
    )

def add_workshop(request):
    if request.method == 'POST':
        item = WorkshopForm(request.POST).save()

        workflow = Workflow.objects.get(name='Workshop')
        utils.set_workflow(item, workflow)

        state = utils.get_state(item)
        item.Status = state
        item.save()

        title = str(item.Ws_Partner)+' - '+str(item.Hours)

        json_list = {'title':title, 'year':item.DueDate.year, 'month':item.DueDate.month-1, 'day':item.DueDate.day, 'id':item.id, 'color':'#21aa38','className':'workshop'}
        return HttpResponse(simplejson.dumps(json_list))

def edit(request, type, id):
    if type == 'internal':
        internal = InternalTimeSheet.objects.get(pk=int(id))
        user = internal.User
        status = internal.Status
        if request.method != 'POST':
            form = InternalForm(instance=internal)
            return render(
                    request,
                    'timesheet/int_edit.html',
                    {
                        'form':form,
                        'internal':internal
                    })
        else:
            item = InternalForm(request.POST, instance=internal).save(commit=False)
            item.User = user
            item.Status = status
            item.save()
            json_list = {'title':item.Internal.Name, 'year':item.InternalDueDate.year, 'month':item.InternalDueDate.month-1, 'day':item.InternalDueDate.day, 'id':item.id}
            return HttpResponse(simplejson.dumps(json_list))
    elif type == 'timesheet':
        timesheet = TimeSheet.objects.get(pk=int(id))
        user = timesheet.User
        status = timesheet.Status
        if request.method != 'POST':
            form = TimeSheetForm(instance=timesheet)
            return render_to_response('timesheet/ts_edit.html', {'form':form,
                                                                 'timesheet':timesheet
            }, context_instance=RequestContext(request))
        else:
            item = TimeSheetForm(request.POST, instance=timesheet).save(commit=False)
            item.User = user
            item.Status = status
            item.save()

            json_list = {'title':item.Project.Name, 'year':item.DueDate.year, 'month':item.DueDate.month-1, 'day':item.DueDate.day, 'id':item.id}
            return HttpResponse(simplejson.dumps(json_list))

def delete(request, type, id):
    if type == 'timesheet':
        timesheet = TimeSheet.objects.get(pk=int(id))

        transition = Transition.objects.get(name="DeleteTimesheet")

        workflows.utils.do_transition(timesheet, transition, request.user)

        timesheet.Status = transition.destination
        timesheet.save()

        json_list = {'result':'success'}

        return HttpResponse(simplejson.dumps(json_list))

    elif type == 'internal':
        internal = InternalTimeSheet.objects.get(pk=int(id))

        transition = Transition.objects.get(name="DeleteInternal")

        workflows.utils.do_transition(internal, transition, request.user)

        internal.Status = transition.destination
        internal.save()

        json_list = {'result':'success'}
        return HttpResponse(simplejson.dumps(json_list))
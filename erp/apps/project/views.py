from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _

from erp.apps.project.models import Allocation
from erp.apps.project.forms.project import ProjectForm
from erp.apps.project.forms.phase import ProjectPhaseForm
from erp.apps.project.models import Project, ProjectPhase
from erp.apps.project.reports import reports
from erp.apps.timesheet.models import TimeSheet
from erp.libs.workflows import utils
from erp.libs.workflows.models import Workflow, State, Transition


def project_list(request, list_type):
    """
    Returns the list of projects based on request parameter. Can be
    either list of all projects (finished and active) or list of
    projects for the user that requested the view.
    """
    if list_type == 'active' or list_type == 'finished':
        if list_type == 'active':
            page_title = _(u'Active projects')
            project_list = Project.objects.filter(
                    Status__name='In progress').exclude(
                    Status__name='Deleted').order_by('Name')
        else:
            page_title = _(u'Finished projects')
            project_list = Project.objects.filter(
                    Status__name='Finished').exclude(
                    Status__name='Deleted').order_by('Name')
        return render(
                request,
                'project/list.html',
                {
                    'project_list':project_list,
                    'page_title':page_title
                })
    elif list_type == 'my_projects':
        # Get list of current allocations of a given resource.
        my_allocations = Allocation.objects.filter(
            Resource=request.user).values_list(
                'Project',flat=True)
        # Get list of projects on which user is given a role of a project manager.
        project_list = Project.objects.filter(
                ProjectManager = request.user,
                Status__name = 'In progress')
        # Get list of projects on which user is allocated.
        allocations = Project.objects.filter(
                pk__in=my_allocations,
                Status__name='In progress')
        # Get list of finished projects of the given user.
        finished_projects = Project.objects.filter(
                ProjectManager=request.user,
                Status__name='Finished')
        # Get list of finished allocations of given user.
        finished_allocations = Project.objects.filter(
                pk__in=my_allocations,
                Status__name='Finished')
        return render(
                request,
                'project/my.html',
                {
                    'project_list':project_list,
                    'allocations':allocations,
                    'finished_projects':finished_projects,
                    'finished_allocations':finished_allocations
                })


def project_details(request, id):
    """
    Returns details of the given project based on the id provided. Currently
    returns the following lists of values:
        - project details,
        - phases,
        - active phases,
        - finished phases,
        - deleted phases,
        - project allocations,
        - time consumption by all resources who work on project.
    """
    # Get the ptoject itself.
    project = Project.objects.get(
            pk=int(id))
    # Get all lists of phases.
    active_phases = ProjectPhase.objects.filter(
            Project=project,
            Status__name='In progress')
    finished_phases = ProjectPhase.objects.filter(
            Project=project,
            Status__name='Finished')
    deleted_phases = ProjectPhase.objects.filter(
            Project=project,
            Status__name='Deleted')
    # Create list of allocated resources for the given project.
    allocation_list = []
    list_of_allocated_users = Allocation.objects.filter(
            Project=project).values(
                'Resource__pk',
                'Resource__first_name',
                'Resource__last_name').distinct()
    for allocation in list_of_allocated_users:
        resource = User.objects.get(pk=int(allocation.get('Resource__pk')))
        single_allocation = Allocation.objects.filter(
                Project=project, Resource=resource)
        temp_allocations = {
                'user':allocation,
                'allocations':single_allocation,
                'count':single_allocation.count()}
        allocation_list.append(temp_allocations)
    # Create simple project report of how much time which resource spent
    # working on the project.
    resource_time_total = []
    users = TimeSheet.objects.filter(
            Project=project).values(
                'User__id').distinct()
    for item in users:
        user = User.objects.get(
                pk=item.get(
                    'User__id'))
        filter = TimeSheet.objects.filter(
                User=user,Project=project).aggregate(Sum('Hours'))
        resource_time_total.append(
            dict(name=user.first_name+' '+user.last_name,hours=filter))
    return render(
            request,
            'project/details/details.html',
            {
                'project':project,
                'active_phases':active_phases,
                'finished_phases':finished_phases,
                'deleted_phases':deleted_phases,
                'allocation_list':allocation_list,
                'resource_time_total':resource_time_total,
            })


def project_create(request):
    """
    Creates a brand new unspilled and 100% virgin version of the project.
    """
    if request.method != 'POST':
        form = ProjectForm()
        return render(
                request,
                'project/forms/project/add_project.html',
                    {
                    'form':form
                })
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():
            item = form.save()
            return HttpResponseRedirect(reverse(
                'core.master.project.views.project_details',
                args=(item.id,)))


def project_edit(request, id):
    """
    Edits the existing ptoject instance based on it's id.
    """
    project = Project.objects.get(pk=int(id))
    if request.method != 'POST':
        form = ProjectForm(initial={
                'name': project.Name,
                'project_client': project.ProjectClient,
                'start': project.Start,
                'end': project.End,
                'project_manager': project.ProjectManager,
                'quality_assurance':project.QualityAssurance,
                'price':project.Price,
                'segment':project.Segment,
                'type':project.Type})
        return render(
                request,
                'project/forms/project/edit_project.html',
                {
                    'project':project,
                    'form':form
                })
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(project_id=project.id)
        return HttpResponseRedirect(reverse(
                'project_details',
                args=(project.id,)))


def project_finish(request, id):
    project = Project.objects.get(pk=int(id))

    transition = Transition.objects.get(name='FinishProject')
    phase_transistion = Transition.objects.get(name='FinishPhase')

    utils.do_transition(project, transition, request.user)

    project.Status = transition.destination
    project.save()

    phases = ProjectPhase.objects.filter(Project=project)
    for item in phases:
        utils.do_transition(item, phase_transistion, request.user)

        item.Status = phase_transistion.destination
        item.save()

    return HttpResponseRedirect(reverse('project.views.project_details', args=(project.id,)))


def project_restart(request, id):
    project = Project.objects.get(pk=int(id))

    transition = Transition.objects.get(name='RestartProject')
    phase_transistion = Transition.objects.get(name='RestartPhase')
    deleted_phase = State.objects.get(name='Deleted', workflow=Workflow.objects.get(name='Phase'))

    utils.do_transition(project, transition, request.user)

    project.Status = transition.destination
    project.save()

    phases = ProjectPhase.objects.filter(Project=project).exclude(Status=deleted_phase)

    for item in phases:
        utils.do_transition(item, phase_transistion, request.user)

        item.Status = phase_transistion.destination
        item.save()

    return HttpResponseRedirect(reverse('project.views.project_details', args=(project.id,)))


def project_delete(request, id):
    project = Project.objects.get(pk=int(id))
    transition = Transition.objects.get(name='DeleteProject')

    utils.do_transition(project, transition, request.user)

    project.Status = transition.destination
    project.save()

    return HttpResponseRedirect(reverse('project.views.project_list', args=()))


def project_add_phase(request, id):
    project = Project.objects.get(pk=int(id))
    if request.method != 'POST':
        form = ProjectPhaseForm()
        return render_to_response('project/forms/phases/add_phase.html', {'form':form,
                                                         'project':project
        }, context_instance=RequestContext(request))
    else:
        item = ProjectPhaseForm(request.POST).save(commit=False)
        item.Project = project
        item.Partner = project.ProjectClient
        item.save()

        workflow = Workflow.objects.get(name='Phase')
        utils.set_workflow(item, workflow)

        state = utils.get_state(item)
        item.Status = state
        item.save()

        return HttpResponseRedirect(reverse('project_details', args=(project.id,)))


def project_edit_phase(request, id):
    phase = ProjectPhase.objects.get(pk=int(id))
    project = Project.objects.get(pk=int(phase.Project_id))
    if request.method != 'POST':
        form = ProjectPhaseForm(instance=phase)
        return render_to_response('project/forms/phases/edit_phase.html', {'form':form,
                                                         'phase':phase
        }, context_instance=RequestContext(request))
    else:
        item = ProjectPhaseForm(request.POST, instance=phase).save(commit=False)
        item.save()

        return HttpResponseRedirect(reverse('project_details', args=(project.id,)))


def project_finish_phase(request, id):
    phase = ProjectPhase.objects.get(pk=int(id))
    if request.method != 'POST':
        return render_to_response('project/forms/phases/finish_phase.html', {'phase':phase}, context_instance=RequestContext(request))
    else:
        transition = Transition.objects.get(name='FinishPhase')
        utils.do_transition(phase, transition, request.user)

        phase.Status = transition.destination
        phase.save()

        return HttpResponseRedirect(reverse('project_details', args=(phase.Project_id,)))


def project_delete_phase(request, id):
    phase = ProjectPhase.objects.get(pk=int(id))
    if request.method != 'POST':
        return render_to_response('project/forms/phases/delete_phase.html', {'phase':phase}, context_instance=RequestContext(request))
    else:
        project = Project.objects.get(pk=int(phase.Project_id))

        transition = Transition.objects.get(name='DeletePhase')
        utils.do_transition(phase, transition, request.user)

        phase.Status = transition.destination
        phase.save()

        return HttpResponseRedirect(reverse('project_details', args=(project.id,)))


def project_restart_phase(request, id):
    phase = ProjectPhase.objects.get(pk=int(id))
    if request.method != 'POST':
        return render_to_response('project/forms/phases/restart_phase.html', {'phase':phase}, context_instance=RequestContext(request))
    else:
        project = Project.objects.get(pk=int(phase.Project_id))

        transition = Transition.objects.get(name='RestartPhase')
        utils.do_transition(phase, transition, request.user)

        phase.Status = transition.destination
        phase.save()

        return HttpResponseRedirect(reverse('project_details', args=(project.id,)))


# TODO This one needs depreciation
def project_reports(request, id):
    project = Project.objects.get(pk=int(id))
    used_budget = reports.used_budget(project)
    free_budget = project.Price - used_budget
    resource_budget = reports.resource_budget_constumption(project)
    time_consumption = reports.time_consumption(project)

    used_budget = (u"%.15f" % used_budget).replace(',', '.')
    free_budget = (u"%.15f" % free_budget).replace(',', '.')

    #timesheets = TimeSheet.objects.filter(Project=project)

    return render_to_response('project/reports.html', {'project':project,
                                                       'used_budget':used_budget,
                                                       'free_budget':free_budget,
                                                       'resource_budget':resource_budget,
                                                       'time_consumption':time_consumption
    }, context_instance=RequestContext(request))
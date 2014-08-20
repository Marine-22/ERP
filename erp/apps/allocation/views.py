from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from erp.apps.allocation.forms import AllocationForm
from erp.apps.allocation.models import Allocation
from erp.apps.project.models import Project

def add_allocation(request, id):
    project = Project.objects.get(pk=int(id))
    if request.method != 'POST':
        form = AllocationForm()
        return render_to_response('project/forms/allocation/add_allocation.html', {'form':form, 'project':project}, context_instance=RequestContext(request))
    else:
        item = AllocationForm(request.POST).save(commit=False)
        item.Project = project
        item.save()
        return HttpResponseRedirect(reverse('project_details', args=(project.id,)))

def edit_allocation(request, id):
    allocation = Allocation.objects.get(pk=int(id))
    project = Project.objects.get(pk=int(allocation.Project_id))
    if request.method != 'POST':
        form = AllocationForm(instance=allocation)
        return render_to_response('allocation/edit_allocation.html', {'form':form, 'allocation':allocation}, context_instance=RequestContext(request))
    else:
        item = AllocationForm(request.POST, instance=allocation).save(commit=False)
        item.Project = project
        item.save()
        if request.environ.get('HTTP_REFERER').split('/')[-2] == 'resources':
            return HttpResponseRedirect(reverse('core.master.resources.views.resource_details', args=(item.Resource.id,)))
        else:
            return HttpResponseRedirect(reverse('core.master.project.views.project_details', args=(project.id,)))

def delete_allocation(request, id):
    allocation = Allocation.objects.get(pk=int(id))
    if request.method != 'POST':
        return render_to_response('allocation/delete_allocation.html', {'allocation':allocation}, context_instance=RequestContext(request))
    else:
        project = Project.objects.get(pk=int(allocation.Project_id))
        allocation.delete()
        return HttpResponseRedirect(reverse('core.master.project.views.project_details', args=(project.id,)))

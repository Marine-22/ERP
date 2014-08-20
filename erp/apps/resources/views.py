import datetime

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from erp.apps.project.models import Allocation, Project
from erp.apps.resources.models import UserProfile
from erp.apps.resources.forms.profile import ProfileForm


def resource_list(request):
    """
    Function will return the lsit of all resources separated into groups
    """
    users_list = []
    groups = Group.objects.all()

    for group in groups:
        group_list = User.objects.filter(groups=group).order_by('first_name')
        if group_list:
            users = {'id':group.id,'name':group.name,'users':group_list}
            users_list.append(users)

    return render(
            request,
            'resources/list.html',
            {
                'users_list': users_list
            })


def resource_create(request):
    """
    Function to create a new resource. This is still not implemented
    but I do promise that someday I will finish it.
    """
    return render(
            request,
            'resources/create.html')


def resource_details(request, id):
    resource = User.objects.get(pk=int(id))
    project_management = Project.objects.filter(ProjectManager=resource)
    now = datetime.datetime.now()
    past_allocations = Allocation.objects.filter(Resource=resource, End__lt=now)
    current_allocations = Allocation.objects.filter(Resource=resource, End__gte=now)
    return render(
            request,
            'resources/details.html',
            {
                'resource': resource,
                'past_allocations': past_allocations,
                'current_allocations': current_allocations,
                'project_management': project_management
            })


def resource_edit(request, id):
    singleUser = User.objects.get(pk=int(id))
    userProfile = UserProfile.objects.get(pk=int(id))
    if request.method != 'POST':
        # Fill the form with the data
        profileForm = ProfileForm(initial = {
            'firstName':singleUser.first_name,
            'lastName':singleUser.last_name,
            'userEmail':singleUser.email,
            'userPhone':userProfile.Phone,
            'userLdap':singleUser.username,
            'userRoles':singleUser.groups
        })

        return render(
                request,
                'resources/forms/profile.html',
                {
                    'profileForm':profileForm
                })
    else:
        UserForm(request.POST, instance=resource).save()
        ProfileForm(request.POST, instance=profile).save()
        return HttpResponseRedirect(reverse('core.master.resources.views.resource_details', args=(profile.id,)))

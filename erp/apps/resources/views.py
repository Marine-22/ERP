import datetime

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse

from erp.apps.project.models import Allocation, Project
from erp.apps.resources.models import UserProfile
from erp.apps.resources.forms.profile import ProfileForm
from erp.apps.resources.forms.userforms import UserUpdateForm, UserCreateForm



# becouse python cant work with object itself. dunno why o.O
class A(object):
    pass



# user je prihlaseny pouzivatel, user_id je id pouzivatela, ktory sa zobrazuje v GUI
def get_user_permissions(user, user_id=None):
    if user_id:
        usr = User.objects.get(id=user_id)
    else:
        usr = A()
    usr.canEdit = user.is_superuser or (user.id == int(user_id) if user_id else False)
    usr.officeManager = False
    for group in user.groups.all():
        if group.name == 'Office manager': # office manager ma prava navyse
            usr.officeManager = True
    usr.isSuperLoggedIn = user.is_superuser
    usr.needOldPassword = (user.id == int(user_id) if user_id else True)
    return usr

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
                'userDetail': get_user_permissions(request.user),
                'users_list': users_list
            })


def resource_create(request):
    usr = A()
    usr.action = 'create'
    usr.first_name = _('New')
    usr.last_name = _('User')

    if request.method != 'POST':
        form = UserCreateForm()
        form.setAccess(request.user.is_superuser)
        return TemplateResponse(request, 'resources/manage_user.html', 
            {'userDetail':usr, 
             'userForm':form})
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('resource_details', args=(user.id,)))
        else:
            form.setAccess(request.user.is_superuser)
            return TemplateResponse(request, 'resources/manage_user.html', 
                {'userDetail':usr,
                 'userForm':form})


def resource_details(request, id):
    resource = get_user_permissions(request.user, id)
    resource.action = 'detail'
    project_management = Project.objects.filter(ProjectManager=resource)
    now = datetime.datetime.now()
    past_allocations = Allocation.objects.filter(Resource=resource, End__lt=now)
    current_allocations = Allocation.objects.filter(Resource=resource, End__gte=now)
    return render(
            request,
            'resources/manage_user.html',
            {
                'userDetail': resource,
                'past_allocations': past_allocations,
                'current_allocations': current_allocations,
                'project_management': project_management
            })



def resource_update(request, id):
    usr = get_user_permissions(request.user, id)
    usr.action = 'change' # riadenie v template
    if request.method != 'POST':
        form = UserUpdateForm(instance=usr)
        form.add_fields(usr)
        form.setAccess(usr)
        return TemplateResponse(request, 'resources/manage_user.html', 
            {'userDetail':usr, 
             'userForm':form})
    else:
        form = UserUpdateForm(request.POST, instance=usr)
        if form.is_valid(usr.needOldPassword):
            form.save()
            return HttpResponseRedirect(reverse('resource_details', args=(id,)))
        else:
            form.add_fields(usr)
            return TemplateResponse(request, 'resources/manage_user.html', 
                {'userDetail':usr,
                 'userForm':form})
"""
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
"""
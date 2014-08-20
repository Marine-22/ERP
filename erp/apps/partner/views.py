from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext

from erp.apps.resources.models import UserProfile
from erp.apps.partner.forms.partner import PartnerForm
from erp.apps.partner.models import Partner, PartnerContact
from erp.apps.project.models import Project


def partner_list(request):
    """
    Returns list of partners ordered by name, alphabetically
    """
    partner_list = Partner.objects.all().order_by('PartnerName')
    return render(
            request,
            'partner/list.html',
            {
                'partner_list': partner_list
            })


def partner_details(request, id):
    """
    Returns all the details of the selected partner among with active
    projects, contacts and resources that belong to the partner
    """
    partner = Partner.objects.get(pk=int(id))
    active_projects = Project.objects.filter(
            ProjectClient=partner,
            Status__name='In progress')
    finished_projects = Project.objects.filter(
            ProjectClient=partner,
            Status__name='In progress')
    contacts = PartnerContact.objects.filter(Partner=partner)
    resources = UserProfile.objects.filter(Partner=partner)
    return render(
            request,
            'partner/details/details.html',
            {
                'partner': partner,
                'active_projects': active_projects,
                'finished_projects': finished_projects,
                'contacts': contacts,
                'resources': resources
            })


def partner_create(request):
    """
    Provides partner form to create a new partner instance
    """
    if request.method != 'POST':
        form = PartnerForm()
        return render(
                request,
                'partner/forms/add_partner.html',
                {
                    'form':form
                })
    else:
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save()
            return HttpResponseRedirect(
                    reverse('partner_details', args=(partner.id,)))


def partner_edit(request, id):
    partner = Partner.objects.get(pk=int(id))
    if request.method != 'POST':
        form = PartnerForm()
        return render(
                request,
                'partner/forms/edit_partner.html',
                {
                    'form':form,
                    'partner':partner
                })
    else:
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save(partner_id=partner.id)
            return HttpResponseRedirect(
                    reverse('partner_details', args=(partner.id,)))


def partner_add_contact(request, id):
    partner = Partner.objects.get(pk=int(id))
    if request.method != 'POST':
        form = PartnerContactForm()
        return render_to_response('partner/contact_form.html', {'form':form,
                                                                'partner':partner
        }, context_instance=RequestContext(request))
    else:
        contact = PartnerContactForm(request.POST).save(commit=False)
        contact.Partner = partner
        contact.save()
        return HttpResponseRedirect(reverse('partner.views.partner_details', args=(partner.id,)))

def partner_edit_contact(request, id):
    contact = PartnerContact.objects.get(pk=int(id))
    form = PartnerContactForm(instance=contact)
    if request.method != 'POST':
        return render_to_response('partner/contact_form.html', {'contact':contact,
                                                                   'form':form
        }, context_instance=RequestContext(request))
    else:
        item = PartnerContactForm(request.POST, instance=contact).save()
        return HttpResponseRedirect(reverse('partner.views.partner_details', args=(item.Partner.id,)))

def partner_delete_contact(request, id):
    contact = PartnerContact.objects.get(pk=int(id))
    project = contact.Partner_id
    contact.delete()
    return HttpResponseRedirect(reverse('partner.views.partner_details', args=(project,)))
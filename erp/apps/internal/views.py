from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from erp.apps.internal.forms import InternalForm
from erp.apps.internal.models import Internal
from erp.apps.django_excel_templates import *
import datetime
import time

def internal_list(request):
    internals = Internal.objects.all()
    return render_to_response('internal/list.html', {'internals':internals}, context_instance=RequestContext(request))

def internal_create(request):
    if request.method != 'POST':
        form = InternalForm()
        return render_to_response('internal/form.html', {'form':form}, context_instance=RequestContext(request))
    else:
        internal = InternalForm(request.POST)
        internal.save()
        return HttpResponseRedirect(reverse('internal.views.internal_list', args=()))

def internal_edit(request, id):
    internal = Internal.objects.get(pk=int(id))
    if request.method != 'POST':
        form = InternalForm(instance = internal)
        return render_to_response('internal/form.html', {'form':form,
                                                         'internal':internal
        }, context_instance=RequestContext(request))
    else:
        item = InternalForm(request.POST, instance=internal).save(commit=False)
        item.save()
        return HttpResponseRedirect(reverse('internal.views.internal_list', args=()))

def internal_delete(request, id):
    internal = Internal.objects.get(pk=int(id))
    internal.delete()
    return HttpResponseRedirect(reverse('internal.views.internal_list', args=()))
# -*- coding: utf-8 -*-
import types

from django.core.urlresolvers import get_callable
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import simplejson
from django.shortcuts import get_object_or_404, render_to_response 
from django.template import RequestContext, Context, loader
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.contrib import messages

from erp.apps.simplewiki.models import *
from erp.apps.simplewiki.settings import *

def view(request, slug):

    (article, err) = fetch_from_url(request, slug)
    if err:
        return err
        
    perm_err = check_permissions(request, article, check_read=True)
    if perm_err:
        return perm_err
    c = RequestContext(request, {'wiki_article': article,
                                 'wiki_write': article.can_write_l(request.user),
                                 'wiki_attachments_write': article.can_attach(request.user),
                                 } ) 
    return render_to_response('simplewiki_view.html', c)

def root_redirect(request):
    """
    Reason for redirecting:
    The root article needs to to have a specific slug
    in the URL, otherwise pattern matching in urls.py will get confused.
    I've tried various methods to avoid this, but depending on Django/Python
    versions, regexps have been greedy in two different ways.. so I just
    skipped having problematic URLs like '/wiki/_edit' for editing the main page.
    #benjaoming
    """
    try:
        root = Article.get_root()
    except RootArticleNotFound, e:
        err = not_found(request, WIKI_ROOT_SLUG)
        return err

    return HttpResponseRedirect(reverse('wiki_view', args=(root.slug,)))

@transaction.commit_on_success
def create(request, slug):
    
    url_path = get_url_path(slug)

    if request.method == 'POST':
        f = CreateArticleForm(request.POST)
        if f.is_valid():
            article = Article()
            article.slug = url_path[-1]
            if not request.user.is_anonymous():
                article.created_by = request.user
            article.title = f.cleaned_data.get('title')
            a = article.save()
            new_revision = f.save(commit=False)
            if not request.user.is_anonymous():
                new_revision.revision_user = request.user
            new_revision.article = article
            new_revision.save()
            return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))
    else:
        if Article.objects.filter(slug__iexact=url_path[-1]).exists():
            messages.add_message(request, messages.ERROR,
                "An article with the '%s' slug already exists." % url_path[-1])
            return HttpResponseRedirect(reverse('wiki_view', args=(Article.get_root(),)))
        f = CreateArticleForm(initial={'title':request.GET.get('wiki_article_name', url_path[-1]),
                                       'contents':_('Headline\n===\n\n')})
        
    c = RequestContext(request, {'wiki_form': f,
                                 'wiki_write': True,
                                 })

    return render_to_response('simplewiki_create.html', c)

@transaction.commit_on_success
def edit(request, slug):

    (article, err) = fetch_from_url(request, slug)
    if err:
        return err

    # Check write permissions
    perm_err = check_permissions(request, article, check_write=True, check_locked=True)
    if perm_err:
        return perm_err

    if WIKI_ALLOW_TITLE_EDIT:
        EditForm = RevisionFormWithTitle
    else:
        EditForm = RevisionForm
    
    if request.method == 'POST':
        f = EditForm(request.POST)
        if f.is_valid():
            new_revision = f.save(commit=False)
            new_revision.article = article
            # Check that something has actually been changed...
            if not new_revision.get_diff():
                return (None, HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),))))
            if not request.user.is_anonymous():
                new_revision.revision_user = request.user
            new_revision.save()
            if WIKI_ALLOW_TITLE_EDIT:
                new_revision.article.title = f.cleaned_data['title']
                new_revision.article.save()
            return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))
    else:
        f = EditForm({'contents': article.current_revision.contents, 'title': article.title})
    c = RequestContext(request, {'wiki_form': f,
                                 'wiki_write': True,
                                 'wiki_article': article,
                                 'wiki_attachments_write': article.can_attach(request.user),
                                 })

    return render_to_response('simplewiki_edit.html', c)

@transaction.commit_on_success
def history(request, slug, page=1):

    (article, err) = fetch_from_url(request, slug)
    if err:
        return err

    perm_err = check_permissions(request, article, check_read=True)
    if perm_err:
        return perm_err

    page_size = 10
    
    try:
        p = int(page)
    except ValueError:
        p = 1
   
    history = Revision.objects.filter(article__exact = article).order_by('-counter')
    
    if request.method == 'POST':
        if request.POST.__contains__('revision'):
            perm_err = check_permissions(request, article, check_write=True, check_locked=True)
            if perm_err:
                return perm_err
            try:
                r = int(request.POST['revision'])
                article.current_revision = Revision.objects.get(id=r)
                article.save()
            except:
                pass
            finally:
                return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))
    
    page_count = (history.count()+(page_size-1)) / page_size
    if p > page_count:
        p = 1
    beginItem = (p-1) * page_size
    
    next_page = p + 1 if page_count > p else None
    prev_page = p - 1 if p > 1 else None
    
    c = RequestContext(request, {'wiki_page': p,
                                 'wiki_next_page': next_page,
                                 'wiki_prev_page': prev_page,
                                 'wiki_write': article.can_write_l(request.user),
                                 'wiki_attachments_write': article.can_attach(request.user),
                                 'wiki_article': article,
                                 'wiki_history': history[beginItem:beginItem+page_size],})

    return render_to_response('simplewiki_history.html', c)

def search_articles(request, slug):
    # blampe: We should check for the presence of other popular django search
    # apps and use those if possible. Only fall back on this as a last resort.
    # Adding some context to results (eg where matches were) would also be nice.
    
    # todo: maybe do some perm checking here
    
    if request.method == 'POST':
        querystring = request.POST['value'].strip()
        if querystring:
            results = Article.objects.all()
            for queryword in querystring.split():
                # Basic negation is as fancy as we get right now
                if queryword[0] == '-' and len(queryword) > 1:
                    results._search = lambda x: results.exclude(x)
                    queryword = queryword[1:]
                else:
                    results._search = lambda x: results.filter(x)
                    
                results = results._search(Q(current_revision__contents__icontains = queryword) | \
                                          Q(title = queryword))
        else:
            # Need to throttle results by splitting them into pages...
            results = Article.objects.all()

        if results.count() == 1:
            messages.add_message(request, messages.INFO,
                "Showing this page because it was the only page found for the entered query.")
            return HttpResponseRedirect(reverse('wiki_view', args=(results[0].get_url(),)))
        else:        
            c = RequestContext(request, {'wiki_search_results': results,
                                         'wiki_search_query': querystring})
            return render_to_response('simplewiki_searchresults.html', c)
    
    return view(request, slug)

def search_related(request, slug):

    (article, err) = fetch_from_url(request, slug)
    if err:
        return err

    perm_err = check_permissions(request, article, check_read=True)
    if perm_err:
        return perm_err

    search_string = request.GET.get('query', None)
    self_pk = request.GET.get('self', None)
    if search_string:
        results = []
        related = Article.objects.filter(title__istartswith = search_string)
        others = article.related.all()
        if self_pk:
            related = related.exclude(pk=self_pk)
        if others:
            related = related.exclude(related__in = others)
        related = related.order_by('title')[:10]
        for item in related:
            results.append({'id': str(item.id),
                            'value': item.title,
                            'info': item.get_url()})
    else:
        results = []
    
    json = simplejson.dumps({'results': results})
    return HttpResponse(json, mimetype='application/json')

@transaction.commit_on_success
def add_related(request, slug):

    (article, err) = fetch_from_url(request, slug)
    if err:
        return err
    
    perm_err = check_permissions(request, article, check_write=True, check_locked=True)
    if perm_err:
        return perm_err
    
    try:
        related_id = request.POST['id']
        rel = Article.objects.get(id=related_id)
        has_already = article.related.filter(id=related_id).count()
        if has_already == 0 and not rel == article:
            article.related.add(rel)
            article.save()
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))

@transaction.commit_on_success
def remove_related(request, slug, related_id):

    (article, err) = fetch_from_url(request, slug)
    if err:
        return err

    perm_err = check_permissions(request, article, check_write=True, check_locked=True)
    if perm_err:
        return perm_err

    try:
        rel_id = int(related_id)
        rel = Article.objects.get(id=rel_id)
        article.related.remove(rel)
        article.save()
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))

def random_article(request, slug):
    from random import randint
    num_arts = Article.objects.count()
    if num_arts == 0:
        return root_redirect(request)
    article = Article.objects.all()[randint(0, num_arts-1)]
    return HttpResponseRedirect(reverse('wiki_view', args=(article.get_url(),)))

def encode_err(request, url):
    return render_to_response('simplewiki_error.html',
                              RequestContext(request, {'wiki_err_encode': True}))
    
def not_found(request, slug):
    """Generate a NOT FOUND message for some URL"""
    return render_to_response('simplewiki_error.html',
                              RequestContext(request, {'wiki_err_notfound': True,
                                                       'wiki_url': slug}))

def get_url_path(url):
    """Return a list of all actual elements of a url, safely ignoring
    double-slashes (//) """
    return filter(lambda x: x!='', url.split('/'))

def fetch_from_url(request, url):
    """Analyze URL, returning the article and the articles in its path
    If something goes wrong, return an error HTTP response"""

    try:
        article = Article.objects.get(slug__iexact=url)
        return (article,  None)
    except:
        err = not_found(request, url)
        return (None, err)

def check_permissions(request, article, check_read=False, check_write=False, check_locked=False):
    read_err = check_read and not article.can_read(request.user)
    write_err = check_write and not article.can_write(request.user)
    locked_err = check_locked and article.locked

    if read_err or write_err or locked_err:
        c = RequestContext(request, {'wiki_article': article,
                                     'wiki_err_noread': read_err,
                                     'wiki_err_nowrite': write_err,
                                     'wiki_err_locked': locked_err,})
        # TODO: Make this a little less jarring by just displaying an error
        #       on the current page? (no such redirect happens for an anon upload yet)
        # benjaoming: I think this is the nicest way of displaying an error, but
        # these errors shouldn't occur, but rather be prevented on the other pages.
        return render_to_response('simplewiki_error.html', c)
    else:
        return None

####################
# LOGIN PROTECTION #
####################

if WIKI_REQUIRE_LOGIN_VIEW:
    view            = login_required(view)
    history         = login_required(history)
    search_related  = login_required(search_related)
    encode_err = login_required(encode_err)
    
if WIKI_REQUIRE_LOGIN_EDIT:
    create          = login_required(create)
    edit            = login_required(edit)
    add_related     = login_required(add_related)
    remove_related  = login_required(remove_related)

if WIKI_CONTEXT_PREPROCESSORS:
    settings.TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + WIKI_CONTEXT_PREPROCESSORS

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import uuid

from django.test import TestCase
from django.contrib.auth.models import User

from erp.apps.simplewiki.models import Article, Revision

class WikiBaseTest(TestCase):
    
    def _create_admin_user(self):
        admin = User.objects.create_user('admin', 'admin@example.com', 'admin')
        admin.is_staff = True
        admin.save()
    
    def _create_new_page(self, slug, title, contents):
        """
        Creates a page. An administrator user must be logged in.
        """
        articles = Article.objects.count()
        
        response = self.client.get('/wiki/%s/_create/' % slug)
        self.assertTemplateUsed(response, 'simplewiki_create.html')
        
        response = self.client.post('/wiki/%s/_create/' % slug, {
            'title': title,
            'contents': contents,
        })
        
        self.assertRedirects(response, '/wiki/%s' % slug)
        self.assertEqual(Article.objects.count(), articles+1)
        
        article = Article.objects.get(slug__iexact=slug)
        self.assertEqual(article.current_revision.contents, contents)

class TestEmptyWiki(WikiBaseTest):
    
    def setUp(self):
        self._create_admin_user()
    
    def test_create_initial_page(self):
        
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Revision.objects.count(), 0)
        
        # Home
        response = self.client.get('/')
        self.assertRedirects(response, '/wiki/', status_code=301)
        
        # /wiki/
        response = self.client.get('/wiki/')
        self.assertTemplateUsed(response, 'simplewiki_error.html')
        self.assertContains(response, "/wiki/mainpage/_create/")
        
        # /wiki/mainpage/_create/ - Anonymous
        response = self.client.get('/wiki/mainpage/_create/')
        self.assertRedirects(response, '/accounts/login/?next=/wiki/mainpage/_create/')
        
        # /wiki/mainpage/_create/ - as 'admin'
        self.client.login(username='admin', password='admin')
        self._create_new_page('mainpage', 'Some title', 'This is the content')

    def test_create_more_pages(self):
        self.client.login(username='admin', password='admin')
        self._create_new_page('mainpage', 'Some title', 'This is the content')
        self._create_new_page('mainpage2', 'Some title 2', 'This is the content 2')
        self._create_new_page(str(uuid.uuid4()), 'Some title', 'This is the content')

class TestBugs(WikiBaseTest):
    fixtures = ['mainpage.json']

    def setUp(self):
        self._create_admin_user()

    def test_detect_creation_of_duplicated_slug(self):
        self.client.login(username='admin', password='admin')
        
        slug = str(uuid.uuid4())
        self._create_new_page(slug, 'Some title', 'This is the content')

        response = self.client.get('/wiki/%s/_create/' % slug) # Try to create
        self.assertRedirects(response, '/wiki/mainpage')
        
        self.assertRaises(AssertionError, self._create_new_page, slug, 'Some title', 'This is the content')

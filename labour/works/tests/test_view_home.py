#test_view_home.py
from django.test import TestCase
from django.urls import reverse , resolve
from ..views import home
from ..models import Work

class HomeTests(TestCase):
    def setUp(self):
        self.work = Work.objects.create(name='Operator', description='Oper')
        url = reverse('home')
        self.response = self.client.get(url)
        
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_workers_page(self):
        work_workers_url = reverse('work_workers', kwargs={'pk': self.work.pk})
        self.assertContains(self.response, 'href="{0}"'.format(work_workers_url))
        

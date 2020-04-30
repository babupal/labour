from django.urls import reverse , resolve
from ..views import work_workers
from ..models import Work
from django.test import TestCase


class WorkWorkersTests(TestCase):
    def setUp(self):
        self.work = Work.objects.create(
            name='Plumber', description='Plumbing.')

    def test_work_workers_view_success_status_code(self):
        url = reverse('work_workers', kwargs={'pk': self.work.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_work_workers_view_not_found_status_code(self):
        url = reverse('work_workers', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_work_workers_url_resolves_work_workers_view(self):
        view = resolve('/works/1/')
        self.assertEquals(view.func, work_workers)

##    def test_work_workers_view_contains_link_back_to_homepage(self):
##        work_workers_url = reverse('work_workers', kwargs={'pk': self.work.pk})
##        response = self.client.get(work_workers_url)
##        homepage_url = reverse('home')
##        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_work_workers_view_contains_navigation_links(self):
        work_workers_url = reverse('work_workers', kwargs={'pk': self.work.pk})
        homepage_url = reverse('home')
        new_worker_url = reverse('new_worker', kwargs={'pk': self.work.pk})
        
        response = self.client.get(work_workers_url)
        
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_worker_url))
        

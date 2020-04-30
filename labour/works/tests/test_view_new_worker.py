from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse , resolve

from ..forms import NewWorkerForm
from ..models import Work, Worker, Assignment
from ..views import new_worker

# test_view_new_worker

#from datetime import datetime
  
class NewWorkerTests(TestCase):
    def setUp(self):
        self.work=Work.objects.create(name='Elec', description='Electrician.')
        print(" In New Worker Tests Crated Work with name " + self.work.name)
        print("self.work is " + str(self.work.id))
        User.objects.create_user(
            username='john', email='john@doe.com', password='123'
            )
        self.client.login(username='john', password='123')
        
    def test_new_worker_view_success_status_code(self):
        url = reverse('new_worker', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_worker_view_not_found_status_code(self):
        url = reverse('new_worker', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_worker_url_resolves_new_worker_view(self):
        view = resolve('/works/1/new/')
        self.assertEquals(view.func, new_worker)

    def test_new_worker_view_contains_link_back_to_work_workers_view(self):
        new_worker_url = reverse('new_worker', kwargs={'pk': 1})
        work_workers_url = reverse('work_workers', kwargs={'pk': 1})
        response = self.client.get(new_worker_url)
        self.assertContains(response, 'href="{0}"'.format(work_workers_url))

    def test_csrf(self):
        url = reverse('new_worker', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):  # <- new test
        url = reverse('new_worker', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewWorkerForm)

    def test_new_worker_valid_post_data(self):
        print("Inside test_new_worker_valid_post_data(self)")
        url = reverse('new_worker', kwargs={'pk': 1})
        data = {
            'short_name': 'Duguna',
            'full_Name': 'Duguna Jameendar',
            'asg_start_date':'2020-04-29',
##            'asg_end_date':'2020-04-29',
##            'aadhaar_number': '123456789012',
##            'telephone_number':'1234432112',
##            'local_address': 'Local address',
##            'permanent_address': 'Permanent Address',
##            'last_updated': '2020-04-21',#datetime.now(),
##            'dob':'2020-04-21',#datetime.today(),
##            'work':Work.objects.first()
        }
        response = self.client.post(url, data)
        self.assertTrue(Worker.objects.exists())
        self.assertTrue(Assignment.objects.exists())

    def test_new_worker_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        print("test_new_worker_invalid_post_data(self)")
        url = reverse('new_worker', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

####    def test_new_worker_invalid_post_data(self):  # <- updated this one
####        '''
####        Invalid post data should not redirect
####        The expected behavior is to show the form again with validation errors
####        '''
####        url = reverse('new_worker', kwargs={'pk': 1})
####        response = self.client.post(url, {})
####        #form = response.context.get('form')
####        self.assertEquals(response.status_code, 200)
####        #self.assertTrue(form.errors)
##
##
    def test_new_worker_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        print("Inside test_new_worker_invalid_post_data_empty_fields(self)")
        url = reverse('new_worker', kwargs={'pk': 1})
        data = {
            'short_name': '',
            'asg_start_date':'2020-04-15',
            'full_Name': ''
            #'aadhaar_number': ' ',
            #'telephone_number':'',
            #'local_address': '',
            #'permanent_address': '',
            #'last_updated': '',#datetime.now(),
            #'dob':'',#datetime.today(),
            #'work':''#Work.objects.first()
        }
        print(data)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Worker.objects.exists())
        self.assertFalse(Assignment.objects.exists())

class LoginRequiredNewWorkerTests(TestCase):
    def setUp(self):
        Work.objects.create(name='Baker', description='Bakery Worker.')
        self.url = reverse('new_worker', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))



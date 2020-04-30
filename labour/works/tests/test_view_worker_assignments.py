from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Work, Assignment, Worker
from ..views import worker_assignments

class WorkerAssignmentsTests(TestCase):
    def setUp(self):
        work = Work.objects.create(name='Tailor', description='Tailor.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        worker = Worker.objects.create(
##            subject='Hello, world', board=board, starter=user
            short_name = 'Manoj',
            full_Name = 'Tailor Manot',
            aadhaar_number = '123456789021',
            telephone_number = '1234567890',
            local_address = 'Here, very Near',
            permanent_address = 'There, very far',
            work = work,
            created_by = user
            )
        Assignment.objects.create(
##            message='Lorem ipsum dolor sit amet', topic=topic, created_by=user
            worker=worker,
            asg_start_date='2020-04-29',#date.today(),
            asg_end_date='2020-04-29',#date.today(),
##            created_at=datetime.now(),
##            updated_at=datetime.now(),
            created_by=user,
            updated_by=user
            )
        url = reverse('worker_assignments', kwargs={'pk': work.pk, 'worker_pk': worker.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/works/2/workers/6/')
        self.assertEquals(view.func, worker_assignments)




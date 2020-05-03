#from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Work(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def get_assignments_count(self):
        return Assignment.objects.filter(worker__work=self).count()

    def get_last_assignment(self):
        return Assignment.objects.filter(worker__work=self).order_by('-created_at').first()

class Worker(models.Model):
    short_name = models.CharField(max_length=20)
    full_Name = models.CharField(max_length=60)
    aadhaar_number = models.CharField(max_length=12)
    telephone_number = models.CharField(max_length=10)
    local_address = models.CharField(max_length=255,null=True)
    permanent_address = models.CharField(max_length=255,null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    dob = models.DateField(null=True)
    work = models.ForeignKey(Work,on_delete = models.PROTECT, related_name='workers')
    created_by = models.ForeignKey(User, on_delete = models.PROTECT, related_name='workers')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.short_name

    def get_assignments_count(self):
        return Assignment.objects.filter(worker=self).count()

    def get_last_assignment(self):
        return Assignment.objects.filter(worker=self).order_by('-created_at').first()

class Assignment(models.Model):
    worker = models.ForeignKey(Worker, related_name='assignments',on_delete = models.PROTECT)
    asg_start_date = models.DateField(null=True)
    asg_end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete = models.PROTECT,related_name='assignments')
    updated_by = models.ForeignKey(User, on_delete = models.PROTECT,null=True, related_name='+')
    
    def __str__(self):
        worker_asg_st_date = self.worker.short_name + '-' + self.asg_start_date.strftime ('%Y%m%d')
        return worker_asg_st_date


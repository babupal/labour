from django import forms
from .models import Worker,Assignment

class NewWorkerForm(forms.ModelForm):
    asg_start_date = forms.DateField(widget=forms.DateInput())
    
    class Meta:
        model = Worker
        fields = ['short_name','full_Name','aadhaar_number','telephone_number',
            'local_address','permanent_address',
            'dob',
                  #'work',
                  'created_by','asg_start_date']

class AddAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['asg_start_date','asg_end_date','updated_at','updated_by', ]

from django import forms
from .models import Worker

class NewWorkerForm(forms.ModelForm):
    asg_start_date = forms.DateField(widget=forms.DateInput())
##    short_name = forms.TextInput(attrs={'size': 20, 'title': 'Your name'})
##    full_Name = forms.CharField(
##        widget=forms.Textarea(),
##        max_length=60,
##        help_text='The max length of the text is 60.'
##    )
##    aadhaar_number=forms.TextInput(attrs={'size': 12})
##    telephone_number=forms.TextInput(attrs={'size': 10})
##    asg_start_date = forms.DateField()
##    asg_end_date = forms.DateField()
##    local_address = forms.CharField(
##        widget=forms.Textarea(),
##        max_length=120,
##        help_text='The max length of the text is 120.'
##    )
##    permanent_address = forms.CharField(
##        widget=forms.Textarea(),
##        max_length=120,
##        help_text='The max length of the text is 120.'
##    )
##    dob = forms.DateField(widget=forms.DateInput())
    
    class Meta:
        model = Worker
        fields = ['short_name','full_Name','aadhaar_number','telephone_number',
            'local_address','permanent_address',
            'dob',
                  #'work',
                  'created_by','asg_start_date']


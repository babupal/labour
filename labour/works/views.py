from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewWorkerForm
from .models import Work, Worker, Assignment
from datetime import datetime #todays_date = datetime.now()
from django.contrib.auth.decorators import login_required

def home(request):
    works = Work.objects.all()
    return render(request, 'home.html', {'works': works})

def work_workers(request, pk):
    work = get_object_or_404(Work, pk=pk)
    return render(request, 'workers.html', {'work': work})

##def new_worker(request, pk):
##    work = get_object_or_404(Work, pk=pk)
##    return render(request, 'new_worker.html', {'work': work})

##def new_worker(request, pk):
##    work = get_object_or_404(Work, pk=pk)
##
##    if request.method == 'POST':
##        
##        if 'short_name' in request.POST:            
##            short_name = request.POST['short_name']
##        else:
##            short_name = 'Not_Found'
##            
##        if 'asg_start_date' in request.POST:            
##            asg_start_date = request.POST['asg_start_date']
##        else:
##            asg_start_date = datetime.today()
##            
##        if 'full_Name' in request.POST:            
##            full_name = request.POST['full_Name']
##        else:
##            full_name = 'No_full_name'
####        full_name = request.POST['full_name']
####        asg_start_date = request.POST['asg_start_date']
##        if 'asg_end_date' in request.POST:              
##            asg_end_date = request.POST['asg_end_date']
##        else:
##            asg_end_date = datetime.today()    
####        asg_end_date = request.POST['asg_end_date']
##
##        if 'aadhaar_number' in request.POST:            
##            aadhaar_number = request.POST['aadhaar_number']
##        else:
##            aadhaar_number = 'no aadhaar'
##        if 'telephone_number' in request.POST:            
##            telephone_number = request.POST['telephone_number']
##        else:
##            telephone_number = 'no tel'
##        if 'dob' in request.POST:            
##            dob = request.POST['dob']
##        else:
##            dob = datetime.today()
##        if 'local_address' in request.POST:
##            local_address = request.POST['local_address']
##        else:
##            local_address = 'Empty'
##        if 'permanent_address' in request.POST:
##            permanent_address = request.POST['permanent_address']
##        else:
##            permanent_address = 'Empty'
##            
####        telephone_number = request.POST['telephone_number']
####        local_address = request.POST['local_address']
####        permanent_address = request.POST['permanent_address']
####        dob = request.POST['dob']
##            
##        
##        user = User.objects.first()  # TODO: get the currently logged in user
##
##        worker = Worker.objects.create(
##            short_name=short_name,
##            full_Name = full_name,
##            aadhaar_number=aadhaar_number,
##            telephone_number=telephone_number,
##            local_address=local_address,
##            permanent_address=permanent_address,
##            dob = dob,
##            work=work,
##            created_by=user
##        )
##
##        assignment = Assignment.objects.create(
##            asg_start_date = asg_start_date,
##            asg_end_date = asg_end_date,
##            worker=worker,
##            created_by=user
##        )
##        return redirect('work_workers', pk=work.pk)  # TODO: redirect to the created worker page
##    return render(request, 'new_worker.html', {'work': work})

@login_required
def new_worker(request, pk):
    print("In Views.py Entering new worker")
    work = get_object_or_404(Work, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        print("Method is POST")
        form = NewWorkerForm(request.POST)
        if form.is_valid():
#            worker = form.save()
            print("form.is_valid")
            worker = form.save (commit=False)
            print("worker is " + worker.short_name)
            worker.work = work
            worker.created_by = request.user
            worker.save()
            print("worker saved " + worker.full_Name)
            asg_st_date = form.cleaned_data.get('asg_start_date')
            assignment = Assignment.objects.create(
                #asg.start_date = form.cleaned_data.get('asg_start_date'),                
                asg_start_date=asg_st_date,
                #asg_end_date=asg_end_date,
                worker=worker,
                created_by=request.user
            )
            print("Assignment saved with st date " + asg_st_date.strftime("%d-%m-%Y"))
        return redirect('work_workers', pk=pk, work_pk=work.pk)  # TODO:(Done) redirect to the created worker page
    else:
        form = NewWorkerForm()        
    return render(request, 'new_worker.html', {'work': work,'form': form})
    
def worker_assignments(request, pk, worker_pk):
    print("inside worker_assignments pk " + pk + ' worker pk ' + worker_pk)
    worker = get_object_or_404(Worker, work__pk=pk, pk=worker_pk)
    return render(request, 'worker_assignments.html', {'worker': worker})

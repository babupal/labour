from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewWorkerForm,AddAssignmentForm
from .models import Work, Worker, Assignment

from datetime import datetime #todays_date = datetime.now()
from django.contrib.auth.models import User
from django.views.generic import View, UpdateView

from django.utils import timezone

def home(request):
    works = Work.objects.all()
    return render(request, 'home.html', {'works': works})

def work_workers(request, pk):
    work = get_object_or_404(Work, pk=pk)
    workers = work.workers.order_by('-last_updated').annotate(asgs=Count('assignments'))
    return render(request, 'workers.html', {'work': work, 'workers': workers})


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
            print("Redirecting to worker_assignments with pk work_pk "
                   + str(pk) + ' ' + str(work.pk))
##            print("Redirecting to work_workers with pk " + str(pk))

##        return redirect('work_workers', pk=work.pk)  # TODO:(Done) redirect to the created worker page
        return redirect('worker_assignments', pk=pk, worker_pk=worker.pk)  # TODO:(Done) redirect to the created worker page
    else:
        print("request_method " + request.method)
        form = NewWorkerForm()        
    return render(request, 'new_worker.html', {'work': work,'form': form})
    
def worker_assignments(request, pk, worker_pk):
    print("inside worker_assignments pk " + pk + ' worker pk ' + worker_pk)
    worker = get_object_or_404(Worker, work__pk=pk, pk=worker_pk)
    print("Worker Name is " + worker.short_name)
    worker.views += 1
    worker.save()
    return render(request, 'worker_assignments.html', {'worker': worker})

@login_required
def add_assignment_worker(request, pk, worker_pk):
    print("In add_assignment_worker with pk worker_pk "  + str(pk) + ' ' + str(worker_pk))
    worker = get_object_or_404(Worker, work__pk=pk, pk=worker_pk)
    worker.views += 1
    worker.save()
    if request.method == 'POST':
        form = AddAssignmentForm(request.POST)
        if form.is_valid():
            print("form is valid")
            assignment = form.save(commit=False)
            assignment.worker = worker
            assignment.created_by = request.user
            assignment.save()
            print("form is saved")
            print("redirecting to worker_assignments with pk worker_pk" +
                str(pk) + ' ' + str(worker_pk))
            return redirect('worker_assignments', pk=pk, worker_pk=worker_pk)
    else:
        form = AddAssignmentForm()
        print(" request method is " + request.method)
        print(" rendering add_assignment_worker.html")
    return render(request, 'add_assignment_worker.html', {'worker': worker, 'form': form})

##def new_assignment(request):
##    if request.method == 'POST':
##        form = AddAssignmentForm(request.POST)
##        if form.is_valid():
##            form.save()
##            return redirect('assignment_list')
##    else:
##        form = AddAssignmentForm()
##    return render(request, 'new_assignment.html', {'form': form})
##
##class NewAssignmentView(View):
##    def post(self, request):
##        form = AddAssignmentForm(request.POST)
##        if form.is_valid():
##            form.save()
##            return redirect('assignment_list')
##        return render(request, 'new_assignment.html', {'form': form})
##
##    def get(self, request):
##        form = AddAssignmentForm()
##        return render(request, 'new_assignment.html', {'form': form})

class AssignmentUpdateView(UpdateView):
    print("Enter AssignmentUpdateView")
    model = Assignment
    fields = ('asg_start_date','asg_end_date' )
    template_name = 'edit_assignment.html'
    pk_url_kwarg = 'assignment_pk'
    context_object_name = 'assignment'
    
    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.updated_by = self.request.user
        assignment.updated_at = timezone.now()
        assignment.save()        
        print("form saved awwpk awpk" + str(assignment.worker.work.pk) + ' ' + str(assignment.worker.pk))
        return redirect('worker_assignments', pk=assignment.worker.work.pk, worker_pk=assignment.worker.pk)

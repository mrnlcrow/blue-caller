from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from jobs.models import Worker, Customer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

def index(request):
    return HttpResponse("<h1>BlueCaller</h1>")

#class based view - reduces the code and simplifies
class WorkerListView(ListView):
    model = Worker

class WorkerDetailView(LoginRequiredMixin,DetailView):
    model = Worker

    def get_queryset(self):
        # Return all workers initially
        return Worker.objects.all()

    def get_object(self, queryset=None):
        # Get the worker object based on the provided ID
        worker = super().get_object(queryset)
        
        # Ensure that the user is either the owner of the worker or a customer
        if self.request.user != worker.owner and not hasattr(self.request.user, 'customer'):
            # Raise 404 if the user is not authorized to view the worker's detail
            raise PermissionDenied("You do not have permission to view this worker's details.")
        
        return worker

class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    fields=['name','profile_pic','tagline','phone_number','bio']
    success_url=reverse_lazy('worker-list')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super(WorkerCreateView, self).form_valid(form)

# naming convention of the templates for these classes ..CreateView expect is model_form.html

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields=['name','profile_pic','phone_number']
    success_url=reverse_lazy('worker-list')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super(CustomerCreateView, self).form_valid(form)    

@login_required
def handle_login(request):
    # check if user has a worker/customer account -> take them home
    # if they don't , render some template where they can select one or the other

    if request.user.get_worker() or request.user.get_customer():
        return redirect(reverse_lazy('worker-list'))
    
    return render(request,'jobs/choose_account.html',{})
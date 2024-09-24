from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from jobs.models import Worker, Customer
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return HttpResponse("<h1>BlueCaller</h1>")

#class based view - reduces the code and simplifies
class WorkerListView(ListView):
    model = Worker

class WorkerDetailView(DetailView):
    model = Worker

class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    fields=['name','profile_pic','tagline','phone_number','bio','citizenship_image', 'certificate_file']
    success_url=reverse_lazy('worker-list')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super(WorkerCreateView, self).form_valid(form)
    
    def add_worker(request):
        if request.method == 'POST':
            form = WorkerCreateView(request.POST, request.FILES)  # Include request.FILES to handle file uploads
            if form.is_valid():
                form.save()  # Save the worker instance
                return redirect('success')  # Redirect after a successful submission
        else:
            form = WorkerCreateView()

        return render(request, 'add_worker.html', {'form': form})

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
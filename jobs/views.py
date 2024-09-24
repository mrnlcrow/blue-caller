from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from jobs.models import Worker, Customer

def index(request):
    return HttpResponse("<h1>BlueCaller</h1>")

#class based view - reduces the code and simplifies
class WorkerListView(ListView):
    model = Worker

class WorkerDetailView(DetailView):
    model = Worker

class WorkerCreateView(CreateView):
    model = Worker
    fields=['name','tagline','phone_number','bio']
    success_url=reverse_lazy('worker-list')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super(WorkerCreateView, self).form_valid(form)

# naming convention of the templates for these classes ..CreateView expect is model_form.html

class CustomerCreateView(CreateView):
    model = Customer
    fields=['name','phone_number']
    success_url=reverse_lazy('worker-list')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super(WorkerCreateView, self).form_valid(form)    

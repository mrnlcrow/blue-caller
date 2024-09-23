from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from jobs.models import Worker

def index(request):
    return HttpResponse("<h1>BlueCaller</h1>")

#class based view - reduces the code and simplifies
class WorkerListView(ListView):
    model = Worker

class WorkerDetailView(DetailView):
    model = Worker


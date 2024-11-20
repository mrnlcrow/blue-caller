from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from jobs.models import Worker, Customer, Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail

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
    fields=['name','profile_pic','tagline','phone_number','bio','citizenship_image', 'certificate_file']
    success_url=reverse_lazy('worker-list')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        form.instance.latitude = self.request.POST.get('latitude')
        form.instance.longitude = self.request.POST.get('longitude')
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
        form.instance.latitude = self.request.POST.get('latitude')
        form.instance.longitude = self.request.POST.get('longitude')
        form.instance.owner=self.request.user
        return super(CustomerCreateView, self).form_valid(form)    

@login_required
def handle_login(request):
    # check if user has a worker/customer account -> take them home
    # if they don't , render some template where they can select one or the other

    if request.user.get_worker() or request.user.get_customer():
        return redirect(reverse_lazy('worker-list'))
    
    return render(request,'jobs/choose_account.html',{})

def appoint_worker(request, worker_id):

    worker = get_object_or_404(Worker, id = worker_id)
    customer = get_object_or_404(Customer, owner=request.user)
    appointment = Appointment.objects.create(
        customer = customer,
        worker = worker,
        appointment_date = timezone.now(),
        status = 'pending'
    )
    worker.appointed = True
    worker.appointment_date = appointment.appointment_date
    worker.save()
    messages.success(request, "Worker has been appointed and notified sucessfully.")
    return redirect('worker-list')

def send_email_to_worker(worker):
    subject = "Appointment Details"
    message = f"Dear {worker.name},\n\n You have been appointed on {worker.appointment_date}.\n\nThankyou!"
    from_email = "mitas.player@gmail.com"
    recipent_list = [worker.email]
    send_mail(subject, message, from_email, recipent_list)

def customer_appointments(request):
    # Assuming the logged-in user is a customer
    customer = get_object_or_404(Customer, owner=request.user)
    appointments = Appointment.objects.filter(customer=customer)
    return render(request, 'jobs/customer_appointments.html', {'appointments': appointments})

# View for Workers to Manage Appointments
def worker_appointments(request):
    # Assuming the logged-in user is a worker
    worker = get_object_or_404(Worker, owner=request.user)
    appointments = Appointment.objects.filter(worker=worker)
    return render(request, 'jobs/worker_appointments.html', {'appointments': appointments})

def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = 'accepted'
        appointment.save()
    return redirect('worker_appointments')

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = 'rejected'
        appointment.save()
    return redirect('worker_appointments')

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Ensure that only the customer or worker associated with the appointment can delete it
    if request.user == appointment.customer.owner or request.user == appointment.worker.owner:
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this appointment.")
    
    return redirect('customer_appointments')  # Redirect back to customer appointments page
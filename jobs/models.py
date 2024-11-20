from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.
class Worker(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10, unique=True)
    tagline=models.CharField(max_length=100)
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(upload_to="profiles/", blank=True)
    verified = models.BooleanField(default=False)
    citizenship_image = models.ImageField(upload_to='citizenship/', blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    latitude = models.CharField(max_length=20,null=True,blank=True)
    longitude = models.CharField(max_length=20,null=True,blank=True)
    appointed = models.BooleanField(default=False)
    appointment_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.id} | {self.name}"
    
class Customer(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10, unique=True)
    profile_pic=models.ImageField(upload_to="profiles/", blank=True)
    latitude = models.CharField(max_length=20,null=True,blank=True)
    longitude = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return f"{self.id} | {self.name}"
    

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_appointments')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='worker_appointments')
    appointment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.worker} on {self.date}"

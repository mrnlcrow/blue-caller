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


    def __str__(self):
        return f"{self.id} | {self.name}"
    
class Customer(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10, unique=True)
    profile_pic=models.ImageField(upload_to="profiles/", blank=True)
    
    def __str__(self):
        return f"{self.id} | {self.name}"
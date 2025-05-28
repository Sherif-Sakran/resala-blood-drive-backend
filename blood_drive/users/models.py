from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('operator', 'Operator'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='donor')
    title = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f'{self.username} - {self.role}' 
    
class DonorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    blood_type = models.CharField(max_length=3)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_type}"

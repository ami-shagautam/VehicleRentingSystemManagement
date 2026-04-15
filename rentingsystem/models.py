from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
# from . import forms
from django import forms
from django.core.exceptions import ValidationError


# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,blank=True)
    address=models.TextField(blank=True)
    location=models.CharField(max_length=100,blank=True)
    profile_picture=models.ImageField(upload_to='profile',blank=True,null=True)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='category',blank=True,null=True)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vehicles')
    name = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicle')
    is_available=models.BooleanField(default=True)
    description=models.TextField(blank=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    
class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_days = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.id}: {self.user.username} - {self.vehicle.name} ({self.status})"

    def save(self, *args, **kwargs):
        # Calculate total days and total cost automatically
        if self.start_date and self.end_date and self.vehicle_id:
            self.total_days = max((self.end_date - self.start_date).days + 1, 1)
            self.total_cost = Decimal(self.total_days) * self.vehicle.price_per_day
        super().save(*args, **kwargs)
    

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('refunded','Refunded')
    ]
    PAYMENT_METHODS = [
        ('COD','Cash on Delivery'),
        ('esewa',"E-sewa"),
        ('khalti','Khalti')
    ]

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='COD')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id}: {self.status}"

    def mark_paid(self, method='COD'):
        self.status = 'completed'
        self.method = method
        self.paid_at = timezone.now()
        self.save()

        # Update booking status
        self.booking.status = 'confirmed'  # mark booking as confirmed after payment
        self.booking.save()

        # Update vehicle availability
        self.booking.vehicle.is_available = False  # vehicle is now booked
        self.booking.vehicle.save()
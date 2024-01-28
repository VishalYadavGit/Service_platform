from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('electrician', 'Electrician'),
        ('plumber', 'Plumber'),
        # Add more categories as needed
    ]
    types_choices = [
        ('service', 'Service'),
        # Add more categories as needed
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='electrician')
    types = models.CharField(max_length=20, choices=types_choices, default='service')
    rating = models.FloatField()
    total_reviews = models.IntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='service_photos/')
    def __str__(self):
        return self.name
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electrician', 'Electrician'),
        ('plumber', 'Plumber'),
        # Add more categories as needed
    ]
    types_choices = [
        ('product', 'Product'),
        # Add more categories as needed
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='electrician')
    types = models.CharField(max_length=20, choices=types_choices, default='product')
    rating = models.FloatField()
    total_reviews = models.IntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photos/')    
    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    picture=models.ImageField(upload_to='uploads/')
    address=models.CharField(max_length=255)
    pincode=models.IntegerField()

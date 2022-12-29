import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='customer/avatars', blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=255,blank=True)    
    stripe_payment_method_id = models.CharField(max_length=255,blank=True)
    stripe_card_last4 = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Category(models.Model):
    slug = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)  

    def __str__(self):
        return self.name

class Job(models.Model):
    SMALL_SIZE = "small"
    MEDIUM_SIZE = "medium"
    LARGE_SIZE = "large"
    SIZES = (
        (SMALL_SIZE,"small"),
        (MEDIUM_SIZE,"medium"),
        (LARGE_SIZE,"large"),
    )

    CREATING_STATUS = 'creating'
    PROCESSING_STATUS = 'processing'
    PICKING_STATUS = 'picking'
    DELIVERING_STATUS = 'delivering'
    COMPLETED_STATUS = 'completed'
    CANCELLED_STATUS = 'cancelled'

    STATUSES = (
        (CREATING_STATUS,'creating'),
        (PROCESSING_STATUS,'processing'),
        (PICKING_STATUS,'picking'),
        (DELIVERING_STATUS,'delivering'),
        (COMPLETED_STATUS,'completed'),
        (CANCELLED_STATUS, 'cancelled')

    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250) 
    description = models.CharField(max_length=250,null=True,blank=True)  
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=20,choices=SIZES, default=MEDIUM_SIZE )
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='job/photos/')
    status = models.CharField(max_length=20,choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

from django.db import models
import uuid
from django.utils import timezone
from core.models import Courier,Customer
from accounts.models import User
from django.utils.text import slugify



class Address(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    aid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstaddress = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.street
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=250, unique=True, blank=True, null=True) 
    lid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


#Category Model
class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)  
    description = models.TextField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=250, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='category/photos/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Modifier(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    

class ModifierGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mgid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    modifiers = models.ManyToManyField(Modifier, related_name='groups',blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=255, blank=True, null=True)
    category = models.ManyToManyField(Category,null=True, blank=True)
    modifier_groups = models.ManyToManyField(ModifierGroup, related_name='products',null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='product/photos/', null=True, blank=True)
    location = models.ManyToManyField(Restaurant, related_name='location',null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Menu(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ManyToManyField(Restaurant, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250,null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, null=True)
    product = models.ManyToManyField(Product, blank=True, null=True)
    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

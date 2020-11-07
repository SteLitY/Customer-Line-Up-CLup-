from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms 

class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField() 

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=12, blank=False)
    is_customer = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class All_Customers(models.Model):
    name = models.CharField(max_length=30, default="")
    position = models.IntegerField(default=0)
    group_size = models.IntegerField(default=10)
    def __iter__(self):
        return iter([self.name, self.position, self.group_size])


#Customer Registration
class Customer(models.Model):
    username = models.CharField(max_length=30, default="")
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, default="123@gmail.com")
    phone_number = models.CharField(max_length=12, default="")
    is_customer = models.BooleanField(default=True)
    is_business = models.BooleanField(default=False)
    def __str__(self):
        return self.username

#business table
class Business(models.Model):
    username = models.CharField(max_length=30, default="")
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, default="123@gmail.com")
    phone_number = models.CharField(max_length=12, default="")
    store_name = models.CharField(max_length=100, default="")
    store_number = models.CharField(max_length=12, default="")
    store_address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=30, default="New York")
    state = models.CharField(max_length=2, default="")
    zipcode = models.CharField(max_length=5, default="")
    is_customer = models.BooleanField(default=False)
    is_business = models.BooleanField(default=True)
    # business hours
    sunday_open = models.CharField(max_length=5, default="00:00")
    sunday_closed = models.CharField(max_length=5, default="00:00")
    monday_open = models.CharField(max_length=5, default="00:00")
    monday_closed = models.CharField(max_length=5, default="00:00")
    tuesday_open = models.CharField(max_length=5, default="00:00")
    tuesday_closed = models.CharField(max_length=5, default="00:00")
    wednesday_open = models.CharField(max_length=5, default="00:00")
    wednesday_closed = models.CharField(max_length=5, default="00:00")
    thursday_open = models.CharField(max_length=5, default="00:00")
    thursday_closed = models.CharField(max_length=5, default="00:00")
    friday_open = models.CharField(max_length=5, default="00:00")
    friday_closed = models.CharField(max_length=5, default="00:00")
    saturday_open = models.CharField(max_length=5, default="00:00")
    saturday_closed = models.CharField(max_length=5, default="00:00")
    #capacity
    store_capacity = models.IntegerField(default=10)
    #group limit
    group_limit = models.IntegerField(default=1)
    #for queue
    in_line =  models.IntegerField(default=0)
    in_store = models.IntegerField(default=0)
    scheduled = models.IntegerField(default=0)
    #List of cutomers
    all_tickets = models.ForeignKey(All_Customers, on_delete=models.CASCADE, null = True)

    
    def __str__(self):
        return self.store_name

    def __iter__(self):
        return iter([self.username, self.first_name, self.last_name, self.email,
         self.phone_number, self.store_name, self.store_number,
         self.store_address, self.city, self.state, self.zipcode, 
         self.is_customer, self.is_business, self.in_store])
        
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
     instance.profile.save()

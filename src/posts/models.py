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
    password1 =  models.CharField(max_length=30, blank=False)
    is_customer = models.BooleanField(default=True)
    is_business = models.BooleanField(default=False)

#Customer Registration
class Customer(models.Model):
    user = models.OneToOneField(User, default="", on_delete=models.CASCADE)
    username = models.CharField(max_length=30, default="")
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, default="123@gmail.com")
    phone_number = models.CharField(max_length=12, default="")
    password1 =  models.CharField(max_length=30, default="")
    is_customer = models.BooleanField(default=True)
    is_business = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
     instance.profile.save()

#business table
class Business(models.Model):
    business = models.OneToOneField(User, default="", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default="")
    store_name = models.CharField(max_length=100, default="")
    store_number = models.CharField(max_length=12, default="")
    store_address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=30, default="New York")
    state = models.CharField(max_length=2, default="")
    zipcode = models.CharField(max_length=5, default="")
    input_sex = models.CharField(max_length=3, default="")
    is_customer = models.BooleanField(default=False)
    is_business = models.BooleanField(default=True)


# @receiver(post_save, sender=User)
# def create_business_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profileb(sender, instance, **kwargs):
#     instance.profile.save()


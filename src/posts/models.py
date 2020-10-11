from django.db import models

# Create your models here.

class Test(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms 

class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField() 

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField() 

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=31, blank=True)
    cell_number = models.CharField(max_length=12, blank=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#business table
class business(models.Model):
    email = models.CharField(max_length=127, default='')
    first_name = models.CharField(max_length=127, default='')
    middle_name = models.CharField(max_length=127, default='')
    last_name = models.CharField(max_length=127, default='')
    password = models.CharField(max_length=127, default='')
    cellnumber = models.CharField(max_length=127, default='')
